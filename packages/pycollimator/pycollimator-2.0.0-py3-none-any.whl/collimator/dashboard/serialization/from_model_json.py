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

import dataclasses
import io
import math
from typing import Any

import jax.numpy as jnp
import numpy as np

from collimator import backend, logging
from collimator.framework.error import (
    CollimatorError,
    BlockParameterError,
    BlockInitializationError,
    ModelInitializationError,
    StaticError,
    LegacyBlockConfigurationError,
)
from collimator.lazy_loader import LazyLoader

control = LazyLoader("control", globals(), "control")

from collimator.framework import (
    Diagram,
    DiagramBuilder,
    SystemBase,
    SystemCallback,
)
from collimator.library import ReferenceSubdiagram
from collimator.simulation import (
    ResultsOptions,
    SimulatorOptions,
    simulate,
    ResultsMode,
)
from . import block_interface
from . import model_json


"""
Layer between the Collimator app JSON output and the sim engine.
Presently, this works for model.json+list[submodel-uuid-ver.json] content
from both simworkerpy(wildcat) and simworker(go)(cmlc).

Processing steps:
1] The classes in types.py are used to "read" the json, packaging convinently
Not ideal, but there is some transformation that happen here.
Specifically, model.json.parameters dict is transformed to match List[ParameterDefinition]
so that the top level diagram and all submodel diagrams can be treated identically
w.r.t. parameter namespace handling at later loading stages.

2] visit all the model subdiagrams by depth first search through the json.
create node name_path ids, and a dict diagrams[subdiagram_node_id]=LoadCtxtDiagram (e.g. most the raw json content).

3] visit all the elements of diagrams dict, and build a wildcat diagram object for each, composing them as we go.

"""


@dataclasses.dataclass
class SimulationContext:
    model_uuid: str
    diagram: Diagram
    results_options: ResultsOptions
    recorded_signals: dict[str, SystemCallback]
    simulator_options: SimulatorOptions = None


def loads_model(
    model_json_str: str,
    namespace: dict[str, Any] = None,
) -> SimulationContext:
    """Load a model from a JSON string.

    Reference submodels must be registered before calling this function.
    """
    if namespace is None:
        namespace = {}
    model_fp = io.StringIO(model_json_str)
    model = model_json.Model.from_json(model_fp)

    root_namespace = namespace
    model_parameters = eval_parameters(
        default_parameters=model.parameter_definitions,
        instance_parameters=model.parameters,
        call_site_namespace=namespace,
        name_path=[],
        ui_id_path=[],
    )
    root_namespace.update(model_parameters)

    recorded_signals = {}
    diagram = make_subdiagram(
        "root",
        model.diagram,
        model.subdiagrams,
        model.state_machines,
        parent_path=[],
        parent_ui_id_path=[],
        ui_id=model.diagram.uuid,
        namespace_params=root_namespace,
        global_discrete_interval=model.configuration.sample_time,
        record_mode=model.configuration.record_mode,
        recorded_signals=recorded_signals,
        start_time=model.configuration.start_time,
    )

    results_options = None
    if model.configuration:
        results_options, simulator_options = simulation_settings(
            model.configuration, recorded_signals=recorded_signals
        )

    return SimulationContext(
        model_uuid=model.uuid,
        diagram=diagram,
        results_options=results_options,
        recorded_signals=recorded_signals,
        simulator_options=simulator_options,
    )


def eval_parameter(value: str, _globals: dict, _locals: dict):
    # Block parameters can be left empty, but JSON may contain null or "None"
    if not value or value == "None":
        return None
    p = eval(str(value), _globals, _locals)
    # Rules for user-input parameters:
    # - if explicitly given as an array with dtype, use that dtype
    # - if boolean, use as given
    # - otherwise, convert to a numpy array
    if not hasattr(p, "dtype") and not isinstance(p, bool):
        p = np.array(p)
        # if the array has integer dtype convert to float. Note that
        # this case will still not be reached if the parameter is explicitly
        # declared as an array with integer datatype.  However, this will
        # promote inputs like `"0"` or `"[1, 0]"` to floats.
        if issubclass(p.dtype.type, np.integer):
            p = p.astype(float)
    return p


def eval_parameters(
    default_parameters: list[model_json.ParameterDefinition] = None,
    instance_parameters: dict[str, model_json.Parameter] = None,
    call_site_namespace: dict[str, Any] = None,
    name_path: list[str] = None,
    ui_id_path: list[str] = None,
):
    # parameter handling.
    # at this point we have the following:
    # 1] diagrams[block_id].default_parameters
    #   these are from the submodel-uuid-ver.json[parameter_definitions].
    #   these are the definitions and defaults for all parameters in the name space of the submodel
    # 2] instance_parameters
    #   these are the parameter values from the instance of the submodel. this must be a subset of 1]
    #   this dict is typically limited to those params which have been modified from their default value.
    #   the values of these should have been evaluated in the context of the parent of the instance.
    # 3] call_site_namespace
    #   these are the parameters in the name space of the parent.
    #   these are only used here because before getting here, only the instance parameters
    #   have been evaluated in the parent name space. if a parameters has not been modified,
    #   then we use the default value from 1] but we need to evaluate it in the parent name space.
    #
    # Note: reference submodels have a 'protected' parameter names space. parents can only pass
    # parameter values through the submodels defined parameters. i.e. there is no shared name space
    # between the reference submodel instance and its parent.

    if default_parameters is None:
        default_parameters = []
    if call_site_namespace is None:
        call_site_namespace = {}
    if instance_parameters is None:
        instance_parameters = {}

    def _eval(param_name, value: str, _locals):
        try:
            return eval_parameter(value, globals(), _locals)
        # We will probably want to be much more discriminating with respect to what gets
        # caught here. This uses exception chaining to record the offending block id
        # and parameter name.
        except Exception as exc:
            raise BlockParameterError(
                name_path=name_path, ui_id_path=ui_id_path, parameter_name=param_name
            ) from exc

    # multi round eval is required in case we have parameters that reference other parameters.
    # FIXME: WC-112 this should not be allowed
    def _multi_round_eval(params, eval_fn, _locals):
        eval_results = {}
        max_eval_depth = 10
        for i in range(max_eval_depth):
            need_eval = False
            for pname, p in params.items():
                try:
                    eval_results[pname] = eval_fn(pname, p, _locals)
                except BlockParameterError as exc:
                    if i == max_eval_depth - 1:
                        raise exc
                    need_eval = True
            _locals.update(eval_results)
            if not need_eval:
                break
        return eval_results

    # We don't technically need to pass np and jnp here, but it makes them explicitly
    # available in the local `eval` environment.
    _locals = {
        **call_site_namespace,
        "np": np,
        "jnp": jnp,
        "math": math,
        "false": False,
        "true": True,
    }

    def _eval_param_def(pname, p, _locals):
        if p.default_value != "":
            return _eval(pname, p.default_value, _locals)
        return None

    default_values = _multi_round_eval(
        {p.name: p for p in default_parameters},
        _eval_param_def,
        _locals,
    )
    instance_values = _multi_round_eval(
        instance_parameters,
        lambda pname, p, l: _eval(pname, p.value, l) if not p.is_string else p.value,
        _locals,
    )

    default_values.update(instance_values)
    return default_values


def eval_init_script(
    init_script_file_name: str,
    namespace_params: dict = None,
    name_path: list[str] = None,
    ui_id_path: list[str] = None,
) -> dict:
    # FIXME: don't do this:
    # We don't technically need to pass np and jnp here, but it makes them explicitly
    # available in the local `exec` environment. a user could also do these imports.
    # "__main__": {} is necessary for script of the form
    #   imports ...
    #   a = 1
    #   def f(b):
    #       return a+b
    #   out_0 = f(2)
    # withotu getting "a not defined" error.

    namespace_params = namespace_params or {}

    _locals = {
        **namespace_params,
        "np": np,
        "jnp": jnp,
        "control": control,
        "__main__": {},
    }

    with open(init_script_file_name, "r") as file:
        _init_script_code = file.read()

    try:
        exec(_init_script_code, _locals, _locals)
    except Exception as e:
        raise ModelInitializationError(
            f"Failed to execute init_script {init_script_file_name}",
            name_path=name_path,
            ui_id_path=ui_id_path,
        ) from e

    # _locals will be pretty messy after exec() since it wil contain all the stuff
    # python puts in globals for any execution. doesn't matter, this globals env
    # is only retained for parameter evaluation.
    return _locals


def GroupBlock(
    block_spec: model_json.Node,
    global_discrete_interval: float,
    subdiagrams: dict[str, model_json.Diagram],
    state_machines: dict[str, model_json.LoadStateMachine],
    parent_path: list[str],
    parent_ui_id_path: list[str],
    record_mode: str = "selected",
    namespace_params: dict[str, Any] = None,
    block_overrides=None,
    recorded_signals=None,
    start_time: float = 0.0,
) -> Diagram:
    return make_subdiagram(
        block_spec.name,
        subdiagrams.get_diagram(block_spec.uuid),
        subdiagrams,
        state_machines,
        ui_id=block_spec.uuid,
        parent_path=parent_path,
        parent_ui_id_path=parent_ui_id_path,
        global_discrete_interval=global_discrete_interval,
        namespace_params=namespace_params or {},
        block_overrides=block_overrides,
        record_mode=record_mode,
        recorded_signals=recorded_signals,
        start_time=start_time,
    )


def register_reference_submodel(ref_id: str, model: model_json.Model):
    def _make_subdiagram_instance(
        global_discrete_interval,
        block_name,
        parameters,
        parent_path,
        parent_ui_id_path,
        record_mode,
        recorded_signals,
        uuid,
        start_time,
    ):
        namespace_params = {k: p.evaluated_value for k, p in parameters.items()}
        diagram = dataclasses.replace(model.diagram, uuid=uuid)
        return make_subdiagram(
            block_name,
            diagram,
            model.subdiagrams,
            model.state_machines,
            namespace_params=namespace_params,
            ui_id=uuid,
            parent_path=parent_path,
            parent_ui_id_path=parent_ui_id_path,
            global_discrete_interval=global_discrete_interval,
            record_mode=record_mode,
            recorded_signals=recorded_signals,
            start_time=start_time,
        )

    parameters = None
    if model.parameter_definitions:
        parameters = model.parameter_definitions
    elif model.parameters:
        # NOTE: simworker-go instantiates the submodel with parameters (dict of parameters)
        # see test_0080a.py for example.
        # So here we convert to parameter definitions (list of ParameterDefinition).
        logging.debug("Converting instantiated parameters to parameter definitions.")
        parameters = [
            model_json.ParameterDefinition(name=k, default_value=v.value)
            for k, v in model.parameters.items()
        ]

    ReferenceSubdiagram.register(
        ref_id,
        _make_subdiagram_instance,
        parameter_definitions=parameters,
    )


# FIXME: simplify this function. it's too long.
# pylint: disable=too-complex
# flake8: noqa: C901
def make_subdiagram(
    name: str,
    diagram: model_json.Diagram,
    subdiagrams: dict[str, model_json.Diagram],
    state_machines: dict[str, model_json.LoadStateMachine],
    parent_path: list[str],
    parent_ui_id_path: list[str],
    ui_id: str = None,
    namespace_params=None,
    block_overrides: dict[str, SystemBase] = None,
    record_mode: str = "selected",
    recorded_signals: dict[str, SystemCallback] = None,
    global_discrete_interval: float = 0.1,
    start_time: float = 0.0,
) -> Diagram:
    if namespace_params is None:
        namespace_params = {}

    # The "node_spec" passed here is the "node" specification that doesn't
    # contain the actual blocks. the info about the block tat constains the
    # subdiagram, e.g. submodel instance.

    # TODO: correctly handle RefSubmodelConfiguration features
    # (atomic, discrete_step)

    builder = DiagramBuilder()

    # I/O ports are considered "blocks" in the UI, so they need to be tracked
    # specificially (lists of block names)
    exported_inputs: list[str] = []
    exported_outputs: list[str] = []

    # needed for dereferencing node ids in link specs. this map is local to a
    # canvas.
    block_uuid_to_name: dict[str, str] = {}

    # block name to created object
    blocks: dict[str, SystemBase | Diagram] = {}

    for block_spec in diagram.nodes:
        block: SystemBase | Diagram = None

        # block names are used as locally (in this canvas) unique identifiers
        block_name = block_spec.name
        block_ui_id = block_spec.uuid
        block_uuid_to_name[block_ui_id] = block_name

        # these are used for rich errors before the block is created
        block_name_path = parent_path + [block_name]
        block_ui_id_path = parent_ui_id_path + [block_ui_id]

        if block_spec.type == "core.Inport":
            exported_inputs.append(block_name)
        elif block_spec.type == "core.Outport":
            exported_outputs.append(block_name)

        try:
            # FIXME: refactor below contents of try into a function

            if block_overrides and block_name in block_overrides:
                # FIXME this was probably broken inside subdiagrams and looks extremely hacky anyway
                block_name_path_str = ".".join(block_name_path)
                block = block_overrides[block_name_path_str]

            elif block_spec.type == "core.ReferenceSubmodel":
                logging.debug(
                    "Creating reference submodel %s (ref id: %s) "
                    "with instance_parameters: %s, call_site_namespace: %s",
                    block_name,
                    block_spec.submodel_reference_uuid,
                    block_spec.parameters,
                    namespace_params,
                )

                # Note: only expressions are supported here, no string literals
                instance_parameters = {
                    k: p.value for k, p in block_spec.parameters.items()
                }
                block = ReferenceSubdiagram.create_diagram(
                    block_spec.submodel_reference_uuid,
                    global_discrete_interval=global_discrete_interval,
                    record_mode=record_mode,
                    block_name=block_name,
                    call_site_namespace=namespace_params,
                    instance_parameters=instance_parameters,
                    recorded_signals=recorded_signals,
                    parent_path=parent_path + [block_name],
                    parent_ui_id_path=parent_ui_id_path + [block_ui_id],
                    uuid=block_spec.uuid,
                    start_time=start_time,
                )
            elif block_spec.type in ("core.Group", "core.Submodel"):
                block = GroupBlock(
                    block_spec,
                    global_discrete_interval,
                    subdiagrams,
                    state_machines,
                    parent_path=parent_path + [block_name],
                    parent_ui_id_path=parent_ui_id_path + [block_ui_id],
                    namespace_params=namespace_params,
                    record_mode=record_mode,
                    recorded_signals=recorded_signals,
                    start_time=start_time,
                )
            else:
                common_kwargs = {
                    "name": block_name,
                    "ui_id": block_ui_id,
                }
                parameters = eval_parameters(
                    instance_parameters=block_spec.parameters,
                    call_site_namespace=namespace_params,
                    name_path=block_name_path,
                    ui_id_path=block_ui_id_path,
                )
                if block_spec.type == "core.StateMachine":
                    block = block_interface.get_block_fcn(block_spec.type)(
                        block_spec=block_spec,
                        discrete_interval=global_discrete_interval,
                        state_machine_diagram=state_machines.sm_diagrams[
                            block_spec.state_machine_diagram_id
                        ],
                        **common_kwargs,
                        **parameters,
                    )
                elif block_spec.type == "core.ModelicaFMU":
                    block = block_interface.get_block_fcn(block_spec.type)(
                        block_spec=block_spec,
                        discrete_interval=global_discrete_interval,
                        start_time=start_time,
                        **common_kwargs,
                        **parameters,
                    )
                else:
                    block = block_interface.get_block_fcn(block_spec.type)(
                        block_spec=block_spec,
                        discrete_interval=global_discrete_interval,
                        **common_kwargs,
                        **parameters,
                    )

                if block_spec.inputs:
                    input_port_names = [port.name for port in block_spec.inputs]
                    for port_name, port in zip(input_port_names, block.input_ports):
                        port.name = port_name

                if block_spec.outputs:
                    output_port_names = [port.name for port in block_spec.outputs]
                    for port_name, port in zip(output_port_names, block.output_ports):
                        port.name = port_name

            # NOTE: Here we assume that the port order is the same in the frontend and wildcat
            # Log anything with record=True
            if block_spec.outputs and recorded_signals is not None:
                for i, port in enumerate(block_spec.outputs):
                    if port.record or record_mode == "all":
                        port_path = parent_path + [block_name, port.name]
                        port_path = ".".join(port_path)
                        logging.debug("Recording %s", port_path)

                        if i < 0 or i >= len(block.output_ports):
                            # This unlikely error can happen when for instance there's
                            # an invalid JSON with more i/o ports than what wildcat
                            # defines (eg. old StateSpace blocks)
                            raise LegacyBlockConfigurationError(
                                message=f"Output port index {i} out of range"
                                f"({len(block.output_ports)}) for block {block.name}",
                                name_path=block_name_path,
                                ui_id_path=block_ui_id_path,
                                port_index=i,
                                port_name=port.name,
                                port_direction="out",
                            )

                        recorded_signals[port_path] = block.output_ports[i]

            builder.add(block)
            blocks[block_name] = block

        except (StaticError, BlockInitializationError) as exc:
            raise exc
        except Exception as exc:
            if isinstance(exc, CollimatorError):
                # Avoid repetition in the error message by only keeping this info in
                # the top-level error
                exc.name_path = None
                exc.system_id = None
            path = ".".join(block_name_path)
            raise BlockInitializationError(
                message=f"Failed to create block {path} of type {block_spec.type}",
                system=block,
                name_path=block_name_path,
                ui_id_path=block_ui_id_path,
            ) from exc

    # Export the input port of any Inport
    for input_port_id_key in exported_inputs:
        builder.export_input(blocks[input_port_id_key].input_ports[0])

    # Export the output port of any Outport
    for output_port_id_key in exported_outputs:
        builder.export_output(blocks[output_port_id_key].output_ports[0])

    for link in diagram.links:
        if (
            (link.src is None)
            or (link.dst is None)
            or (link.src.node not in block_uuid_to_name)
            or (link.dst.node not in block_uuid_to_name)
        ):
            continue

        src_block_name = block_uuid_to_name[link.src.node]
        dst_block_name = block_uuid_to_name[link.dst.node]
        src_port_index = int(link.src.port)
        dst_port_index = int(link.dst.port)

        # These unlikely errors can happen when for instance there's
        # an invalid JSON with more i/o ports than what wildcat
        # defines (eg. old StateSpace blocks)
        if src_port_index < 0 or src_port_index >= len(
            blocks[src_block_name].output_ports
        ):
            raise LegacyBlockConfigurationError(
                f"Invalid src port index {src_port_index} for block {blocks[src_block_name].name}",
                name_path=block_name_path,
                ui_id_path=block_ui_id_path,
            )
        elif dst_port_index < 0 or dst_port_index >= len(
            blocks[dst_block_name].input_ports
        ):
            raise LegacyBlockConfigurationError(
                f"Invalid dst port index {dst_port_index} for block {blocks[dst_block_name].name}",
                name_path=block_name_path,
                ui_id_path=block_ui_id_path,
            )

        builder.connect(
            blocks[src_block_name].output_ports[src_port_index],
            blocks[dst_block_name].input_ports[dst_port_index],
        )

    return builder.build(name=name, ui_id=ui_id)


def simulation_settings(
    config: model_json.Configuration, recorded_signals: dict[str, SystemCallback] = None
):
    sim_output_mode_lookup = {
        "auto": ResultsMode.auto,
        "discrete_steps_only": ResultsMode.discrete_steps_only,
        "fixed_interval": ResultsMode.fixed_interval,
    }
    sim_output_mode = sim_output_mode_lookup.get(
        config.sim_output_mode, ResultsMode.auto
    )

    method = config.solver.method
    if method in ["default", "non-stiff"]:
        pass
    elif method in ["RK45"]:
        method = "non-stiff"
    elif method in ["stiff", "BDF", "Kvaerno5"]:
        method = "stiff"
    else:
        raise ValueError(f"Unsupported solver method: {config.solver.method}")

    numerical_backend = config.numerical_backend or "auto"
    if numerical_backend not in ["auto", "numpy", "jax"]:
        raise ValueError(f"Unsupported numerical backend: {config.numerical_backend}")

    results_options = ResultsOptions(
        mode=sim_output_mode,
        max_results_interval=config.max_results_interval,
        fixed_results_interval=config.fixed_results_interval,
    )

    simulator_options = SimulatorOptions(
        math_backend=numerical_backend,
        max_major_steps=config.max_major_steps,
        max_major_step_length=config.sample_time,
        max_minor_steps_per_major_step=config.solver.max_minor_steps_per_major_step,
        min_minor_step_size=config.solver.min_step,
        max_minor_step_size=config.solver.max_step,
        atol=config.solver.absolute_tolerance,
        rtol=config.solver.relative_tolerance,
        ode_solver_method=method,
        return_context=False,
        recorded_signals=recorded_signals,
    )

    logging.info("Simulation settings: %s", simulator_options)
    logging.info("Results settings: %s", results_options)

    return results_options, simulator_options
