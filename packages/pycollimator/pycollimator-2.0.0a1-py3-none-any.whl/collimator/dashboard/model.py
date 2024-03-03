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

import asyncio
import io
import json
import logging
import time

from collimator.dashboard.serialization import model_json, to_model_json
from collimator.framework import Diagram
from collimator.library import ReferenceSubdiagram
from collimator.simulation.types import SimulationResults

from . import api, results


logger = logging.getLogger(__name__)


class SimulationFailedError(api.CollimatorApiError):
    pass


def get_reference_submodel(project_uuid: str, model_uuid: str) -> model_json.Model:
    """
    Retrieves the reference submodel for a given project UUID and model UUID.

    Args:
        project_uuid (str): The UUID of the project.
        model_uuid (str): The UUID of the model.

    Returns:
        model_json.Model: The reference submodel as a Model object.

    Raises:
        None

    """
    try:
        model_dict = api.get(f"/project/{project_uuid}/submodels/{model_uuid}")
    except api.CollimatorNotFoundError:
        return None
    model_json_str = json.dumps(model_dict)
    return model_json.Model.from_json(io.StringIO(model_json_str))


def create_reference_submodel(
    project_uuid: str,
    model_uuid: str,
    model: model_json.Model,
    parameter_definitions=list[model_json.ParameterDefinition],
):
    """
    Create a reference submodel.

    Args:
        project_uuid (str): The UUID of the project.
        model_uuid (str): The UUID of the model.
        model (model_json.Model): The model object.
        parameter_definitions (list[model_json.ParameterDefinition], optional): The list of parameter definitions. Defaults to an empty list.

    Returns:
        dict: The response from the API.
    """
    return api.post(
        f"/project/{project_uuid}/submodels",
        body={
            "uuid": model_uuid,
            "name": model.name,
            "diagram": model.diagram,
            "parameter_definitions": parameter_definitions,
            "submodels": model.subdiagrams,
        },
    )


def update_reference_submodel(
    project_uuid: str,
    model_uuid: str,
    model: model_json.Model,
    edit_id: str,
    parameter_definitions: list[model_json.ParameterDefinition] = None,
):
    """
    Update a reference submodel in the dashboard.

    Args:
        project_uuid (str): The UUID of the project.
        model_uuid (str): The UUID of the submodel to be updated.
        model (model_json.Model): The updated model object.
        edit_id (str): The ID of the edit.
        parameter_definitions (list[model_json.ParameterDefinition], optional): The list of parameter definitions. Defaults to None.

    Returns:
        dict: The response from the API call.
    """
    body = {
        "name": model.name,
        "diagram": model.diagram,
        "submodels": model.subdiagrams,
        "edit_id": edit_id,
    }

    if parameter_definitions is not None:
        body["parameter_definitions"] = parameter_definitions

    return api.call(
        f"/project/{project_uuid}/submodels/{model_uuid}",
        "PUT",
        body=body,
    )


def get_model(model_uuid: str) -> model_json.Model:
    """
    Retrieves a model from the API based on its UUID.

    Args:
        model_uuid (str): The UUID of the model to retrieve.

    Returns:
        model_json.Model: The retrieved model object.

    Raises:
        None

    """
    try:
        model_dict = api.get(f"/models/{model_uuid}")
    except api.CollimatorNotFoundError:
        return None
    model_json_str = json.dumps(model_dict)
    return model_json.Model.from_json(io.StringIO(model_json_str))


def create_model(project_uuid: str, model: model_json.Model):
    """
    Creates a new model in the dashboard.

    Args:
        project_uuid (str): The UUID of the project to which the model belongs.
        model (model_json.Model): The model object containing the details of the model.

    Returns:
        dict: The response from the API containing the details of the created model.
    """

    body = {
        "name": model.name,
        "diagram": model.diagram,
        "project_uuid": project_uuid,
        "configuration": model.configuration,
    }

    return api.post(
        "/models",
        body=body,
    )


def update_model(model_uuid: str, model: model_json.Model):
    """
    Update the specified model with the given model data.

    Args:
        model_uuid (str): The UUID of the model to be updated.
        model (model_json.Model): The updated model data.

    Returns:
        dict: The response from the API call.
    """

    body = {
        "configuration": model.configuration,
        "diagram": model.diagram,
        "name": model.name,
        "submodels": model.subdiagrams,
        "state_machines": model.state_machines,
        "version": model.version if model else 1,
    }

    if model.parameters is not None:
        body["parameters"] = model.parameters

    return api.call(
        f"/models/{model_uuid}",
        "PUT",
        body=body,
    )


BlockNamePortIdPair = tuple[str, int]


def _find_link(
    diagram: model_json.Diagram, src: BlockNamePortIdPair, dst: BlockNamePortIdPair
):
    src_block = _find_node_by_name(diagram, src[0])
    dst_block = _find_node_by_name(diagram, dst[0])
    if not src_block or not dst_block:
        return None

    for link in diagram.links:
        node_match = src_block.uuid == link.src.node and dst_block.uuid == link.dst.node
        port_match = src[1] == link.src.port and dst[1] == link.dst.port
        if node_match and port_match:
            return link


def _find_node_by_name(diagram: model_json.Diagram, name: str):
    for node in diagram.nodes:
        if node.name == name:
            return node


def _copy_uiprops(model1: model_json.Model, model2: model_json.Model):
    for link1 in model1.diagram.links:
        if link1.uiprops is None:
            continue

        src_node = model1.diagram.find_node(link1.src.node)
        dst_node = model1.diagram.find_node(link1.dst.node)
        link2 = _find_link(
            model2.diagram,
            (src_node.name, link1.src.port),
            (dst_node.name, link1.dst.port),
        )
        if link2 is not None:
            link2.uiprops = link1.uiprops

    for node1 in model1.diagram.nodes:
        if node1.uiprops is None:
            continue
        node2 = _find_node_by_name(model2.diagram, node1.name)
        if node2 is not None:
            node2.uiprops = node1.uiprops

    for group_uuid1, group_diagram1 in model1.subdiagrams.diagrams.items():
        group_diagram2 = model2.subdiagrams.diagrams.get(group_uuid1)
        if group_diagram2 is not None:
            _copy_uiprops(group_diagram1, group_diagram2)


def put_model(
    project_uuid: str,
    diagram: Diagram,
    configuration: model_json.Configuration = None,
):
    """
    Updates or creates a model in the dashboard based on the provided diagram.

    Args:
        project_uuid (str): The UUID of the project to which the model belongs.
        diagram (Diagram): The diagram object representing the model.
        configuration (model_json.Configuration, optional): The configuration object for the model. Defaults to None.

    Returns:
        str: The UUID of the updated or created model.

    Raises:
        None
    """
    model_json, ref_submodels = to_model_json.convert(
        diagram,
        configuration=configuration,
    )

    for ref_id, ref_submodel in ref_submodels.items():
        submodel = get_reference_submodel(project_uuid, ref_id)
        submodel_uuid = ref_id
        param_def = ReferenceSubdiagram.get_parameter_definitions(ref_id)
        if submodel is None:
            logger.info("Creating submodel %s (%s)", ref_submodel.name, ref_id)
            response = create_reference_submodel(
                project_uuid, ref_id, ref_submodel, param_def
            )
            submodel_uuid = response["uuid"]
            edit_id = response["edit_id"]
        else:
            edit_id = submodel.edit_id
            _copy_uiprops(submodel, ref_submodel)
        logger.info("Updating submodel %s (%s)", ref_submodel.name, submodel_uuid)
        update_reference_submodel(
            project_uuid,
            submodel_uuid,
            ref_submodel,
            edit_id,
            parameter_definitions=param_def,
        )

    model_uuid = diagram.ui_id

    model = None
    if model_uuid:
        model = get_model(model_uuid)

    if model is None:
        if model_uuid is not None:
            logger.warning("Model %s not found", model_uuid)
        response = create_model(project_uuid, model_json)
        model_uuid = response["uuid"]
        logger.info("Creating model %s", model_uuid)
    else:
        model_json.version = model.version
        _copy_uiprops(model, model_json)

    logger.info("Updating model %s", model_uuid)

    update_model(model_uuid, model_json)

    return model_uuid


def stop_simulation(model_uuid: str, simulation_uuid: str) -> dict:
    """
    Stops a running simulation.

    Args:
        model_uuid (str): The UUID of the model for which the simulation is running.
        simulation_uuid (str): The UUID of the simulation to stop.

    Returns:
        dict: The response from the API call.

    """
    return api.post(
        f"/models/{model_uuid}/simulations/{simulation_uuid}/events",
        body={"command": "stop"},
    )


async def run_simulation(
    model_uuid: str, timeout: int = None, ignore_cache: bool = False
) -> SimulationResults:
    """
    Runs a simulation for the specified model UUID.

    Args:
        model_uuid (str): The UUID of the model to run the simulation for.
        timeout (int, optional): The maximum time to wait for the simulation to complete, in seconds. Defaults to None.

    Returns:
        SimulationResults: The results of the simulation.

    Raises:
        TimeoutError: If the simulation does not complete within the specified timeout.
        SimulationFailedError: If the simulation fails.

    """
    start_time = time.perf_counter()
    summary = api.post(
        f"/models/{model_uuid}/simulations", body={"ignore_cache": ignore_cache}
    )

    # wait for simulation completion
    while summary["status"] not in ("completed", "failed"):
        await asyncio.sleep(1)
        logger.info("Waiting for simulation to complete...")
        summary = api.get(f"/models/{model_uuid}/simulations/{summary['uuid']}")
        if timeout is not None and time.perf_counter() - start_time > timeout:
            stop_simulation(model_uuid, summary["uuid"])
            raise TimeoutError

    logs = api.get(f"/models/{model_uuid}/simulations/{summary['uuid']}/logs")
    logger.info(logs)

    if summary["status"] == "failed":
        raise SimulationFailedError(summary["fail_reason"])

    signals = results.get_signals(model_uuid, summary["uuid"])

    return SimulationResults(
        context=None,
        time=signals["time"],
        outputs=signals,
    )
