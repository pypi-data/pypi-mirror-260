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

from dataclasses import dataclass
import dataclasses
from typing import Optional
import sys
import ts_type as ts

from dataclasses_jsonschema import JsonSchemaMixin

from collimator.framework.error import CollimatorError

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from strenum import StrEnum


def with_to_api(cls):
    def _filter_none(d: dict) -> dict:
        ret = {}
        if isinstance(d, list):
            return [_filter_none(v) for v in d]
        if not isinstance(d, dict):
            return d
        for k, v in d.items():
            if v is not None:
                ret[k] = _filter_none(v)
        return ret

    def to_api(self, omit_none=True):
        d = dataclasses.asdict(self)
        if omit_none:
            d = _filter_none(d)
        return d

    cls.to_api = to_api  # type: ignore
    return cls


@ts.gen_type
class PortDirection(StrEnum):
    IN = "in"
    OUT = "out"


@ts.gen_type
class TimeMode(StrEnum):
    CONSTANT = "Constant"
    DISCRETE = "Discrete"
    CONTINUOUS = "Continuous"
    HYBRID = "Hybrid"


@ts.gen_type
@with_to_api
@dataclass
class Port(JsonSchemaMixin):
    index: int
    dtype: str
    dimension: list[int]
    time_mode: TimeMode
    discrete_interval: Optional[float]
    name: str


@ts.gen_type
@with_to_api
@dataclass
class Node(JsonSchemaMixin):
    namepath: list[str]
    uuidpath: list[str]
    outports: list[Port]
    time_mode: TimeMode
    discrete_interval: Optional[float]


@ts.gen_type
@with_to_api
@dataclass
class SignalTypes(JsonSchemaMixin):
    nodes: list[Node]


@ts.gen_type
@with_to_api
@dataclass
class ErrorLoopItem(JsonSchemaMixin):
    name_path: Optional[str] = None
    uuid_path: Optional[list[str]] = None
    port_direction: Optional[PortDirection] = None
    port_index: Optional[int] = None


@ts.gen_type
@with_to_api
@dataclass
class ErrorLog(JsonSchemaMixin):
    kind: str
    name_path: Optional[str] = None
    uuid_path: Optional[list[str]] = None
    port_direction: Optional[str] = None
    port_name: Optional[str] = None
    port_index: Optional[int] = None
    parameter_name: Optional[str] = None
    loop: Optional[list[ErrorLoopItem]] = None

    @classmethod
    def from_error(cls, error: CollimatorError):
        def _path(loc) -> str | None:
            return ".".join(loc.name_path) if loc.name_path else None

        return cls(
            kind=error.__class__.__name__,
            name_path=_path(error),
            uuid_path=error.ui_id_path,
            port_direction=error.port_direction,
            port_name=error.port_name,
            port_index=error.port_index,
            parameter_name=error.parameter_name,
            loop=(
                [
                    ErrorLoopItem(
                        name_path=_path(loc),
                        uuid_path=loc.ui_id_path,
                        port_direction=loc.port_direction,
                        port_index=loc.port_index,
                    )
                    for loc in error.loop
                ]
                if error.loop
                else None
            ),
        )
