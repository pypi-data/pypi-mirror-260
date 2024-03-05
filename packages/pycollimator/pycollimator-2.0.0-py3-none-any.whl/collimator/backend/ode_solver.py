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

from __future__ import annotations
import dataclasses
from typing import TYPE_CHECKING, ClassVar, NamedTuple

if TYPE_CHECKING:
    from .typing import Array
    from ..framework import SystemBase, ContextBase
    from ..framework.state import State, StateComponent


__all__ = [
    "ODESolverOptions",
    "ODESolution",
    "ODESolverBase",
]


@dataclasses.dataclass
class ODESolverOptions:
    """Options for the ODE solver.

    See documentation for `simulate` for details on these options.
    """

    rtol: float = 1e-3
    atol: float = 1e-6
    min_step_size: float = None
    max_step_size: float = None
    max_steps: float = None
    method: str = "default"  # Tsit5 (diffrax) or Dopri5 (jax/scipy)
    save_steps: bool = True


# Internal data structure to mimic diffrax.Solution
class ODESolution(NamedTuple):
    ys: object
    ts: object
    # Number of solver steps (used for signal reconstruction).  For JAX solvers this
    # must be static (the `max_steps` bound), but for SciPy it can be variable.
    n_steps: int
    stats: object = None
    step_interpolant: object = None


@dataclasses.dataclass
class ODESolverBase:
    """Common interface for defining ODE solvers.

    The ODE solving function has signature:
    ```
    def __call__(
        context: ContextBase, t_span: Tuple[float, float], t_eval: Array = None
    ): -> (sol: ODESolution, context: ContextBase)
    ```
    and can be used for instance to advance continuous time during hybrid
    simulation.
    """

    system: SystemBase
    rtol: float = 1e-6
    atol: float = 1e-8
    max_steps: int = None
    max_step_size: float = None
    min_step_size: float = None
    method: str = "default"
    save_steps: bool = True

    # this is a temporary solution for avoiding the compile time penalty associated
    # with returning the interpolant from diffrax for models that do not have ZCs.
    return_step_interpolant: bool = False

    DEFAULT_MAX_STEPS: ClassVar[int] = 100

    @staticmethod
    def ode_rhs(
        system: SystemBase,
        t: float,
        y: StateComponent,
        context: ContextBase,
    ) -> StateComponent:
        """Evaluate the time derivatives of the system at a given time and state."""
        context = context.with_time(t)
        # Update the continuous state, holding discrete state fixed.
        context = context.with_continuous_state(y)
        xcdot = system.eval_time_derivatives(context)
        return xcdot

    def _finalize(self):
        """Hook for any class-specific finalization after __post_init__."""
        pass

    def __post_init__(self):
        if self.max_steps is None:
            self.max_steps = self.DEFAULT_MAX_STEPS
        self.return_step_interpolant = self.system.zero_crossing_events.has_events
        self._finalize()

    def _solve(
        self, context: ContextBase, t_span: tuple[float, float], t_eval: Array = None
    ) -> tuple[ODESolution, ContextBase]:
        raise NotImplementedError(
            "ODESolver._solve must be implemented or created by _finalize"
        )

    def __call__(
        self,
        context: ContextBase,
        t_span: tuple[float, float],
        t_eval: Array = None,
        x0: State = None,
    ) -> tuple[ODESolution, ContextBase]:
        """Advance continuous time by integrating the ODE component of the system.

        This will not advance discrete time or handle any events.  It is intended
        to be used either for pure-continuous systems or for advancing continuous
        time as part of the hybrid simulation loop.

        Args:
            context (ContextBase):
                The context to use for integration.  This will be updated with the
                final time and state after integration.
            t_span (tuple[float, float]):
                The start and end times of the integration interval.
            t_eval (Array, optional):
                The times at which to save the state.  See specific implementations
                for how this argument is used. Default is None
            x0 (State, optional):
                The initial state to use for integration.  Default is None (use the
                current state in the context).

        Returns:
            tuple[ODESolution, ContextBase]:
                The solution of the ODE integration and the updated context. The ODE
                solution has the same pytree structure as the context's continuous
                state, expanded along the leading axis to include all intermediate
                time steps taken by the solver.
        """

        t0, tf = t_span
        context = context.with_time(t0)
        if x0 is not None:
            context = context.with_state(x0)

        # this is needed in the case of system without continuous states,
        # but with zero-crossing events, i.e. events that may only be based
        # on some function which depends only on time.
        if context.num_continuous_states == 0:
            return None, context.with_time(tf)

        ode_sol, context = self._solve(context, t_span, t_eval=t_eval)

        # The first entry of the ode_sol is the final state (second is all solver steps)
        xc = ode_sol.ys[0]

        # logger.debug(f"Integrated from t={context.time} to t={tf}: result={xc}")
        context = context.with_continuous_state(xc)
        context = context.with_time(tf)
        return ode_sol, context
