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

from .backend import (
    DEFAULT_BACKEND,
    dispatcher,
    asarray,
    array,
    zeros,
    zeros_like,
    reshape,
    Rotation,
    cond,
    scan,
    jit,
    io_callback,
    pure_callback,
    odeint,
    ODESolver,
    ResultsData,
    inf,
    nan,
)

from .ode_solver import ODESolution, ODESolverOptions

# Alternate name for clear imports `from collimator.backend import numpy_api`
numpy_api = dispatcher

__all__ = [
    "DEFAULT_BACKEND",
    "dispatcher",
    "asarray",
    "array",
    "zeros",
    "zeros_like",
    "reshape",
    "Rotation",
    "cond",
    "scan",
    "jit",
    "io_callback",
    "pure_callback",
    "odeint",
    "ODESolver",
    "ODESolution",
    "ODESolverOptions",
    "ResultsData",
    "inf",
    "nan",
]
