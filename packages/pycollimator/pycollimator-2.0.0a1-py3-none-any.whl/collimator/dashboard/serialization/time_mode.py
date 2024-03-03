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

"""
These funtions are used to classify nodes and signals of a wildcat diagram in terms of the
time_modes that are displayed in the UI.
Wildcat does not rely on time_mode propagation nor assignment per-se to interpret the model,
so there is not necessray a perfect set of rules here.
The outcome is merely guidance for the user in the UI, so errors are not critical.
"""

from collimator.framework.dependency_graph import DependencyTicket
from .ui_types import TimeMode


def time_mode_node(node, ports_tm: list[TimeMode]) -> TimeMode:
    # some blocks are by definition discrete,
    # dont bother classifying based on port deps,
    # just classify by Class.
    discrete_blocks = [
        "DerivativeDiscrete",
        "DiscreteInitializer",
        "DiscreteClock",
        "FilterDiscrete",
        "IntegratorDiscrete",
        "PIDDiscrete",
        "ZeroOrderHold",
        "UnitDelay",
    ]

    # node time_mode rules.
    if node.__class__.__name__ in discrete_blocks:
        return TimeMode.DISCRETE
    elif TimeMode.CONTINUOUS in ports_tm and TimeMode.DISCRETE in ports_tm:
        # this case is actually used for subdiagrams, and ports_tm is actaully
        # a list of the subdiagams' nodes time_modes.
        return TimeMode.HYBRID
    elif TimeMode.CONTINUOUS in ports_tm:
        return TimeMode.CONTINUOUS
    elif TimeMode.DISCRETE in ports_tm:
        return TimeMode.DISCRETE
    else:
        # if nothing, this is the only options left.
        return TimeMode.CONSTANT


def time_mode_port(out_port) -> TimeMode:
    # extract the dependencies we care fabout for this port.
    dep_none = out_port.tracker.depends_on([DependencyTicket.nothing])
    dep_time = out_port.tracker.depends_on([DependencyTicket.time])
    dep_xc = out_port.tracker.depends_on([DependencyTicket.xc])
    dep_xd = out_port.tracker.depends_on([DependencyTicket.xd])
    xd_dep = out_port.tracker.is_prerequisite_of([DependencyTicket.xd])
    xcdot_dep = out_port.tracker.is_prerequisite_of([DependencyTicket.xcdot])

    # Port time_mode rules.
    if (dep_time or dep_xc) and xcdot_dep:
        return TimeMode.CONTINUOUS
    elif (dep_xd and dep_xc) and not xd_dep:
        return TimeMode.CONTINUOUS
    elif dep_xd or xd_dep:
        return TimeMode.DISCRETE
    elif dep_none and not dep_time and not dep_xc and not dep_xd:
        return TimeMode.CONSTANT
    else:
        return TimeMode.CONTINUOUS
