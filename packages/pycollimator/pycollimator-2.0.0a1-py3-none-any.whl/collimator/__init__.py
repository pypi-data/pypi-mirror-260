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

import os

import jax

from . import logging
from .framework import (
    LeafSystem,
    DiagramBuilder,
)
from .backend import dispatcher as backend

from .simulation import (
    Simulator,
    simulate,
    estimate_max_major_steps,
    odeint,
    ODESolver,
    ODESolverOptions,
    SimulatorOptions,
)
from .cli import load_model
from .version import __version__

jax.config.update("jax_enable_x64", True)  # Turn off for float32 (limits accuracy)

_log_level = os.environ.get("LOG_LEVEL", "INFO")
logging.set_log_level(_log_level)

logging.set_stream_handler()

_per_package_log_levels = os.environ.get("LOG_LEVELS", None)
if _per_package_log_levels is not None:
    _per_package_log_levels = _per_package_log_levels.split(",")
    _per_package_log_levels = [level.split(":") for level in _per_package_log_levels]
    for pkg, level in _per_package_log_levels:
        logging.set_log_level(level, pkg=pkg)

set_backend = backend.set_backend

__all__ = [
    "__version__",
    "load_model",
    "LeafSystem",
    "DiagramBuilder",
    "Simulator",
    "SimulatorOptions",
    "simulate",
    "estimate_max_major_steps",
    "odeint",
    "ODESolver",
    "SimulatorOptions",
    "ODESolverOptions",
    "backend",
    "set_backend",
]
