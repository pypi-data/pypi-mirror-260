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

"""Ordinary differential equation (ODE) solvers for continuous-time simulation.

This module provides a common interface for ODE solvers used to advance continuous
time by the hybrid simulator.  The module has interfaces to diffrax, JAX, and SciPy
ODE solvers.  A callable ODE solver can be created by calling the `ODESolver` function,
which will return an instance of a class implementing the `ODESolverBase` interface.

Additionally, the module provides an `odeint` function with a similar interface to
SciPy's `solve_ivp` function, which can be used as a simplified interface for
simulating purely continuous-time systems (without any events).
"""

from __future__ import annotations

import dataclasses
from functools import partial
from typing import TYPE_CHECKING, ClassVar, Tuple

import diffrax
import diffrax._solution as diffrax_sol
import jax
import jax.numpy as jnp
import numpy as np
from diffrax import ODETerm, PIDController, SaveAt, SubSaveAt, diffeqsolve
from jax import tree_util
from jax.experimental.ode import odeint as jax_odeint

from .rk4 import odeint as rk4_odeint
from ..ode_solver import ODESolverBase, ODESolution, ODESolverOptions

if TYPE_CHECKING:
    from ..typing import Array
    from ...framework import ContextBase, SystemBase

__all__ = ["ODESolver"]


def _raise_diffrax_error_fun(sol, t_err_interval):
    if not diffrax_sol.is_successful(sol.result):
        if sol.result == diffrax_sol.RESULTS.max_steps_reached:
            # catch and change name of 'max_steps' to 'max_minor_step_per_major_step'
            raise RuntimeError(
                "The differential equations solver is failing to converge on a solution."
                f"The time at which this occurred is between {t_err_interval[0]} and {t_err_interval[1]}"
            )
        else:
            raise RuntimeError(sol.result)


@jax.jit
def _raise_diffrax_error(sol, t_err_interval):
    jax.debug.callback(_raise_diffrax_error_fun, sol, t_err_interval)


class DiffraxSolver(ODESolverBase):
    supported_methods = {
        "default": diffrax.Tsit5,
        "non-stiff": diffrax.Tsit5,
        "stiff": diffrax.Kvaerno5,
        "Euler": diffrax.Euler,
        "Tsit5": diffrax.Tsit5,
        "Heun": diffrax.Heun,
        "Midpoint": diffrax.Midpoint,
        "Ralston": diffrax.Ralston,
        "Bosh3": diffrax.Bosh3,
        "Dopri5": diffrax.Dopri5,
        "Dopri8": diffrax.Dopri8,
        "ImplicitEuler": diffrax.ImplicitEuler,
        "Kvaerno3": diffrax.Kvaerno3,
        "Kvaerno4": diffrax.Kvaerno4,
        "Kvaerno5": diffrax.Kvaerno5,
    }

    DEFAULT_MAX_STEPS: ClassVar[int] = 16**3

    def _finalize(self):
        """Create a wrapper for diffrax.diffeqsolve for ODE solving.

        This is a preferred method for ODE solving, but it requires that the system
        time derivatives are traceable by JAX.
        """
        term = ODETerm(partial(self.ode_rhs, self.system))

        stepsize_controller = PIDController(
            rtol=self.rtol,
            atol=self.atol,
            dtmin=self.min_step_size,
            dtmax=self.max_step_size,
        )

        try:
            solver = self.supported_methods[self.method]()
        except KeyError:
            raise ValueError(
                f"Invalid method '{self.method}' for JAX ODE solver. Must be one of "
                f"{list(self.supported_methods.keys())}"
            )

        def _ode_solve(
            context: ContextBase, t_span: Tuple[float, float], t_eval: Array = None
        ) -> Tuple[ODESolution, ContextBase]:
            xc0 = context.continuous_state

            if t_eval is None:
                if self.save_steps:
                    # Save both the final state and all the intermediate solver steps
                    saveat = SaveAt(
                        subs=[
                            SubSaveAt(t0=False, t1=True),
                            SubSaveAt(t0=True, steps=True),
                        ],
                        dense=self.return_step_interpolant,
                    )
                else:
                    # Only save the final state
                    saveat = SaveAt(
                        t0=False, t1=True, dense=self.return_step_interpolant
                    )
            else:
                # Save both the final state and the requested time points
                saveat = SaveAt(
                    subs=[
                        SubSaveAt(t0=False, t1=True),
                        SubSaveAt(t0=False, ts=t_eval),
                    ],
                    dense=self.return_step_interpolant,
                )

            sol = diffeqsolve(
                term,
                solver,
                t_span[0],
                t_span[1],
                None,
                xc0,
                context,
                stepsize_controller=stepsize_controller,
                saveat=saveat,
                max_steps=self.max_steps,
                throw=False,
            )

            if self.save_steps:
                num_accepted_steps = sol.stats["num_accepted_steps"]
                xf = sol.ys[0]
                xs = sol.ys[1]
                tf = sol.ts[0]
                # The solution handling will record the final value separately,
                # so set the final time to infinity to avoid duplicate entries.
                # This will get trimmed out of the solution later
                # (see ResultsData.trim)
                ts = sol.ts[1].at[num_accepted_steps].set(sol.ts[1][-1])
            else:
                xf = sol.ys
                xs = None
                tf = sol.ts
                ts = None

            # catch diffrax error
            _raise_diffrax_error(sol, (tf, t_span[1]))

            if self.return_step_interpolant:
                step_interpolant = sol.interpolation
            else:
                step_interpolant = None

            n_steps = int(self.max_steps)
            sol_out = ODESolution(
                (xf, xs), (tf, ts), n_steps, sol.stats, step_interpolant
            )
            return sol_out, context

        self._solve = jax.jit(_ode_solve)


class JaxSolver(ODESolverBase):
    # FIXME: This is currently broken with autodiff - throws an error
    # ValueError: dtype=dtype([('float0', 'V')]) is not a valid dtype for JAX type promotion.
    # from somewhere jax.experimental.ode._odeint_rev
    supported_methods = {
        # TODO: define default, stiff and non-stiff methods
        "Dopri5": jax_odeint,
        "RK4": rk4_odeint,
    }

    def _finalize(self):
        """Create a wrapper for jax.experimental.odeint for ODE solving.

        This is a preferred method for ODE solving, but it requires that the system
        time derivatives are traceable by JAX.
        """
        # Extract flattened symbolic variables from the context along with information
        # to recreate the tree structure from the solution data.

        options = {
            "rtol": self.rtol,
            "atol": self.atol,
            "hmax": self.max_step_size or np.inf,
        }

        try:
            odeint = self.supported_methods[self.method]
        except KeyError:
            raise ValueError(
                f"Invalid method '{self.method}' for JAX ODE solver. Must be one of "
                f"{list(self.supported_methods.keys())}"
            )

        def func(y, t, context):
            return self.ode_rhs(self.system, t, y, context)

        def _ode_solve(
            context: ContextBase, t_span: Tuple[float, float], t_eval: Array = None
        ) -> Tuple[ODESolution, ContextBase]:
            xc0 = context.continuous_state

            if t_eval is None:
                if self.save_steps:
                    t_eval = jnp.linspace(t_span[0], t_span[1], self.max_steps + 1)
                else:
                    # Only save the final state
                    t_eval = jnp.asarray(t_span)
            else:
                t_eval = jnp.asarray(t_eval)

            ys = odeint(
                func,
                xc0,
                t_eval,
                context,
                **options,
            )

            # Extract the final time/state
            num_accepted_steps = len(t_eval) - 1
            xf = tree_util.tree_map(lambda x: x[num_accepted_steps], ys)
            tf = t_eval[num_accepted_steps]
            if self.save_steps:
                xs = ys
                ts = t_eval
            else:
                xs = None
                ts = None

            stats = {"num_accepted_steps": num_accepted_steps}

            n_steps = self.max_steps
            sol_out = ODESolution((xf, xs), (tf, ts), n_steps, stats, None)
            return sol_out, context

        self._solve = jax.jit(_ode_solve)


def ODESolver(
    system: SystemBase,
    options: ODESolverOptions = None,
) -> ODESolverBase:
    """Create an ODE solver used to advance continuous time in hybrid simulation.

    Args:
        system (SystemBase):
            The system to be simulated.
        options (ODESolverOptions, optional):
            Options for the ODE solver.  Defaults to None.
        enable_tracing (bool, optional):
            Whether to enable tracing of time derivatives for JAX solvers.  Defaults
            to True.

    Returns:
        ODESolverBase:
            An instance of a class implementing the `ODESolverBase` interface.
            The specific class will depend on the system and options. This object
            is a callable with signature:
            ```python
            def __call__(
                context: ContextBase, t_span: Tuple[float, float], t_eval: Array = None
            ): -> (sol: ODESolution, context: ContextBase)
            ```

    Notes:
        For simulating pure-continuous systems, the `odeint` function is a more
        convenient interface.
    """

    if options is None:
        options = ODESolverOptions()
    options = dataclasses.asdict(options)

    if options["method"] in JaxSolver.supported_methods:
        return JaxSolver(system, **options)
    return DiffraxSolver(system, **options)
