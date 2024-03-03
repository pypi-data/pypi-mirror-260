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

import concurrent.futures
import dataclasses
import os
import logging
import mimetypes
import requests
import tempfile
from typing import IO, AnyStr

from collimator.dashboard.serialization import (
    model_json,
    from_model_json,
    SimulationContext,
)
from collimator.dashboard.schemas import (
    FileSummary,
    ModelKind,
    ModelSummary,
    ProjectSummary,
)

from . import api, model as model_api


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Project:
    """
    Represents a project in the Collimator dashboard.

    Attributes:
        models (dict[str, SimulationContext]): A dictionary mapping model names to SimulationContext objects.
        files (list[str]): A list of file names associated with the project.
    """

    summary: ProjectSummary
    models: dict[str, SimulationContext]
    files: list[str]


def _get_reference_submodels(
    project_uuid: str, model: model_json.Model, memo: set[str]
) -> dict[str, model_json.Model]:
    """Finds submodels & HLBs referenced by a given model or submodel"""
    if model.uuid in memo:
        return {}
    memo.add(model.uuid)
    refs = {}
    for node in model.diagram.nodes:
        if node.type != "core.ReferenceSubmodel":
            continue
        if node.submodel_reference_uuid in memo:
            continue
        submodel = model_api.get_reference_submodel(
            project_uuid, node.submodel_reference_uuid
        )
        refs[node.submodel_reference_uuid] = submodel
        refs.update(_get_reference_submodels(project_uuid, submodel, memo))

    for diagram_uuid, diagram in model.subdiagrams.diagrams.items():
        if diagram.uuid in memo:
            continue
        group = model_json.Model(
            uuid=diagram_uuid,
            diagram=diagram,
            subdiagrams=model_json.Subdiagrams(diagrams={}, references={}),
            state_machines={},  # FIXME
            parameters={},
            parameter_definitions=[],
            configuration=None,
            name="",
        )
        refs.update(_get_reference_submodels(project_uuid, group, memo))

    return refs


def _parse_project_summary(project_summary: dict) -> ProjectSummary:
    models = []
    for model in project_summary.get("models", []):
        models.append(
            ModelSummary(
                uuid=model["uuid"],
                kind=ModelKind(model.get("kind", "Model")),
                name=model["name"],
            )
        )

    submodels = []
    for model in project_summary.get("reference_submodels", []):
        submodels.append(
            ModelSummary(
                uuid=model["uuid"],
                kind=ModelKind(model.get("kind", "Submodel")),
                name=model["name"],
            )
        )

    files = []
    for file in project_summary.get("files", []):
        files.append(
            FileSummary(
                uuid=file["uuid"],
                name=file["name"],
                status=file["status"],
            )
        )

    return ProjectSummary(
        uuid=project_summary["uuid"],
        title=project_summary["title"],
        models=models,
        files=files,
        reference_submodels=submodels,
    )


def _download_file(file: FileSummary, project_uuid: str, destination: str):
    response = api.get(f"/projects/{project_uuid}/files/{file.uuid}/download")
    logger.debug("Downloading %s to %s", response["download_link"], destination)
    resp = requests.get(response["download_link"])
    if resp.status_code != 200:
        logger.error(
            "Failed to download data file %s from project %s", file.name, project_uuid
        )
        return
    with open(destination, "wb") as f:
        f.write(resp.content)


def get_project_by_name(project_name: str, project_dir=None) -> Project:
    """
    Retrieves a project by its name.

    Args:
        project_name (str): The name of the project to retrieve.
        project_dir (str, optional): The directory where the project is located. If not provided, a temporary directory will be created.

    Returns:
        Project: The project object.

    Raises:
        CollimatorNotFoundError: If the project with the specified name is not found.
        CollimatorApiError: If multiple projects with the same name are found.

    """

    response = api.get("/projects")
    results = []
    for project in response["projects"]:
        if project["title"] == project_name:
            results.append(project)

    user_profile = api.get("/user/profile")

    if len(results) == 0:
        raise api.CollimatorNotFoundError(f"Project '{project_name}' not found")
    elif len(results) > 1:
        uuids = []
        for p in results:
            if p["is_default"]:
                uuids.append(f"- {p['uuid']} (public project)")
            elif p["owner_uuid"] == user_profile["uuid"]:
                uuids.append(f"- {p['uuid']} (private project)")
            else:
                uuids.append(f"- {p['uuid']} (shared with me)")
        uuids = "\n".join(uuids)

        raise api.CollimatorApiError(
            f"Multiple projects found with name '{project_name}':\n{uuids}\n"
            "Please use get_project_by_uuid() instead."
        )

    project_uuid = results[0]["uuid"]
    return get_project_by_uuid(project_uuid, project_dir)


def get_project_by_uuid(project_uuid: str, project_dir=None) -> Project:
    """
    Retrieves a project with the given UUID and downloads its files.

    Args:
        project_uuid (str): The UUID of the project to retrieve.
        project_dir (str, optional): The directory to download the project files to. If not provided, a temporary directory will be created.

    Returns:
        Project: The downloaded project, including its models and files.
    """

    logger.info("Downloading project %s...", project_uuid)

    response = api.call(f"/projects/{project_uuid}", "GET", retries=3)
    project_summary = _parse_project_summary(response)

    # download project files
    files = []

    if project_dir is None:
        project_dir = tempfile.mkdtemp()
    logger.info("Project dir: %s", project_dir)

    for file in project_summary.files:
        if file.status == "processing_completed":
            dst = os.path.join(project_dir, file.name)
            _download_file(file, project_uuid, dst)
            files.append(dst)
        else:
            logger.warning(
                "File %s is not ready to be downloaded (status: %s)",
                file.name,
                file.status,
            )

    # Must first register submodels
    visited = set()
    ref_submodels: dict[str, model_json.Model] = {}
    for model_summary in project_summary.reference_submodels:
        submodel = model_api.get_reference_submodel(project_uuid, model_summary.uuid)
        ref_submodels.update(
            {
                model_summary.uuid: submodel,
                **_get_reference_submodels(project_uuid, submodel, visited),
            }
        )
    for model_summary in project_summary.models:
        model = model_api.get_model(model_summary.uuid)
        ref_submodels.update(_get_reference_submodels(project_uuid, model, visited))
    for submodel_uuid, submodel in ref_submodels.items():
        logger.info("Registering submodel %s", submodel.name)
        from_model_json.register_reference_submodel(submodel_uuid, submodel)

    # Load models
    models = {}
    _globals = {}
    for model_summary in project_summary.models:
        if model_summary.kind == ModelKind.MODEL:
            model = model_api.get_model(model_summary.uuid)
            init_scripts = model.configuration.workspace.init_scripts
            if len(init_scripts) > 1:
                raise NotImplementedError("Only one init script is supported")
            elif len(init_scripts) == 1 and init_scripts[0]:
                init_script_path = os.path.join(
                    project_dir, init_scripts[0]["file_name"]
                )
                if os.path.exists(init_script_path):
                    logger.info("Evaluating %s", init_scripts[0])
                    with open(init_script_path, "r") as f:
                        import numpy as np

                        _globals = {**globals(), "np": np}
                        exec(f.read(), _globals)
            if model.diagram.nodes:
                logger.info('Loading model "%s"', model.name)
                try:
                    models[model.name] = from_model_json.loads_model(
                        model.to_json(), namespace=_globals
                    )
                except BaseException as e:
                    logger.error(
                        "Failed to load model %s: %s", model.name, e, exc_info=True
                    )

    return Project(summary=project_summary, models=models, files=files)


def create_project(name: str) -> ProjectSummary:
    """
    Creates a new project with the given name.

    Args:
        name (str): The name of the project.

    Returns:
        ProjectSummary: The summary of the created project.
    """
    logger.info("Creating project %s...", name)
    response = api.call("/projects", "POST", body={"title": name})
    return _parse_project_summary(response)


def get_or_create_project(name: str) -> ProjectSummary:
    """
    Retrieves a project by its name or creates a new one if it doesn't exist.

    Args:
        name (str): The name of the project.

    Returns:
        ProjectSummary: The summary of the retrieved or created project.
    """
    try:
        return get_project_by_name(name).summary
    except api.CollimatorNotFoundError:
        return create_project(name)


def delete_project(project_uuid: str):
    """
    Deletes a project with the given UUID.

    Args:
        project_uuid (str): The UUID of the project to delete.
    """
    logger.info("Deleting project %s...", project_uuid)
    api.call(f"/projects/{project_uuid}", "DELETE")


def upload_file(project_uuid: str, name: str, fp: IO[AnyStr], overwrite=True):
    """
    Uploads a file to a project.

    Args:
        project_uuid (str): The UUID of the project.
        name (str): The name of the file.
        fp (IO[AnyStr]): The file pointer of the file to be uploaded.
        overwrite (bool, optional): Flag indicating whether to overwrite an existing file with the same name.
            Defaults to True.

    Returns:
        dict: A dictionary containing the summary of the uploaded file.

    Raises:
        api.CollimatorApiError: If the file upload fails.
    """

    mime_type, _ = mimetypes.guess_type(name)
    size = os.fstat(fp.fileno()).st_size

    logger.info(
        "Uploading file %s (type: %s, size: %d) to project %s...",
        name,
        mime_type,
        size,
        project_uuid,
    )
    body = {
        "name": name,
        "content_type": mime_type,
        "overwrite": overwrite,
        "size": size,
    }
    put_url_response = api.call(f"/projects/{project_uuid}/files", "POST", body=body)
    s3_presigned_url = put_url_response["put_presigned_url"]
    s3_response = requests.put(
        s3_presigned_url,
        headers={"Content-Type": mime_type},
        data=fp,
        verify=False,
    )
    if s3_response.status_code != 200:
        logging.error("s3 upload failed: %s", s3_response.text)
        raise api.CollimatorApiError(
            f"Failed to upload file {name} to project {project_uuid}"
        )
    file_uuid = put_url_response["summary"]["uuid"]
    process_response = api.call(
        f"/projects/{project_uuid}/files/{file_uuid}/process", "POST"
    )
    return process_response["summary"]


def upload_files(project_uuid: str, files: list[str], overwrite=True):
    """
    Uploads multiple files to a project.

    Args:
        project_uuid (str): The UUID of the project.
        files (list[str]): A list of file paths to be uploaded.
        overwrite (bool, optional): Flag indicating whether to overwrite existing files.
            Defaults to True.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for file in files:
            with open(file, "rb") as fp:
                futures.append(
                    executor.submit(
                        upload_file, project_uuid, os.path.basename(file), fp, overwrite
                    )
                )
        for future in concurrent.futures.as_completed(futures):
            future.result()
