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

import jax
from jax import lax
import jax.numpy as jnp
from jax.scipy.spatial.transform import Rotation

from .ode_solver import ODESolver
from .results_data import JaxResultsData

__all__ = ["jax_functions", "jax_constants"]


jax_functions = {
    "cond": lax.cond,
    "scan": lax.scan,
    "jit": jax.jit,
    "io_callback": jax.experimental.io_callback,
    "pure_callback": jax.pure_callback,
    "ODESolver": ODESolver,
}

jax_constants = {
    "lib": jnp,
    "Rotation": Rotation,
    "ResultsDataImpl": JaxResultsData,
}
