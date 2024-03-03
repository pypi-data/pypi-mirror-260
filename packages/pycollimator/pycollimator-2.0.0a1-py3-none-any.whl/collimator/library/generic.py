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

from ..framework import LeafSystem, DependencyTicket
from ..backend import asarray

__all__ = [
    "SourceBlock",
    "FeedthroughBlock",
    "ReduceBlock",
]


def _add_parameters(sys, parameters):
    """Add parameters to a system.

    These will appear in created contexts, hence are optimizable via
    differentiation through simulations.
    """
    for key, val in parameters.items():
        # Check if the parameter is convertible to an array
        #   If not, it will be stored as an arbitrary object and it's up
        #   to the user to handle it appropriately.
        try:
            asarray(val)
            param_as_array = True
        except TypeError:
            param_as_array = False

        sys.declare_parameter(key, val, as_array=param_as_array)


class SourceBlock(LeafSystem):
    """Simple blocks with a single time-dependent output"""

    def __init__(self, func: Callable, parameters={}, **kwargs):
        """Create a source block with a time-dependent output.

        Args:
            func (Callable):
                A function of time and parameters that returns a single value.
                Signature should be `func(time, **parameters) -> Array`.
            name (str): Name of the block.
            system_id (int): Unique ID of the block.
            parameters (dict): Dictionary of parameters to add to the block.
        """
        super().__init__(**kwargs)

        _add_parameters(self, parameters)

        def _callback(time, state, *inputs, **parameters):
            return func(time, **parameters)

        self.declare_output_port(
            _callback,
            name="out_0",
            prerequisites_of_calc=[DependencyTicket.time],
            requires_inputs=False,
        )


class FeedthroughBlock(LeafSystem):
    """Simple feedthrough blocks with a function of a single input"""

    def __init__(self, func, parameters={}, **kwargs):
        super().__init__(**kwargs)
        self.declare_input_port()

        _add_parameters(self, parameters)

        def _callback(time, state, *inputs, **parameters):
            return func(*inputs, **parameters)

        self.declare_output_port(
            _callback,
            prerequisites_of_calc=[self.input_ports[0].ticket],
            requires_inputs=True,
        )


class ReduceBlock(LeafSystem):
    def __init__(self, n_in, op, parameters={}, **kwargs):
        super().__init__(**kwargs)

        _add_parameters(self, parameters)

        for i in range(n_in):
            self.declare_input_port()

        def _compute_output(time, state, *inputs, **parameters):
            return op(inputs, **parameters)

        self.declare_output_port(
            _compute_output,
            prerequisites_of_calc=[port.ticket for port in self.input_ports],
            requires_inputs=True,
        )
