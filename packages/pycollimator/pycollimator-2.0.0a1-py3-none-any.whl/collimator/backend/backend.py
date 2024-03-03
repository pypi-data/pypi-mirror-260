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
from typing import Callable

import numpy as np
from jax.tree_util import register_pytree_node_class

from ._numpy import numpy_functions, numpy_constants
from ._jax import jax_functions, jax_constants
from ._torch import torch_functions, torch_constants
from .ode_solver import ODESolverOptions
from .results_data import AbstractResultsData

DEFAULT_BACKEND = "jax"


def _make_backend(name, functions, constants):
    # Create a new class with the given name and attributes
    static_functions = {
        name: staticmethod(function) for name, function in functions.items()
    }
    attrs = {**static_functions, **constants}
    return type(name, (), attrs)()


class MathDispatcher:
    """Singleton class for calling out to the appropriate backend."""

    _active_backend = DEFAULT_BACKEND

    _backends = {
        "jax": _make_backend("JaxBackend", jax_functions, jax_constants),
        "torch": _make_backend("TorchBackend", torch_functions, torch_constants),
        "numpy": _make_backend("NumpyBackend", numpy_functions, numpy_constants),
    }

    @property
    def active_backend(self) -> str:
        return self._active_backend

    def set_backend(self, backend: str):
        self._active_backend = backend

    def __getattr__(self, name):
        backend = self._backends[self.active_backend]
        # First look for the attribute in the backend in case the default is overridden
        if hasattr(backend, name):
            return getattr(self._backends[self.active_backend], name)
        # Else try to get it from the underlying lib
        if hasattr(backend.lib, name):
            return getattr(backend.lib, name)
        raise AttributeError(f"Backend {self.active_backend} has no attribute {name}")

    def function(self, name: str) -> Callable:
        # These seem to have to be wrapped in a function to avoid fixing
        # the backend at the time of definition.
        def _call(*args, **kwargs):
            return getattr(self, name)(*args, **kwargs)

        return _call

    @property
    def Rotation(self):
        return self._backends[self.active_backend].Rotation

    @property
    def ResultsDataImpl(self) -> AbstractResultsData:
        return self._backends[self.active_backend].ResultsDataImpl


dispatcher = MathDispatcher()

# TODO: Do we need to be specific about which version of these constants gets used?
inf = np.inf
nan = np.nan

# Alias some core functions for convenience
asarray = dispatcher.function("asarray")
array = dispatcher.function("array")
zeros = dispatcher.function("zeros")
zeros_like = dispatcher.function("zeros_like")
reshape = dispatcher.function("reshape")
cond = dispatcher.function("cond")
scan = dispatcher.function("scan")
jit = dispatcher.function("jit")
io_callback = dispatcher.function("io_callback")
pure_callback = dispatcher.function("pure_callback")
Rotation = dispatcher.Rotation

ODESolver = dispatcher.function("ODESolver")


# Inherits docstring from AbstractResultsData
@register_pytree_node_class
class ResultsData(AbstractResultsData):
    def __init__(self, solution_data: AbstractResultsData):
        self._solution_data = solution_data

    @staticmethod
    def initialize(*args, **kwargs) -> ResultsData:
        solution = dispatcher.ResultsDataImpl.initialize(*args, **kwargs)
        return ResultsData(solution)

    def update(self, *args, **kwargs) -> ResultsData:
        solution = self._solution_data.update(*args, **kwargs)
        return ResultsData(solution)

    def finalize(self):
        return self._solution_data.finalize()

    @classmethod
    def _scan(cls, *args, **kwargs):
        return scan(*args, **kwargs)

    def tree_flatten(self):
        return (self._solution_data,), None

    @classmethod
    def tree_unflatten(cls, aux_data, children):
        (solution_data,) = children
        return ResultsData(solution_data)


def odeint(
    system,
    context,
    t_span,
    t_eval=None,
    ode_options: ODESolverOptions = None,
):
    """Interface to diffrax ODE solvers.

    This is not directly used in the main simulation loop, but is intended to
    be a SciPy-like interface for development/testing/etc in continuous-time-only
    systems.
    """
    if ode_options is None:
        ode_options = ODESolverOptions()
    ode_options.save_steps = t_eval is not None

    solve = ODESolver(system, options=ode_options)
    sol, context = solve(context, t_span, t_eval=t_eval)

    if t_eval is None:
        ys = sol.ys[0]
    else:
        ys = sol.ys[1]

    return ys
