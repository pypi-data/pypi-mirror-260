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

import numpy as np
from scipy.spatial.transform import Rotation

from .python_functions import cond, scan, callback, jit
from .ode_solver import ODESolver
from .results_data import NumpyResultsData

__all__ = ["numpy_functions", "numpy_constants"]


numpy_functions = {
    "cond": cond,
    "scan": scan,
    "jit": jit,
    "io_callback": callback,
    "pure_callback": callback,
    "ODESolver": ODESolver,
}

numpy_constants = {
    "lib": np,
    "Rotation": Rotation,
    "ResultsDataImpl": NumpyResultsData,
}
