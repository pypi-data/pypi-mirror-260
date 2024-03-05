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
from typing import TYPE_CHECKING, Tuple

import jax
import numpy as np
from jax import tree_util
from jax.flatten_util import ravel_pytree
from scipy.integrate import OdeSolution as ScipySolution, solve_ivp

from ..ode_solver import ODESolverBase, ODESolution, ODESolverOptions

if TYPE_CHECKING:
    from ..typing import Array
    from ...framework import ContextBase, SystemBase


__all__ = ["ODESolver"]


class ScipyInterpolant(ScipySolution):
    def __init__(self, result, unravel):
        self._unravel = unravel
        super().__init__(result.sol.ts, result.sol.interpolants)

    def evaluate(self, time: float):
        y = super().__call__(time)
        return self._unravel(y)


@dataclasses.dataclass
class ScipySolver(ODESolverBase):
    supported_methods = {
        "default": "RK45",
        "non-stiff": "RK45",
        "stiff": "BDF",
        "RK45": "RK45",
        "RK23": "RK23",
        "DOP853": "DOP853",
        "Radau": "Radau",
        "BDF": "BDF",
        "LSODA": "LSODA",
    }

    def make_ravel(self, pytree):
        x, unravel = ravel_pytree(pytree)

        def ravel(x):
            return np.hstack(tree_util.tree_leaves(x)).reshape(-1)

        return x, ravel, unravel

    def _finalize(self):
        """Create a wrapper for scipy.integrate.solve_ivp for ODE solving

        This can be used in cases where diffrax cannot - specifically when the system
        time derivatives are not traceable by JAX. However, it is expected to typically
        be less efficient than the JIT-compiled versions from JAX or diffrax.
        """
        try:
            method = self.supported_methods[self.method]
        except KeyError:
            raise ValueError(
                f"Invalid method '{self.method}' for SciPy ODE solver. Must be one of "
                f"{list(self.supported_methods.keys())}"
            )

        self.options = {
            "method": method,
            "rtol": self.rtol,
            "atol": self.atol,
            "max_step": self.max_step_size or np.inf,
            "dense_output": self.return_step_interpolant,
        }

        if self.method == "LSODA":
            self.options["min_step"] = self.min_step_size or 0.0

    def _solve(
        self, context: ContextBase, t_span: Tuple[float, float], t_eval: Array = None
    ) -> Tuple[ODESolution, ContextBase]:
        # Extract flattened symbolic variables from the context along with information
        # to recreate the tree structure from the solution data.
        xc0, ravel, unravel = self.make_ravel(context.continuous_state)

        def f(t, y, context):
            xc = unravel(y)
            xcdot = self.ode_rhs(self.system, t, xc, context)
            return ravel(xcdot)

        sol = solve_ivp(f, t_span, xc0, t_eval=t_eval, args=(context,), **self.options)
        num_accepted_steps = len(sol.t) - 1

        # The default diffrax solver uses a fixed "buffer" size because JAX arrays
        # are immutable and cannot vary in shape. To simulate this, pad the solution
        # with NaNs to the maximum number of steps.
        if len(sol.t) > self.max_steps:
            raise RuntimeError(
                "TODO: Support variable solution length when not using JAX"
            )
        else:
            sol.t = np.append(sol.t, np.full((self.max_steps - len(sol.t),), np.nan))
            sol.y = np.append(
                sol.y,
                np.full((sol.y.shape[0], self.max_steps - sol.y.shape[1]), np.nan),
                axis=1,
            )

        # Restore the pytree structure
        # FIXME: Do this without JAX, and needing to tree_map back to numpyu
        xs = jax.vmap(unravel)(sol.y.T)
        ts = sol.t

        xs = tree_util.tree_map(np.asarray, xs)

        # Extract the final time/state
        xf = tree_util.tree_map(lambda x: x[num_accepted_steps], xs)
        tf = ts[num_accepted_steps]

        # Diffrax will return a tuple where the first element is the final state and
        # the second element is a list of all the intermediate steps.
        stats = {"num_accepted_steps": num_accepted_steps}

        if self.return_step_interpolant:
            step_interpolant = ScipyInterpolant(sol, unravel)
        else:
            step_interpolant = None

        n_steps = num_accepted_steps
        sol_out = ODESolution((xf, xs), (tf, ts), n_steps, stats, step_interpolant)
        return sol_out, context


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

    return ScipySolver(system, **options)
