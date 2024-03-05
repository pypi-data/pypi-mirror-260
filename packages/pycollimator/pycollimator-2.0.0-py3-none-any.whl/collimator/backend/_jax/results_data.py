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
from typing import TYPE_CHECKING
import dataclasses

import numpy as np
import jax
from jax import lax
import jax.numpy as jnp

from ..results_data import AbstractResultsData

if TYPE_CHECKING:
    from ...framework import SystemCallback, ContextBase
    from ..typing import Array
    from ..ode_solver import ODESolution


__all__ = ["JaxResultsData"]


def _make_empty_solution(
    context: ContextBase,
    recorded_signals: dict[str, SystemCallback],
    max_minor_steps: int = 16**3,
    max_major_steps: int = 100,
) -> JaxResultsData:
    """Create an empty "buffer" solution data object with the correct shape.
    For each source in "recorded_signals", determine what the signal data type is
    and create an empty vector that can hold enough data to max out the simulation
    buffer.
    """

    def _expand_template(source: SystemCallback):
        # Determine the data type of the signal (shape and dtype)
        x = source.eval(context)
        if jnp.isscalar(x):
            x = jnp.asarray(x)
        # Create a buffer that can hold the maximum number of (major, minor) steps
        return jnp.zeros(
            (max_major_steps, max_minor_steps + 1, *x.shape), dtype=x.dtype
        )

    signals = {
        key: _expand_template(source) for key, source in recorded_signals.items()
    }
    # The time vector is used to determine the number of steps taken by the ODE solver
    # since diffrax will return inf for unused buffer entries. Then we can use isfinite
    # to trim the unused buffer space.  For this reason, initialize to inf rather
    # than zero.
    times = jnp.full((max_major_steps, max_minor_steps + 1), jnp.inf)
    n_minor_steps = jnp.zeros((max_major_steps,), dtype=jnp.int32)
    return JaxResultsData(
        source_dict=recorded_signals,
        outputs=signals,
        time=times,
        n_minor_steps=n_minor_steps,
        max_minor_steps=max_minor_steps,
    )


def _trim(solution: JaxResultsData) -> tuple[Array, dict[str, Array]]:
    """Remove unused entries from the buffer and return flattened arrays.

    See `JaxResultsData.finalize` for more details.
    """
    n_major_steps = solution.n_major_steps
    outputs = {key: y[:n_major_steps] for key, y in solution.outputs.items()}
    time = solution.time[:n_major_steps]

    time = jnp.concatenate(time, axis=0)

    # Adaptive ODE solvers (like diffrax) should return inf for unused buffer entries.
    # Then we can use isfinite to trim the unused buffer space.
    valid_idx = jnp.isfinite(time)
    time = time[valid_idx]

    for key, y in outputs.items():
        y_trim = jnp.concatenate(y, axis=0)
        y_trim = y_trim[valid_idx]
        outputs[key] = y_trim

    return jax.tree_map(np.array, (time, outputs))


# Inherits docstring from `AbstractResultsData`
@dataclasses.dataclass
class JaxResultsData(AbstractResultsData):
    n_minor_steps: Array = (
        None  # Number of steps taken by the ODE solver in each interval
    )
    n_major_steps: int = 0  # Number of time intervals (major steps) in the solution
    max_minor_steps: int = None  # Maximum number of ODE solver steps per major step

    @staticmethod
    def initialize(
        context: ContextBase,
        recorded_signals: dict[str, SystemCallback],
        max_major_steps: int = None,
        max_minor_steps_per_major_step: int = None,
    ) -> JaxResultsData:
        return _make_empty_solution(
            context,
            recorded_signals,
            max_minor_steps_per_major_step,
            max_major_steps,
        )

    def update(
        self,
        context: ContextBase,
        ode_sol: ODESolution,
    ) -> JaxResultsData:
        """Update the simulation solution with the results of a simulation step.

        This stores the results of a single major step in a modified solution buffer
        (so that it acts as a pure function for the purposes of JAX tracing).
        It will loop over all "minor" steps in the ODE and reconstruct the signals
        at each step, storing the results in the solution buffer.  If a pure discrete
        system is being simulated, then only a single data point will be saved per
        major step.

        Args:
            context (ContextBase):
                The simulation context at the end of the simulation step.
            ode_sol (ODESolution):
                The results of the ODE solver call.

        Returns:
            JaxResultsData: The updated simulation solution data.
        """

        # Index of the current major step in the solution data.
        index = self.n_major_steps

        if ode_sol is not None:
            # The second entries in `ode_sol` contain all steps (first is just the end result)
            ys, ts = ode_sol.ys[1], ode_sol.ts[1]
            n_minor_steps = ode_sol.stats["num_accepted_steps"]

            # Reconstruct the signal at all ODE solver steps
            y = self.scan_eval_sources(context, ys, ts, self.max_minor_steps + 1)

            outputs = {
                key: self.outputs[key].at[index].set(y[key]) for key in self.source_dict
            }

            time = self.time.at[index].set(ts)

        else:
            # Pure discrete system: no ODE solver steps
            ys = context.continuous_state
            n_minor_steps = 1

            # In this case we only need to get the signal at the current step,
            # since there are no intermediate steps from the ODE solver.
            y = self.eval_sources(context)

            outputs = {
                key: self.outputs[key].at[index, 0].set(y[key])
                for key in self.source_dict
            }

            # Set the first entry of the time vector to the current time.
            # The rest will still be inf, indicating unused buffer entries.
            time = self.time.at[index, 0].set(context.time)

        solution = dataclasses.replace(
            self,
            outputs=outputs,
            time=time,
            n_minor_steps=self.n_minor_steps.at[index].set(n_minor_steps),
            n_major_steps=index + 1,
        )

        return solution

    def finalize(self) -> tuple[Array, dict[str, Array]]:
        """Trim unused buffer space from the solution data.

        The raw solution data contains the full 'buffer' of max_minor_steps ODE solver steps and
        max_major_steps time intervals. This function trims the unused buffer space from
        the solution data, the trimmed data.

        Because this returns variable-length arrays depending on the results of the solver
        calls it cannot be called from a JAX jit-compiled function.  Instead, call as part
        of a 'postprocessing' step after simulation is complete.  This is done by default
        if the simulation is invoked via the `simulate` function.
        """
        return _trim(self)

    @classmethod
    def _scan(cls, *args, **kwargs):
        return lax.scan(*args, **kwargs)


#
# Register as custom pytree nodes
#    https://jax.readthedocs.io/en/latest/pytrees.html#extending-pytrees
#
def _solution_flatten(solution: JaxResultsData):
    """Flatten the solution data for tracing."""
    children = (
        solution.time,
        solution.outputs,
        solution.n_minor_steps,
        solution.n_major_steps,
    )
    aux_data = (
        solution.source_dict,
        solution.max_minor_steps,
    )
    return children, aux_data


def _solution_unflatten(aux_data, children):
    """Unflatten the solution data after tracing."""
    time, outputs, n_minor_steps, n_major_steps = children
    source_dict, max_minor_steps = aux_data
    return JaxResultsData(
        source_dict=source_dict,
        time=time,
        outputs=outputs,
        n_minor_steps=n_minor_steps,
        n_major_steps=n_major_steps,
        max_minor_steps=max_minor_steps,
    )


jax.tree_util.register_pytree_node(
    JaxResultsData,
    _solution_flatten,
    _solution_unflatten,
)
