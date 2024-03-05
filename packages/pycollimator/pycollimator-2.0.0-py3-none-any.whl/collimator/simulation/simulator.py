# Copyright (C) 2024 Collimator, Inc.
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, version 3. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General
# Public License for more details.  You should have received a copy of the GNU
# Affero General Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

"""Functionality for simulating hybrid dynamical systems.

This module provides the `simulate` function, which is the primary entry point
for running simulations.  It also defines the `Simulator` class used by `simulate`,
which provides more fine-grained control over the simulation process.
"""

from __future__ import annotations
from functools import partial
import dataclasses
from typing import TYPE_CHECKING, SupportsIndex, Callable, Any

import numpy as np
import jax
import jax.numpy as jnp
from jax import lax

from ..logging import logger
from ..profiling import Profiler

from .types import (
    StepEndReason,
    GuardIsolationData,
    ContinuousIntervalData,
    SimulatorOptions,
    SimulatorState,
    SimulationResults,
    ResultsOptions,
    ResultsMode,
)

from ..backend import ODESolver, ResultsData, numpy_api as cnp, io_callback

from ..framework import (
    IntegerTime,
    is_event_data,
    ZeroCrossingEvent,
)
from collimator import backend

if TYPE_CHECKING:
    from ..backend.ode_solver import ODESolverBase, ODESolution
    from ..framework import ContextBase, SystemBase
    from ..framework.port import OutputPort
    from ..framework.event import PeriodicEventData, EventCollection


__all__ = [
    "estimate_max_major_steps",
    "simulate",
    "Simulator",
]


def _raise_end_time_not_reached(tf, ctx_time, reason):
    if ((tf - ctx_time) / tf > 1e-3) and (
        reason != StepEndReason.TerminalEventTriggered
    ):
        raise RuntimeError(
            f"Simulator failed to reach specified end time. End time={tf}. "
            f"Reached time={ctx_time}. Try increasing Maximum Major Steps."
        )


@jax.jit
def error_end_time_not_reached(tf, ctx_time, reason):
    jax.debug.callback(_raise_end_time_not_reached, tf, ctx_time, reason)


def _raise_end_time_not_representable(tf, max_tf):
    if tf > max_tf:
        required_scale = tf / max_tf
        current_scale = IntegerTime.time_scale
        raise RuntimeError(
            " "
            f"Requested end time {tf} is greater than max representable time {max_tf}. "
            "Increase the time scale by setting `int_time_scale` in `SimulatorOptions`."
            f"Current time scale is {current_scale}, but this end time requires at least "
            f"time_scale={current_scale * required_scale}. The default value of 1e-12 "
            "(picosecond precision) is only capable of representing times up to ~0.3 "
            "years."
        )


@jax.jit
def error_end_time_not_representable(tf, max_tf):
    jax.debug.callback(_raise_end_time_not_representable, tf, max_tf)


def estimate_max_major_steps(
    system: SystemBase,
    tspan: tuple[float, float],
    max_major_step_length: float = None,
    safety_factor: int = 2,
) -> int:
    """Heuristic for estimating the required number of major steps.

    This is used to bound the number of iterations in the while loop in the
    `simulate` function when automatic differentiation is enabled.  The number
    of major steps is determined by the smallest discrete period in the system
    and the length of the simulation interval.  The number of major steps is
    bounded by the length of the simulation interval divided by the smallest
    discrete period, with a safety factor applied.  The safety factor accounts
    for unscheduled major steps that may be triggered by zero-crossing events.

    This function assumes static time variables, so cannot be called from within
    traced (JAX-transformed) functions.  This is typically the case when the
    beginning or end time of the simulation is a variable that will be
    differentiated.  In this case `estimate_max_major_steps` should be called
    statically ahead of time to determine a reasonable bound for `max_major_steps`.

    Args:
        system (SystemBase): The system to simulate.
        tspan (tuple[float, float]): The time interval to simulate over.
        max_major_step_length (float, optional): The maximum length of a major
            step. If provided, this will be used to bound the number of major
            steps. Otherwise it will be ignored.
        safety_factor (int, optional): The safety factor to apply to the number of
            major steps.  Defaults to 2.
    """
    # For autodiff of collimator.simulate, this path is not possible, JAX
    # throws an error. To work around this, create:
    #   options = SimulatorOptions(max_major_steps=<my value>)
    # outside collimator.simulate, and pass in like this:
    #   collimator.simulate(my_model, options=options)

    # Find the smallest period amongst the periodic events of the system
    if system.periodic_events.has_events or max_major_step_length is not None:
        # Initialize to infinity - will be overwritten by at least one conditional
        min_discrete_step = np.inf

        # Bound the number of major steps based on the smallest discrete period in
        # the system.
        if system.periodic_events.has_events:
            event_periods = jax.tree_map(
                lambda event_data: event_data.period,
                system.periodic_events,
                is_leaf=is_event_data,
            )
            min_discrete_step = jax.tree_util.tree_reduce(min, event_periods)

        # Also bound the number of major steps based on the max major step length
        # in case that is shorter than any of the update periods.
        if max_major_step_length is not None:
            min_discrete_step = min(min_discrete_step, max_major_step_length)

        # in this case, we assume that, on average, major steps triggered by
        # zero crossing event, will be as frequent or less frequent than major steps
        # triggered by the smallest discrete period.
        # anything less than 100 is considered inadequate. user can override if they want this.
        max_major_steps = max(100, safety_factor * int(tspan[1] // min_discrete_step))
        logger.info(
            "max_major_steps=%s based on smallest discrete period=%s",
            max_major_steps,
            min_discrete_step,
        )
    else:
        # in this case we really have no valuable information on which to make an
        # educated guess. who knows how many events might occurr!!!
        # users will have to iterate.
        max_major_steps = 200
        logger.info(
            "max_major_steps=%s by default since no discrete period in system",
            max_major_steps,
        )
    return max_major_steps


def _check_options(
    system: SystemBase,
    options: SimulatorOptions,
    tspan: tuple[float, float],
    recorded_signals: dict[str, OutputPort],
) -> SimulatorOptions:
    """Check consistency of options and adjust settings where necessary."""

    if options is None:
        options = SimulatorOptions()

    # Check based on the options and the system whether JAX tracing is possible.
    math_backend, enable_tracing = _check_backend(system, options)

    # If we specified JAX but tracing is not enabled, we have fall back to numpy
    # TODO: Reconsider this logic - is there ever a time when untraced JAX is
    # useful, e.g. for debugging?
    if (math_backend == "jax") and not enable_tracing:
        logger.warning(
            "JAX backend is requested but JAX tracing is disabled. Falling back to "
            "numpy backend."
        )
        enable_tracing = False
        math_backend = "numpy"

    # Set the global numerical backend as determined by the options and above logic.
    cnp.set_backend(math_backend)

    if recorded_signals is None:
        recorded_signals = options.recorded_signals
    save_time_series = recorded_signals is not None

    # The while loop must be bounded in order for reverse-mode autodiff to work.
    # Also need this to set buffer sizes for signal recording in compiled JAX.
    # For the NumPy backend, this will be ignored, since neither bounded while
    # loops nor buffered recording is necessary.
    max_major_steps = options.max_major_steps
    if max_major_steps is None or max_major_steps <= 0:
        # logger.warning(
        #     "JAX backend requires a bounded number of major steps. This has not "
        #     "been specified in SimulatorOptions. Using a heuristic to estimate "
        #     "the maximum number of steps. If this fails, it may be because the "
        #     "final time is a traced variable.  If it is necessary to "
        #     "differentiate with respect to the end time of the simulation, then "
        #     "max_major_steps must be set manually. A reasonable value can be "
        #     "estimated using estimate_max_major_steps."
        # )
        max_major_steps = estimate_max_major_steps(
            system, tspan, options.max_major_step_length
        )

    # Check that the options are configured correctly for autodiff.
    if options.enable_autodiff:
        # JAX tracing is required for automatic differentiation
        if not enable_tracing:
            raise ValueError(
                "Autodiff is only supported with `options.enable_tracing=True`."
            )

        # Cannot record time series during autodiff - only final results can
        # be differentiated
        if save_time_series:
            raise ValueError(
                "Recording output time series is not supported with autodiff."
            )

    # Can optionally rescale integer time to allow for longer simulations or higher
    # precision.  The default integer time step corresponds to 1 picosecond, so
    # the default limit is around 0.3 years.  If the end time is greater than that but
    # less than ~300 years, we can use nanosecond integer time (set scale=1e-9), etc.
    if options.int_time_scale is not None:
        IntegerTime.set_scale(options.int_time_scale)
    error_end_time_not_representable(tspan[1], IntegerTime.max_float_time)

    return dataclasses.replace(
        options,
        recorded_signals=recorded_signals,
        save_time_series=save_time_series,
        max_major_steps=max_major_steps,
        math_backend=math_backend,
        enable_tracing=enable_tracing,
    )


def simulate(
    system: SystemBase,
    context: ContextBase,
    tspan: tuple[float, float],
    options: SimulatorOptions = None,
    results_options: ResultsOptions = None,
    recorded_signals: dict[str, OutputPort] = None,
    postprocess: bool = True,
) -> SimulationResults:
    """Simulate the hybrid dynamical system defined by `system`.

    The parameters and initial state are defined by `context`.  The simulation time
    runs from `tspan[0]` to `tspan[1]`.

    The simulation is "hybrid" in the sense that it handles dynamical systems with both
    discrete and continuous components.  The continuous components are integrated using
    an ODE solver, while discrete components are updated periodically as specified by
    the individual system components. The continuous and discrete states can also be
    modified by "zero-crossing" events, which trigger when scalar-valued guard
    functions cross zero in a specified direction.

    The simulation is thus broken into "major" steps, which consist of the following,
    in order:

    (1) Perform any periodic updates to the discrete state.
    (2) Check if the discrete update triggered any zero-crossing events and handle
        associated reset maps if necessary.
    (3) Advance the continuous state using an ODE solver until the next discrete
        update or zero-crossing, localizing the zero-crossing with a bisection search.
    (4) Store the results data.
    (5) If the ODE solver terminated due to a zero-crossing, handle the reset map.

    The steps taken by the ODE solver are "minor" steps in this simulation.  The
    behavior of the ODE solver and the hybrid simulation in general can be controlled
    by configuring `SimulatorOptions`.  Available settings are as follows:

    SimulatorOptions:
        enable_tracing (bool): Allow JAX tracing for JIT compilation
        max_major_step_length (float): Maximum length of a major step
        max_major_steps (int):
            The maximum number of major steps to take in the simulation. This is
            necessary for automatic differentiation - otherwise the "while" loop
            is non-differentiable.  With the default value of None, a heuristic
            is used to determine the maximum number of steps based on the periodic
            update events and time interval.
        rtol (float): Relative tolerance for the ODE solver. Default is 1e-6.
        atol (float): Absolute tolerance for the ODE solver. Default is 1e-8.
        min_minor_step_size (float): Minimum step size for the ODE solver.
        max_minor_step_size (float): Maximum step size for the ODE solver.
        max_minor_steps_per_major_step (int):
            The usage of this parameter depends on the ODE solver.  For the default
            diffrax solvers, this is the static length of the "for loop" used in
            the ODE solve, as well as the size of the buffer used for storing results.
            The default value of None will map to 16**3=4096 steps.  On the other hand,
            for SciPy solvers, this value determines the number of evenly-spaced time
            points to return in the solution (per major step).  The default value of
            None will map to 100 steps.
        ode_solver_method (str): The ODE solver to use.  Default is "default", which
            will use the diffrax Tsit5 solver if JAX tracing is enabled, otherwise the
            SciPy Dopri5 solver.
        save_time_series (bool):
            This option determines whether the simulator saves any data.  If the
            simulation is initiated from `simulate` this will be set automatically
            depending on whether `recorded_signals` is provided.  Hence, this
            should not need to be manually configured.
        recorded_signals (dict[str, OutputPort]):
            Dictionary of ports or other cache sources for which the time series should
            be recorded. Note that if the simulation is initiated from `simulate` and
            `recorded_signals` is provided as a kwarg to `simulate`, anything set here
            will be overridden.  Hence, this should not need to be manually configured.
        return_context (bool):
            If the context is not needed for anything, opting to not return it can
            speed up compilation times.  For instance, typical simulation calls from
            the UI don't use the context for anything, so model_interface.py will
            set `return_context=False` for performance.
        postprocess (bool):
            If using buffered results recording (i.e. with JAX numerical backend), this
            determines whether to automatically trim the buffer after the simulation is
            complete. This is the default behavior, which will serve unless the full
            call to `simulate` needs to be traced (e.g. with `grad` or `vmap`).

    The return value is a `SimulationResults` object, which is a named tuple containing
    all recorded signals as well as the final context (if `options.return_context` is
    `True`). Signals can be recorded by providing a dict of (name, signal_source) pairs
    Typically the signal sources will be output ports, but they can actually be any
    `SystemCallback` object in the system.

    Args:
        system (SystemBase): The hybrid dynamical system to simulate.
        context (ContextBase): The initial state and parameters of the system.
        tspan (tuple[float, float]): The start and end times of the simulation.
        options (SimulatorOptions): Options for the simulation process and ODE solver.
        results_options (ResultsOptions): Options related to how the outputs are
            stored, interpolated, and returned.
        recorded_signals (dict[str, OutputPort]):
            Dictionary of ports for which the time series should be recorded.

    Returns:
        SimulationResults: A named tuple containing the recorded signals and the final
            context (if `options.return_context` is `True`).

    Notes:
        results_options is currently unused, pending:
            https://collimator.atlassian.net/browse/DASH-1350

        If `recorded_signals` is provided as a kwarg, it will override any entry in
        `options.recorded_signals`. This will be deprecated in the future in favor of
        only passing via `options`.
    """

    options = _check_options(system, options, tspan, recorded_signals)

    if results_options is None:
        results_options = ResultsOptions()

    if results_options.mode != ResultsMode.auto:
        raise NotImplementedError(
            f"Simulation output mode {results_options.mode.name} is not supported. "
            "Only 'auto' is presently supported."
        )

    # HACK: Wildcat presently does not use interpolant to produce
    # results sample between minor_step end times, so we clamp
    # the minor step size to the max_results_interval instead.
    if (
        results_options.max_results_interval is not None
        and results_options.max_results_interval > 0
        and results_options.max_results_interval < options.max_minor_step_size
    ):
        options = dataclasses.replace(
            options,
            max_minor_step_size=results_options.max_results_interval,
        )
        logger.info(
            "max_minor_step_size reduced to %s to match max_results_interval",
            options.max_minor_step_size,
        )

    ode_solver = ODESolver(system, options=options.ode_options)

    sim = Simulator(system, ode_solver=ode_solver, options=options)
    logger.info("Simulator ready to start: %s, %s", options, ode_solver)

    # Define a function to be traced by JAX, if allowed, closing over the
    # arguments to `_simulate`.
    def _wrapped_simulate() -> tuple[ContextBase, ResultsData]:
        t0, tf = tspan
        initial_context = context.with_time(t0)
        sim_state = sim.advance_to(tf, initial_context)
        error_end_time_not_reached(
            tf, sim_state.context.time, sim_state.step_end_reason
        )
        final_context = sim_state.context if options.return_context else None
        return final_context, sim_state.results_data

    # JIT-compile the simulation, if allowed
    if options.enable_tracing:
        _wrapped_simulate = jax.jit(_wrapped_simulate)
        _wrapped_simulate = Profiler.jaxjit_profiledfunc(
            _wrapped_simulate, "_wrapped_simulate"
        )

    # Run the simulation
    final_context, results_data = _wrapped_simulate()

    if postprocess and results_data is not None:
        time, outputs = results_data.finalize()
    else:
        time, outputs = None, None

    # Reset the integer time scale to the default value in case we decreased precision
    # to reach the end time of a long simulation.  Typically this won't do anything.
    if options.int_time_scale is not None:
        IntegerTime.set_default_scale()

    return SimulationResults(
        final_context,
        time=time,
        outputs=outputs,
    )


class Simulator:
    """Class for orchestrating simulations of hybrid dynamical systems.

    See the `simulate` function for more details.
    """

    def __init__(
        self,
        system: SystemBase,
        ode_solver: ODESolverBase = None,
        options: SimulatorOptions = None,
    ):
        """Initialize the simulator.

        Args:
            system (SystemBase): The hybrid dynamical system to simulate.
            ode_solver (ODESolverBase):
                The ODE solver to use for integrating the continuous-time component
                of the system.  If not provided, a default solver will be used.
            options (SimulatorOptions):
                Options for the simulation process.  See `simulate` for details.
        """
        self.system = system

        if options is None:
            options = SimulatorOptions()

        # Determine whether JAX tracing can be used (jit, grad, vmap, etc)
        math_backend, self.enable_tracing = _check_backend(system, options)

        # Set the math backend
        cnp.set_backend(math_backend)

        # Should the simulation be run with autodiff enabled?  This will override
        # the `advance_to` method with a custom autodiff rule.
        self.enable_autodiff = options.enable_autodiff

        if ode_solver is None:
            ode_solver = ODESolver(system, options=options.ode_options)

        # Store configuration options
        self.max_steps = ode_solver.max_steps
        self.max_major_steps = options.max_major_steps
        self.max_major_step_length = options.max_major_step_length
        self.save_time_series = options.save_time_series
        self.recorded_outputs = options.recorded_signals
        self.zc_bisection_loop_count = options.zc_bisection_loop_count
        self.major_step_callback = options.major_step_callback

        if self.max_major_step_length is None:
            self.max_major_step_length = np.inf

        logger.debug("Simulator created with enable_tracing=%s", self.enable_tracing)

        self.ode_solve = ode_solver

        # Modify the default autodiff rule slightly to correctly capture variations
        # in end time of the simulation interval.
        self.has_terminal_events = system.zero_crossing_events.has_terminal_events
        self.advance_to = self._override_advance_to_vjp()

        # Determine if the system has any zero-crossing events.  If so, we need to use
        # the bisection search to localize them.  Otherwise, the logic for advancing
        # continuous time is simpler.
        self.has_zero_crossing_events = system.zero_crossing_events.has_events

        # There are two paths for advancing time depending on whether the model
        # has any continuous state component or not.

        # Note: this only matters for the results saving. when there are
        # continuous states or zero-crossing events, we expect that calling
        # _(un)guarded_integrate() will advance time, and have non-zero time
        # stamped solution samples temporarily stored in ode_sol. When this
        # happens, these time stamped solution samples are then extended with
        # discrete state values "as the system would see them", for this major
        # step.

        # When there are no continuous states nor zero-crossing events, then
        # _(un)guarded_integrate() will only return a time stamped solution sample
        # at the end time of the major step. extending this with the discrete
        # state values "as the system would see them", means that the results
        # returned to the user seem to be delayed in time by one discrete step.
        # to get around this, we simply advance time only after the we extend
        # the solution object with the value of the discrete state/outputs.

        if system.has_continuous_state:
            if self.has_zero_crossing_events:
                self._integrate = self._guarded_integrate
            else:
                self._integrate = self._unguarded_integrate
        else:
            self._integrate = self._stateless_integrate

    def while_loop(self, cond_fun, body_fun, val):
        """Dispatch to JAX or Python while loop depending on tracing status."""
        if not self.enable_tracing:
            while cond_fun(val):
                val = body_fun(val)
            return val
        else:
            # If autodiff is enabled, we need to use a custom while loop with a maximum
            # number of steps so that the loop is reverse-mode differentiable.
            # Otherwise we can use a standard unbounded while loop with lax backend.
            while_loop = partial(_bounded_while_loop, max_steps=self.max_major_steps)
            return while_loop(cond_fun, body_fun, val)

    def cond(self, pred, true_fun, false_fun, args=()):
        """Dispatch to JAX or Python if/else depending on tracing status."""
        if not self.enable_tracing:
            return true_fun(*args) if pred else false_fun(*args)
        else:
            return lax.cond(pred, true_fun, false_fun, *args)

    def for_loop(self, lower: SupportsIndex, upper: SupportsIndex, body_fun, args):
        """Dispatch to JAX or Python for loop depending on tracing status."""
        if not self.enable_tracing:
            for i in range(lower, upper):
                args = body_fun(i, args)
            return args
        else:
            return lax.fori_loop(lower, upper, body_fun, args)

    def initialize(self, context: ContextBase) -> SimulatorState:
        """Perform initial setup for the simulation."""
        logger.debug("Initializing simulator")
        # context.state.pprint(logger.debug)

        # Initial simulation time as integer (picoseconds)
        initial_int_time = IntegerTime.from_decimal(context.time)

        # Ensure that _next_update_time() can return the current time by perturbing
        # current time as slightly toward negative infinity as possible
        time_of_next_timed_event, timed_events = _next_update_time(
            self.system.periodic_events, initial_int_time - 1
        )

        # timed_events is now marked with the active events at the next update time
        logger.debug("Time of next timed event (int): %s", time_of_next_timed_event)
        logger.debug(
            "Time of next event (sec): %s",
            IntegerTime.as_decimal(time_of_next_timed_event),
        )
        timed_events.pprint(logger.debug)

        end_reason = cnp.where(
            time_of_next_timed_event == initial_int_time,
            StepEndReason.TimeTriggered,
            StepEndReason.NothingTriggered,
        )

        # Initialize the results data that will hold recorded time series data.
        if self.save_time_series:
            results_data = ResultsData.initialize(
                context, self.recorded_outputs, self.max_major_steps, self.max_steps
            )
        else:
            results_data = None

        return SimulatorState(
            context=context,
            timed_events=timed_events,
            step_end_reason=end_reason,
            int_time=initial_int_time,
            results_data=results_data,
        )

    def save_results(
        self, results_data: ResultsData, context: ContextBase, ode_sol: ODESolution
    ) -> ResultsData:
        """Update the results data with the current state of the system."""
        if not self.save_time_series:
            return results_data

        return results_data.update(context, ode_sol)

    def _override_advance_to_vjp(self) -> Callable:
        """Construct the `advance_to` method for the simulator.

        See the docstring for `Simulator._advance_to` for details.

        If JAX tracing is enabled for autodiff, wrap the advance function with a
        custom autodiff rule to correctly capture variation with respect to end
        time. If somehow autodiff works with tracing disabled, the derivatives will
        not account for possible variations in end time (for instance in finding
        limit cycles or when there are terminal conditions on the simulation).
        """

        if not self.enable_autodiff:
            return self._advance_to

        # This is the main function call whose autodiff rule will be overridden.
        def _wrapped_advance_to(
            sim: Simulator, boundary_time: float, context: ContextBase
        ) -> SimulatorState:
            return sim._advance_to(boundary_time, context)

        # The "forwards pass" to advance the simulation.  Also stores the nominal
        # VJP calculation and the continuous time derivative value, both of which
        # will be needed in the backwards pass.
        def _wrapped_advance_to_fwd(
            sim: Simulator, boundary_time: float, context: ContextBase
        ) -> tuple[SimulatorState, tuple]:
            primals, vjp_fun = jax.vjp(sim._advance_to, boundary_time, context)

            # Also need to keep the final continuous time derivative value for
            # computing the adjoint time variable
            xdot = sim.system.eval_time_derivatives(primals.context)

            # "Residual" information needed in the backwards pass
            res = (vjp_fun, xdot, primals.step_end_reason)

            return primals, res

        def _wrapped_advance_to_adj(
            _sim: Simulator, res: tuple, adjoints: SimulatorState
        ) -> tuple[float, ContextBase]:
            # Unpack the residuals from the forward pass
            vjp_fun, xdot, reason = res

            # Compute whatever the standard adjoint variables are using the
            # automatically derived VJP function.  The first return variable will
            # be the automatically computed tf_adj value, which we will ignore in
            # favor of the manually derived value computed next.
            _, context_adj = vjp_fun(adjoints)

            # The derivative with respect to end time is just the dot product of
            # the adjoint "seed" continuous state with the final time derivatives.
            # We can overwrite whatever the calculated adjoint time was with this.
            vc = adjoints.context.continuous_state
            vT_xdot = jax.tree_map(lambda xdot, vc: jnp.dot(xdot, vc), xdot, vc)

            # On the other hand, if the simulation ends early due to a terminal
            # event, then the derivative with respect to end time is zero.
            tf_adj = jnp.where(
                reason == StepEndReason.TerminalEventTriggered,
                0.0,
                sum(jax.tree_util.tree_leaves(vT_xdot)),
            )

            # Return adjoints to match the inputs to _wrapped_advance_to, except for
            # the first argument (Simulator), which will be marked nondifferentiable.
            return (tf_adj, context_adj)

        advance_to = jax.custom_vjp(_wrapped_advance_to, nondiff_argnums=(0,))
        advance_to.defvjp(_wrapped_advance_to_fwd, _wrapped_advance_to_adj)

        # Copy the docstring and type hints to the overridden function
        advance_to.__doc__ = self._advance_to.__doc__
        advance_to.__annotations__ = self._advance_to.__annotations__

        return partial(advance_to, self)

    def _guarded_integrate(
        self,
        cdata: ContinuousIntervalData,
    ) -> ContinuousIntervalData:
        """Advance the simulation to the next discrete update or zero-crossing event.

        This stores the values of all active guard functions and advances the
        continuous-time component of the system to the next discrete update or
        zero-crossing event, whichever comes first.  Zero-crossing events are
        localized using a bisection search defined by `_trigger_search`, which will
        also record the final guard function values at the end of the search interval
        and determine which (if any) zero-crossing events were triggered.
        """

        # Unpack inputs
        int_tf = cdata.tf
        context = cdata.context
        results_data = cdata.results_data

        zc_events = self.system.determine_active_guards(context)

        # Save the time and current state
        logger.debug(
            "Integrating from t=%s with xc=%s, xd=%s",
            context.time,
            context.continuous_state,
            context.discrete_state,
        )

        # Record guard function values at the beginning of the interval.
        zc_events = guard_interval_start(zc_events, context)

        # Integrate the ODE to the final time of the major_step. this gets us two
        # things:
        #  1] a context we can use to see if any zero crossings occurred, and if not,
        #   skip localization (which is a fori_loop).
        #  2] an interpolant that we use to localize events in time to within some
        #   'small' interval.
        t_span = (context.time, IntegerTime.as_decimal(int_tf))
        ode_sol, context_tf = self.ode_solve(context, x0=context.state, t_span=t_span)
        zc_events = determine_triggered_guards(zc_events, context_tf)

        def _no_events_fun(cdata, ode_sol, zc_events, context_tf):
            return False, context_tf, ode_sol, zc_events, cdata.tf

        def _localize_zero_crossings(cdata, ode_sol, zc_events, context_tf):
            # Using the ODE solver interpolant, employ bisection to find a 'small' time
            # interval within which the earliest zero crossing occurrs. See
            # _bisection_step_fun for details about how bisection is employed for
            # localizing the zero crossing in time.
            context_t0 = cdata.context
            _body_fun = partial(_bisection_step_fun, ode_sol.step_interpolant)
            carry = GuardIsolationData(cdata.t0, cdata.tf, zc_events, context_t0)
            search_data = self.for_loop(
                0, self.zc_bisection_loop_count, _body_fun, carry
            )

            # It is important to note that the above process does not _always_ terminate
            # with guards.has_triggered == True. The reason for this is because the goal
            # of the above is _not_ to check _if_ a guard triggered, but rather to find
            # a small interval within which a guard _will_ trigger. Using bisection to
            # find this interval means that sometimes bisection evaluates an interval in
            # which a guards triggures, and sometimes not, and uses this to determine
            # which subinterval to search next. It's perfectly acceptable to find the
            # interval, eventh if last subinterval searched did not have a triggered guard.
            # The consequence of this is that we cannot use guards.has_triggered here, or
            # in testing to verify that event localization is "working correctly".

            # Integrate the ODE to the final time of the major_step after localizing events.
            # The reason has to do with how we use the saved 'steps' in the ode_sol to
            # determine and save results samples. we need an ode_sol that goes exactly from
            # the beginning of the major step to the end.
            # https://collimator.atlassian.net/browse/WC-191 aims to avoid this second call
            # and produce results samples differently.
            int_tf = search_data.zc_after_time
            t_span = (context_t0.time, IntegerTime.as_decimal(int_tf))
            ode_sol, context_tf = self.ode_solve(
                context_t0, x0=context_t0.state, t_span=t_span
            )
            zc_events = determine_triggered_guards(search_data.guards, context_tf)

            return True, context_tf, ode_sol, zc_events, int_tf

        args = (cdata, ode_sol, zc_events, context_tf)
        triggered, context, ode_sol, zc_events, int_tf = self.cond(
            zc_events.has_triggered, _localize_zero_crossings, _no_events_fun, args
        )

        # Store the results
        results_data = self.save_results(results_data, context, ode_sol)

        # Handle any triggered zero-crossing events
        context = self.system.handle_zero_crossings(zc_events, context)

        return cdata._replace(
            triggered=triggered,
            terminate_early=zc_events.has_active_terminal,
            context=context,
            tf=int_tf,
            results_data=results_data,
        )

    def _unguarded_integrate(
        self,
        cdata: ContinuousIntervalData,
    ) -> ContinuousIntervalData:
        """Advance the simulation to the next discrete update.

        This is a special case of `_guarded_integrate` where there are no zero-crossing
        events in the system.  In this case `_unguarded_integrate` and
        `_guarded_integrate` are logically equivalent, but the unguarded version is
        still slightly more efficient.
        """

        int_tf = cdata.tf
        context = cdata.context
        results_data = cdata.results_data

        # Integrate the ODE to the final time of the major_step
        t_span = (context.time, IntegerTime.as_decimal(int_tf))
        ode_sol, context = self.ode_solve(context, x0=context.state, t_span=t_span)

        # Store the ODE solution
        results_data = self.save_results(results_data, context, ode_sol)

        return cdata._replace(
            terminate_early=False,
            triggered=False,
            context=context,
            results_data=results_data,
        )

    def _stateless_integrate(
        self, cdata: ContinuousIntervalData
    ) -> ContinuousIntervalData:
        """Advance continuous time in the case where there are no continuous states.

        The name "stateless_integrate" is a bit of a misnomer, as there is no actual
        integration happening here, but it the alternative to (un)guarded_integrate,
        which does call out to and ODE solver.

        This method just advances time to the end of the interval, checking to see
        if any zero-crossing events are triggered as a result of the time advance.

        Args:
            cdata (ContinuousIntervalData): The current state of the system and the
                requested end time of the interval.

        Returns:
            ContinuousIntervalData: The updated data after the continuous-time
                interval, including handling any triggered zero-crossing events.
        """

        # Unpack inputs
        int_tf = cdata.tf
        context = cdata.context
        results_data = cdata.results_data

        zc_events = self.system.determine_active_guards(context)

        # Skip the ODE solver for systems without continuous state.  We still
        # have to check for triggered events here in case there are any
        # transitions triggered by time that need to be handled before the
        # periodic discrete update at the top of the next major step
        triggered = False
        ode_sol = None
        zc_events = guard_interval_start(zc_events, context)

        # Store the solution
        results_data = self.save_results(results_data, context, ode_sol)

        # Advance time to the end of the interval
        context = context.with_time(IntegerTime.as_decimal(int_tf))

        # Record guard values after the discrete update and check if anything
        # triggered as a result of advancing time
        zc_events = guard_interval_end(zc_events, context)
        zc_events = determine_triggered_guards(zc_events, context)

        # Handle any triggered zero-crossing events
        context = self.system.handle_zero_crossings(zc_events, context)

        return cdata._replace(
            triggered=triggered,
            context=context,
            terminate_early=zc_events.has_active_terminal,
            tf=int_tf,
            results_data=results_data,
        )

    def _handle_discrete_update(
        self, context: ContextBase, timed_events: EventCollection
    ) -> tuple[ContextBase, bool]:
        """Handle discrete updates triggered by time.

        This method is called at the beginning of each major step to handle any
        discrete updates that are triggered by time.  This includes both discrete
        updates that are triggered by time and any zero-crossing events that are
        triggered by the discrete update.

        This will also work when there are no zero-crossing events: the zero-crossing
        collection will be empty and only the periodic discrete update will happen.

        Args:
            context (ContextBase): The current state of the system.
            timed_events (EventCollection):
                The collection of timed events, with the active events marked.

        Returns:
            ContextBase: The updated state of the system.
            bool: Whether the simulation should terminate early as a result of a
                triggered terminal condition.
        """
        system = self.system

        # Get the collection of zero-crossing events that _might_ be activated
        # given the current state of the system.  For example, some events may
        # be de-activated as a result of the current state of a state machine.
        zc_events = system.determine_active_guards(context)

        # Record guard values at the start of the interval
        zc_events = guard_interval_start(zc_events, context)

        # Handle any active periodic discrete updates
        context = system.handle_discrete_update(timed_events, context)

        # Record guard values after the discrete update
        zc_events = guard_interval_end(zc_events, context)

        # Check if guards have triggered as a result of these updates
        zc_events = determine_triggered_guards(zc_events, context)
        terminate_early = zc_events.has_active_terminal

        # Handle any zero-crossing events that were triggered
        context = system.handle_zero_crossings(zc_events, context)

        return context, terminate_early

    def _advance_continuous_time(
        self,
        cdata: ContinuousIntervalData,
    ) -> ContinuousIntervalData:
        """Advance continuous time to the end of the major step.

        This method will normally call `_integrate` to advance
        continuous time using the ODE solver and handle any triggered zero-crossing
        events. However, if a zero-crossing was triggered as part of the discrete
        update, this method will skip the continuous update and return immediately.

        Args:
            cdata (ContinuousIntervalData):
                Struct holding information needed to advance through the continuous
                time interval.  Includes current context, current integer time stamp,
                requested end time, and step termination info.

        Returns:
            ContinuousIntervalData: The updated data after the continuous-time interval
        """

        if self.has_terminal_events:
            return self.cond(
                cdata.terminate_early,
                lambda cdata: cdata,  # Terminal event triggered - return immediately
                self._integrate,  # Advance continuous time normally
                (cdata,),
            )

        return self._integrate(cdata)

    # This method is marked private because it will be wrapped with a custom autodiff
    # rule to get the correct derivatives with respect to the end time of the
    # simulation interval using `_override_advance_to_vjp`.  This also copies the
    # docstring to the overridden function. Normally the wrapped attribute `advance_to`
    # is what should be called by users.
    def _advance_to(self, boundary_time: float, context: ContextBase) -> SimulatorState:
        """Core control flow logic for running a simulation.

        This is the main loop for advancing the simulation.  It is called by `simulate`
        or can be called directly if more fine-grained control is needed. This method
        essentially loops over "major steps" until the boundary time is reached. See
        the documentation for `simulate` for details on the order of operations in a
        major step.

        Args:
            boundary_time (float): The time to advance to.
            context (ContextBase): The current state of the system.

        Returns:
            SimulatorState:
                A named tuple containing the final state of the simulation, including
                the final context, a collection of pending timed events, and a flag
                indicating the reason that the most recent major step ended.

        Notes:
            API will change slightly as a result of WC-87, which will break out the
            initialization from the main loop so that `advance_to` can be called
            repeatedly.  See:
            https://collimator.atlassian.net/browse/WC-87
        """

        system = self.system
        sim_state = self.initialize(context)
        end_reason = sim_state.step_end_reason
        context = sim_state.context
        timed_events = sim_state.timed_events
        int_boundary_time = IntegerTime.from_decimal(boundary_time)

        # We will be limiting each step by the max_major_step_length.  However, if this
        # is infinite we should just use the end time of the simulation to avoid
        # integer overflow.  This could be problematic if the end time of the
        # simulation is close to the maximum representable integer time, but we can come
        # back to that if it's an issue.
        int_max_step_length = IntegerTime.from_decimal(
            cnp.minimum(self.max_major_step_length, boundary_time)
        )

        # Only activate timed events if the major step ended on a time trigger
        timed_events = activate_timed_events(timed_events, end_reason)

        # Called on the "True" branch of the conditional
        def _major_step(sim_state: SimulatorState) -> SimulatorState:
            end_reason = sim_state.step_end_reason
            context = sim_state.context
            timed_events = sim_state.timed_events
            int_time = sim_state.int_time

            if not self.enable_tracing:
                logger.debug("Starting a simulation step at t=%s", context.time)
                logger.debug("   merged_events: %s", timed_events)

            # Handle any discrete updates that are triggered by time along with
            # any zero-crossing events that are triggered by the discrete update.
            context, terminate_early = self._handle_discrete_update(
                context, timed_events
            )
            logger.debug("Terminate early after discrete update: %s", terminate_early)

            # How far can we go before we have to handle timed events?
            # The time returned here will be the integer time representation.
            time_of_next_timed_event, timed_events = _next_update_time(
                system.periodic_events, int_time
            )
            if not self.enable_tracing:
                logger.debug(
                    "Next timed event at t=%s",
                    IntegerTime.as_decimal(time_of_next_timed_event),
                )
                timed_events.pprint(logger.debug)

            # Determine whether the events include a timed update
            update_time = IntegerTime.max_int_time

            if timed_events.num_events > 0:
                update_time = time_of_next_timed_event

            # Limit the major step end time to the simulation end time, major step limit,
            # or next periodic update time.
            # This is the mechanism used to advance time for systems that have
            # no states and no periodic events.
            # Discrete systems] when there are discrete periodic events, we use those
            # to determine each major step end time.
            # Feedthrough system] when there are just feedthrough blocks (no states or
            # events), use max_major_step_length to determine each major step end time.
            int_tf_limit = int_time + int_max_step_length
            int_tf = cnp.min(
                cnp.array(
                    [
                        int_boundary_time,
                        int_tf_limit,
                        update_time,
                    ]
                )
            )
            if not self.enable_tracing:
                logger.debug(
                    "Expecting to integrate to t=%s",
                    IntegerTime.as_decimal(int_tf),
                )

            # Normally we will advance continuous time to the end of the major step
            # here. However, if a terminal event was triggered as part of the discrete
            # update, we should respect that and skip the continuous update.
            #
            # Construct the container used to hold various data related to advancing
            # continuous time.  This is passed to ODE solvers, zero-crossing
            # localization, and related functions.
            cdata = ContinuousIntervalData(
                context=context,
                terminate_early=terminate_early,
                triggered=False,
                t0=int_time,
                tf=int_tf,
                results_data=sim_state.results_data,
            )
            cdata = self._advance_continuous_time(cdata)

            # Unpack the results of the continuous time advance
            context = cdata.context
            terminate_early = cdata.terminate_early
            triggered = cdata.triggered
            int_tf = cdata.tf
            results_data = cdata.results_data

            # Determine the reason why the major step ended.  Did a zero-crossing
            # trigger, did a timed event trigger, neither, or both?
            # terminate_early = terminate_early | zc_events.has_active_terminal
            logger.debug("Terminate early after major step: %s", terminate_early)
            end_reason = _determine_step_end_reason(
                triggered, terminate_early, int_tf, update_time
            )
            logger.debug("Major step end reason: %s", end_reason)

            # Conditionally activate timed events depending on whether the major step
            # ended as a result of a time trigger or zero-crossing event.
            timed_events = activate_timed_events(timed_events, end_reason)

            if self.major_step_callback:
                io_callback(self.major_step_callback, (), context.time)

            return SimulatorState(
                step_end_reason=end_reason,
                context=context,
                timed_events=timed_events,
                int_time=int_tf,
                results_data=results_data,
            )

        def _cond_fun(sim_state: SimulatorState):
            return (sim_state.int_time < int_boundary_time) & (
                sim_state.step_end_reason != StepEndReason.TerminalEventTriggered
            )

        # Initialize the "carry" values for the main loop.
        sim_state = SimulatorState(
            context=context,
            timed_events=timed_events,
            step_end_reason=end_reason,
            int_time=sim_state.int_time,
            results_data=sim_state.results_data,
        )

        logger.debug(
            "Running simulation from t=%s to t=%s", context.time, boundary_time
        )
        try:
            # Main loop call
            sim_state = self.while_loop(_cond_fun, _major_step, sim_state)
            logger.debug("Simulation complete at t=%s", sim_state.context.time)
        except KeyboardInterrupt:
            # TODO: flag simulation as interrupted somewhere in sim_state
            logger.info("Simulation interrupted at t=%s", sim_state.context.time)

        # At the end of the simulation we need to handle any pending discrete updates
        # and store the solution one last time.
        # FIXME (WC-87): The returned simulator state can't be used with advance_to again,
        # since the discrete updates have already been performed. Should be broken out
        # into a `finalize` method as part of WC-87.

        # update discrete state to x+ at the simulation end_time
        if self.save_time_series:
            logger.debug("Finalizing solution...")
            # 1] do discrete update (will skip if the simulation was terminated early)
            context, _terminate_early = self._handle_discrete_update(
                sim_state.context, sim_state.timed_events
            )
            # 2] do update solution
            results_data = self.save_results(sim_state.results_data, context, None)
            sim_state = sim_state._replace(
                context=context,
                results_data=results_data,
            )
            logger.debug("Done finalizing solution")

        return sim_state


def _bounded_while_loop(
    cond_fun: Callable,
    body_fun: Callable,
    val: Any,
    max_steps: int,
) -> Any:
    """Run a while loop with a bounded number of steps.

    This is a workaround for the fact that JAX's `lax.while_loop` does not support
    reverse-mode autodiff.  The `max_steps` bound can usually be determined
    automatically during calls to `simulate` - see notes on `max_major_steps` in
    `SimulatorOptions` and `estimate_max_major_steps`.
    """

    def _loop_fun(_i, val):
        return lax.cond(
            cond_fun(val),
            body_fun,
            lambda val: val,
            val,
        )

    return lax.fori_loop(0, max_steps, _loop_fun, val)


def _check_backend(system: SystemBase, options: SimulatorOptions) -> tuple[str, bool]:
    """Check if JAX tracing can be used to simulate this system."""

    math_backend = options.math_backend or "auto"
    if math_backend == "auto":
        math_backend = backend.active_backend

    if math_backend != "jax":
        enable_tracing = False

    # If the system uses `io_callback` to execute arbitrary Python code (usually
    # in an untraced PythonScript block), we have to fall back on SciPy ODE solvers.
    elif system.has_ode_side_effects:
        logger.warning(
            "System uses arbitrary Python code in the right-hand side of an ODE. "
            "This is not currently supported with JAX JIT compilation. "
            "Falling back to NumPy backend. The simulation may be slower. Consider "
            'rewriting "agnostic" time mode PythonScript blocks in JAX to improve '
            "performance."
        )
        enable_tracing = False
        math_backend = "numpy"

    else:
        # Otherwise return whatever `options` requested
        enable_tracing = options.enable_tracing

    return math_backend, enable_tracing


def _determine_step_end_reason(
    guard_triggered: bool,
    terminate_early: bool,
    tf: int,
    update_time: int,
) -> StepEndReason:
    """Determine the reason why the major step ended."""
    logger.debug("[_determine_step_end_reason]: tf=%s, update_time=%s", tf, update_time)
    logger.debug("[_determine_step_end_reason]: guard_triggered=%s", guard_triggered)

    # If the integration terminated due to a triggered event, determine whether
    # there are any other events that should be triggered at the same time.
    guard_reason = cnp.where(
        tf == update_time,
        StepEndReason.BothTriggered,
        StepEndReason.GuardTriggered,
    )

    # No guard triggered; handle integration as usual.
    no_guard_reason = cnp.where(
        tf == update_time,
        StepEndReason.TimeTriggered,
        StepEndReason.NothingTriggered,
    )

    reason = cnp.where(guard_triggered, guard_reason, no_guard_reason)

    # No matter why the integration terminated, if a "terminal" event is also
    # active, that will be the overriding reason for the termination.
    return cnp.where(terminate_early, StepEndReason.TerminalEventTriggered, reason)


def _next_sample_time(current_time: int, event_data: PeriodicEventData) -> int:
    """Determine when the specified periodic event happens next.

    This is a helper function for `_next_update_time` for a specific event.
    """

    period, offset = event_data.period_int, event_data.offset_int

    # If we shift the current time by the offset, what would the index of the
    # next periodic sample time be?  This tells us how many samples from the
    # offset we are in either direction.  For example, if offset=dt and t=0,
    # the next "k" value will be -1.
    next_k = (current_time - offset) // period

    # What would the next periodic sample time be?  If the period is infinite,
    # the next sample time is also infinite.  This value is shifted back to the
    # original time frame by adding the offset.  If the sample is more than one
    # period away from the offset, this will be negative.
    next_t = cnp.where(
        cnp.isfinite(event_data.period),
        offset + next_k * period,
        period,
    )

    # If we are in between samples, next_t should be strictly greater than
    # the current time and that should be used as the target major step end time.
    # However, if we are at t = offset + k * period for some k, then the
    # calculation above will give us next_k = k and therefore next_t = t.
    # In this case we should bump to the next time in the series.
    next_sequence_time = cnp.where(
        next_t > current_time,
        next_t,
        offset + (next_k + 1) * period,
    )

    return cnp.where(
        current_time < offset,
        offset,
        next_sequence_time,
    )


def _next_update_time(periodic_events: EventCollection, current_time: int) -> int:
    """Compute next update time over all events in the periodic_events collection.

    This returns a tuple of the minimum next sample time along with a pytree with
    the same structure as `periodic_events` indicating which events are active at
    the next sample time.
    """
    periodic_events = periodic_events.mark_all_inactive()

    # 0. If no events, return an infinite time and empty event collection
    if not periodic_events.has_events:
        return IntegerTime.max_int_time, periodic_events

    # 1. Compute the next sample time for each event
    def _replace_sample_time(event_data):
        return dataclasses.replace(
            event_data,
            next_sample_time=_next_sample_time(current_time, event_data),
        )

    timed_events = jax.tree_map(
        _replace_sample_time,
        periodic_events,
        is_leaf=is_event_data,
    )

    def _get_next_sample_time(event_data: PeriodicEventData) -> int:
        return event_data.next_sample_time

    # 2. Find the minimum next sample time across all events
    min_time = jax.tree_util.tree_reduce(
        cnp.minimum,
        jax.tree_map(
            _get_next_sample_time,
            timed_events,
            is_leaf=is_event_data,
        ),
    )

    # 3. Find the events corresponding to the minimum time by updating the event data `active` field
    def _replace_active(event_data: PeriodicEventData):
        return dataclasses.replace(
            event_data,
            active=(event_data.next_sample_time == min_time),
        )

    active_events = jax.tree_map(
        _replace_active,
        timed_events,
        is_leaf=is_event_data,
    )
    return min_time, active_events


def activate_timed_events(
    timed_events: EventCollection, end_reason: StepEndReason
) -> EventCollection:
    """Conditionally activate timed events.

    Only activate timed events if the major step ended on a time trigger and
    the event was already marked active (by the timing calculation). This will
    deactivate timed events if they were pre-empted by a zero-crossing.
    """

    deactivate = (end_reason != StepEndReason.TimeTriggered) & (
        end_reason != StepEndReason.BothTriggered
    )

    def activation_fn(event_data: PeriodicEventData):
        return event_data.active & ~deactivate

    return timed_events.activate(activation_fn)


def _is_zc_event(x):
    return isinstance(x, ZeroCrossingEvent)


def _record_guard_values(
    events: EventCollection, context: ContextBase, key: str
) -> EventCollection:
    """Store the current values of guard functions in the event data.

    The "key" can either be `"w0"` or `"w1"` to indicate whether the recorded
    values correspond to the start or end of the interval.
    """

    # Set the `w0`/`w1` field of event_data by evaluating the guard functions
    def _update(event: ZeroCrossingEvent):
        event.event_data = dataclasses.replace(
            event.event_data,
            **{key: event.eval_guard(context)},
        )
        return event

    return jax.tree_map(_update, events, is_leaf=_is_zc_event)


# Convenient partial functions for the two valid values of `key`.
guard_interval_start = partial(_record_guard_values, key="w0")
guard_interval_end = partial(_record_guard_values, key="w1")


def determine_triggered_guards(
    events: EventCollection, context: ContextBase
) -> EventCollection:
    """Determine which zero-crossing events are triggered.

    This is done by evaluating the guard functions at the end of the interval
    and comparing the sign of the values to the sign of the values at the
    beginning of the interval, using the "direction" rule for each individual
    event.

    The returned collection has the same pytree structure as the input, but
    the `active` field of the event data will be set to `True` for any events
    that triggered.
    """
    events = guard_interval_end(events, context)

    def _update(event: ZeroCrossingEvent):
        event.event_data = dataclasses.replace(
            event.event_data,
            triggered=event.should_trigger(),
        )
        return event

    return jax.tree_map(_update, events, is_leaf=_is_zc_event)


def _bisection_step_fun(step_interpolant, i, carry: GuardIsolationData):
    """Perform one step of bisection.

    Appropriately return a new zero crossing localization time interval.

    Bisection is employed as follows:
        1] split t0->tf into t0->t_mid0->tf
        2] set guard interval end at t_mid
        3] check if any guards triggered
        4] if so, set t0=t0, and tf=t_mid0,
            which, when we return to step 1, we'll split t0->t_mid to t0->t_mid1->t_mid0,
            and check for triggers in t0->t_mid1
        5] else, set t0=t_mid0 and tf=tf,
            which, when we return to step 1, we'll split t_mid0->tf to t_mid0->t_mid1->tf,
            and check for triggers in t_mid0->t_mid1
    The process repeats until we reach a termination condition. Presently, the termination
    condition is just a fixed number of iterations.
    """

    # bisection algo part 1: find mid point (integer time stamp)
    int_time_mid = (
        carry.zc_before_time + (carry.zc_after_time - carry.zc_before_time) // 2
    )
    time_mid = IntegerTime.as_decimal(int_time_mid)

    # check for triggers in interval
    context_mid = carry.context.with_time(time_mid)
    states_mid = step_interpolant.evaluate(time_mid)
    context_mid = context_mid.with_continuous_state(states_mid)
    guards_mid = determine_triggered_guards(carry.guards, context_mid)

    # bisection algo part 2: decide whether next step will search
    # the first half, or the second half of the current interval.
    zc_before_time = cnp.where(
        guards_mid.has_triggered, carry.zc_before_time, int_time_mid
    )
    zc_after_time = cnp.where(
        guards_mid.has_triggered, int_time_mid, carry.zc_after_time
    )

    return GuardIsolationData(
        zc_before_time,
        zc_after_time,
        carry.guards,
        carry.context,
    )
