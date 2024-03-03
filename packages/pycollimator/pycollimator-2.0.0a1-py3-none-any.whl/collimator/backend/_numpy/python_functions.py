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
from jax import tree_map
import warnings

__all__ = ["cond", "scan", "callback", "jit"]


def cond(pred, true_fun, false_fun, *operands):
    if pred:
        return true_fun(*operands)
    else:
        return false_fun(*operands)


def scan(f, init, xs, length=None):
    warnings.warn("Using scan with numpy backend. This can be extremely slow.")

    if xs is None:
        xs = [None] * length
    carry = init
    ys = []
    for x in xs:
        carry, y = f(carry, x)
        ys.append(y)
    # pylint: disable=no-value-for-parameter
    stacked_ys = tree_map(lambda *ys: np.stack(ys), *ys)
    return carry, stacked_ys


def callback(callback, result_shape_dtypes, *args, **kwargs):
    return callback(*args, **kwargs)


# Dummy placeholder for JIT compilation
def jit(fun, *args, **kwargs):
    return fun
