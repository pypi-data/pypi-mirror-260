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
This module contains types that map directly to Collimator's JSON model format.
"""

import dataclasses
import json
from typing import Any, Dict, List, Optional, TextIO
from uuid import UUID, uuid4

from dataclasses_json import dataclass_json

from collimator.simulation import ResultsOptions, SimulatorOptions

# FIXME: use dataclass_json for all definitions


@dataclasses.dataclass
class JSONObject:
    def to_json(self) -> str:
        obj_dict = dataclasses.asdict(self)
        return json.dumps(obj_dict, indent=2)


@dataclasses.dataclass
class Port:
    node: str
    port: int


@dataclasses.dataclass
class Link:
    uuid: str
    src: Port
    dst: Port
    uiprops: dict = None

    @staticmethod
    def from_dict(data: dict):
        return Link(
            uuid=data["uuid"],
            src=Port(**data["src"]) if "src" in data else None,
            dst=Port(**data["dst"]) if "dst" in data else None,
            uiprops=data.get("uiprops", {}),
        )


@dataclasses.dataclass
class Parameter(JSONObject):
    value: str
    is_string: bool = False

    @staticmethod
    def from_dict(data: dict):
        return Parameter(value=data["value"], is_string=data.get("is_string", False))


@dataclasses.dataclass
class IOPort:
    name: str
    kind: str  # static or dynamic
    parameters: dict[str, Parameter] = None
    record: bool = True

    @staticmethod
    def from_dict(data: dict):
        parameters = data.get("parameters", {})
        return IOPort(
            name=data["name"],
            kind=data.get("kind", "static"),
            parameters={k: Parameter.from_dict(v) for k, v in parameters.items()},
            record=data.get("record", False),
        )


@dataclasses.dataclass
class Node:
    name: str
    type: str = None
    inputs: list[IOPort] = dataclasses.field(default_factory=list)
    outputs: list[IOPort] = dataclasses.field(default_factory=list)
    parameters: dict[str, Parameter] = None
    uuid: str = None
    submodel_reference_uuid: str = None
    state_machine_diagram_id: str = None
    time_mode: str = None
    uiprops: dict = None

    @staticmethod
    def from_dict(data: dict):
        parameters = data.get("parameters", {})
        inputs = data.get("inputs", [])
        outputs = data.get("outputs", [])
        return Node(
            uuid=data["uuid"],
            name=data["name"],
            type=data["type"],
            inputs=[IOPort.from_dict(d) for d in inputs] if inputs else [],
            outputs=[IOPort.from_dict(d) for d in outputs] if outputs else [],
            parameters={k: Parameter.from_dict(v) for k, v in parameters.items()},
            submodel_reference_uuid=data.get("submodel_reference_uuid", None),
            state_machine_diagram_id=data.get("state_machine_diagram_id", None),
            time_mode=data.get("time_mode", "discrete"),
            uiprops=data.get("uiprops", {}),
        )


BlockNamePortIdPair = tuple[str, int]


@dataclasses.dataclass
class Diagram(JSONObject):
    uuid: str
    links: list[Link]
    nodes: list[Node]
    annotations: list[dict] = None

    @staticmethod
    def from_dict(data: dict):
        return Diagram(
            uuid=data.get("uuid", str(uuid4())),
            links=[Link.from_dict(link) for link in data["links"]],
            nodes=[Node.from_dict(n) for n in data["nodes"]],
            annotations=data.get("annotations"),
        )

    def find_node(self, uuid: str):
        for node in self.nodes:
            if node.uuid == uuid:
                return node


@dataclasses.dataclass
class Reference:
    diagram_uuid: UUID


@dataclasses.dataclass
class ParameterDefinition(JSONObject):
    name: str
    default_value: str
    uuid: str = dataclasses.field(default_factory=lambda: str(uuid4()))


@dataclass_json
@dataclasses.dataclass
class WorkSpace:
    init_scripts: list[dict] = dataclasses.field(default_factory=list)

    @staticmethod
    def from_dict(data: dict):
        return WorkSpace(init_scripts=data.get("init_scripts", []))


@dataclass_json
@dataclasses.dataclass
class SolverConfig:
    method: Optional[str] = "non-stiff"
    max_step: Optional[float] = 1e6
    min_step: Optional[float] = 0
    max_minor_steps_per_major_step: Optional[int] = 1e3
    relative_tolerance: Optional[float] = 1e-3
    absolute_tolerance: Optional[float] = 1e-6


@dataclass_json
@dataclasses.dataclass
class Configuration(JSONObject):
    stop_time: Optional[float] = 10.0
    start_time: Optional[float] = 0.0
    sample_time: Optional[float] = 0.1
    numerical_backend: Optional[str] = "auto"  # one of "auto", "numpy", "jax"
    solver: Optional[SolverConfig] = dataclasses.field(default_factory=SolverConfig)
    max_major_steps: Optional[int] = None
    sim_output_mode: Optional[str] = "auto"
    max_results_interval: Optional[float] = None
    fixed_results_interval: Optional[float] = None
    record_mode: Optional[str] = "all"  # "all" or "selected"
    workspace: Optional[WorkSpace] = dataclasses.field(default_factory=WorkSpace)

    @staticmethod
    def from_wildcat_config(
        sim_options: SimulatorOptions,
        results_options: ResultsOptions,
        stop_time: float = 10.0,
        sample_time: float = 0.1,
        workspace=None,
    ):
        return Configuration(
            record_mode="all",
            solver=SolverConfig(
                method=sim_options.ode_solver_method,
                absolute_tolerance=sim_options.atol,
                max_minor_steps_per_major_step=sim_options.max_minor_steps_per_major_step,
                relative_tolerance=sim_options.rtol,
                min_step=sim_options.min_minor_step_size,
                max_step=sim_options.max_minor_step_size,
            ),
            sample_time=sample_time,
            stop_time=stop_time,
            max_major_steps=sim_options.max_major_steps,
            sim_output_mode=results_options.mode.name,
            max_results_interval=results_options.max_results_interval,
            fixed_results_interval=results_options.fixed_results_interval,
            workspace=workspace or WorkSpace(),
        )


@dataclasses.dataclass
class Subdiagrams:
    diagrams: dict[UUID, Diagram]
    references: dict[UUID, Reference]

    def get_diagram(self, group_block_uuid: UUID) -> Diagram:
        diagram_uuid = self.references[group_block_uuid].diagram_uuid
        return self.diagrams[diagram_uuid]


#
# data classes for loading state machine raw json
#


@dataclasses.dataclass
class StateMachineState:
    name: str = None
    uuid: str = None
    exit_priority_list: List[str] = None

    @staticmethod
    def from_dict(data: dict):
        return StateMachineState(
            name=data["name"],
            uuid=data["uuid"],
            exit_priority_list=data["exit_priority_list"],
        )


@dataclasses.dataclass
class StateMachineTransition:
    uuid: str = None
    guard: str = None
    actions: List[str] = None
    dest_node_id: str = None
    source_node_id: str = None

    @staticmethod
    def from_dict(data: dict):
        return StateMachineTransition(
            uuid=data["uuid"],
            guard=data["guard"],
            actions=data["actions"],
            dest_node_id=data["destNodeId"],
            source_node_id=data["sourceNodeId"],
        )


@dataclasses.dataclass
class StateMachineEntryPoint:
    actions: List[str] = None
    dest_node_id: str = None

    @staticmethod
    def from_dict(data: dict):
        return StateMachineEntryPoint(
            actions=data["actions"],
            dest_node_id=data["dest_id"],
        )


@dataclasses.dataclass
class StateMachine:
    uuid: str = None
    links: Dict[str, StateMachineTransition] = None
    nodes: Dict[str, StateMachineState] = None
    entry_point: StateMachineEntryPoint = None

    @staticmethod
    def from_dict(data: dict):
        return StateMachine(
            uuid=data["uuid"],
            links={
                trsn["uuid"]: StateMachineTransition.from_dict(trsn)
                for trsn in data["links"]
            },
            nodes={st["uuid"]: StateMachineState.from_dict(st) for st in data["nodes"]},
            entry_point=StateMachineEntryPoint.from_dict(data["entry_point"]),
        )


@dataclasses.dataclass
class StateMachines:
    sm_diagrams: dict[UUID, StateMachine]


@dataclasses.dataclass
class Model(JSONObject):
    # intended to load model.json and submodel-uuid.ver.json
    uuid: str
    diagram: Diagram
    subdiagrams: Subdiagrams
    state_machines: StateMachines
    parameters: dict[str, Parameter]
    parameter_definitions: list[ParameterDefinition]
    name: str
    configuration: Configuration = dataclasses.field(default_factory=Configuration)
    version: int = 1

    # only for reference submodels
    edit_id: str = None

    # TODO:
    # submodel_configuration

    @staticmethod
    def from_json(fp: TextIO) -> "Model":
        return json.load(fp, cls=_ModelDecoder)


class _ModelDecoder(json.JSONDecoder):
    def decode(self, s, *args, **kwargs) -> Any:
        data = super().decode(s, *args, **kwargs)

        def field(name, dflt):
            # handles both inexisting key and None value (null)
            return data.get(name, dflt) or dflt

        # local subdiagrams
        if "submodels" in data:
            subdiagrams = field("submodels", {"diagrams": {}, "references": {}})
        else:
            subdiagrams = field("subdiagrams", {"diagrams": {}, "references": {}})
        diagrams = {k: Diagram.from_dict(d) for k, d in subdiagrams["diagrams"].items()}
        references = {k: Reference(**d) for k, d in subdiagrams["references"].items()}

        # state machines: uuid -> sm diagram
        state_machines = field("state_machines", {})
        # FIXME: dashboard test fails without 'if d' check
        sm_diagrams = {
            k: StateMachine.from_dict(d) for k, d in state_machines.items() if d
        }

        # model and submodel parameters definitions
        # FIXME why both model & submodel here? it shouldnt be
        parameter_definitions = [
            ParameterDefinition(name=p["name"], default_value=p["default_value"])
            for p in field("parameter_definitions", [])
        ]
        parameters = {
            name: Parameter(param["value"], is_string=param.get("is_string", False))
            for name, param in field("parameters", {}).items()
        }

        configuration = Configuration.from_dict(field("configuration", {}))

        return Model(
            uuid=data.get("uuid", str(uuid4())),
            diagram=Diagram.from_dict(data["diagram"]),
            subdiagrams=Subdiagrams(diagrams=diagrams, references=references),
            state_machines=StateMachines(sm_diagrams=sm_diagrams),
            parameter_definitions=parameter_definitions,
            parameters=parameters,
            configuration=configuration,
            name=data.get("name", "root"),
            version=data.get("version", 1),
            edit_id=data.get("edit_id", None),
        )
