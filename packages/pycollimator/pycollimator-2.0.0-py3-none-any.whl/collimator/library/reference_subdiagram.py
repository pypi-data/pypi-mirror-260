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

from typing import TYPE_CHECKING, Any, Callable

import numpy as np

from collimator import logging
from collimator.framework import InstanceParameter


if TYPE_CHECKING:
    from collimator.framework import Diagram


def eval_parameter(name: str, value: Any, call_site_namespace: dict, allow_empty=False):
    # Empty 'default_value' is allowed for submodel parameter defs and means None
    if allow_empty and (value == "" or value is None):
        return InstanceParameter(name=name, string_value="", evaluated_value=None)

    try:
        p = eval(str(value), globals(), call_site_namespace)
    except Exception as e:
        raise ValueError(
            f"Failed to evaluate parameter '{name}' with value '{value}': {e}"
        )
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
    return InstanceParameter(name=name, string_value=str(value), evaluated_value=p)


class ReferenceSubdiagram:
    # TODO: improve documentation here.
    _registry: dict[str, Callable[[Any], "Diagram"]] = {}
    _parameter_definitions: dict[str, list["ParameterDefinition"]] = {}  # noqa: F821

    @classmethod
    def create_diagram(
        cls,
        ref_id: str,
        *args,
        call_site_namespace: dict[str, Any] = None,
        instance_parameters: dict[str, Any] = None,
        **kwargs,
    ) -> "Diagram":
        """
        Create a diagram based on the given reference ID and parameters.

        Note that for submodels we evaluate all parameters, there is no
        "pure" string parameters.

        Args:
            ref_id (str): The reference ID of the diagram.
            *args: Variable length arguments.
            call_site_namespace (dict[str, Any], optional): The namespace of the call site. Defaults to None.
            instance_parameters (dict[str, Any], optional): The instance parameters for the diagram. Defaults to None.
                example: {"gain": 3.0}
            **kwargs: Keyword arguments.

        Returns:
            Diagram: The created diagram.

        Raises:
            ValueError: If the reference subdiagram with the given ref_id is not found.
        """
        if ref_id not in ReferenceSubdiagram._registry:
            raise ValueError(f"ReferenceSubdiagram with ref_id {ref_id} not found.")

        params_def = ReferenceSubdiagram.get_parameter_definitions(ref_id)
        params: dict[str, InstanceParameter] = {}
        if params_def:
            # compute values for all parameter 'definitions', i.e. the values
            # assigned at the submodel source.
            params = {
                p.name: eval_parameter(
                    p.name, p.default_value, call_site_namespace, allow_empty=True
                )
                for p in params_def
            }

        new_instance_parameters: dict[str, InstanceParameter] = {}
        if instance_parameters:
            # compute the value for any parameter 'modification', i.e. the values
            # at the submodel instance.
            # only evaluate for items whose namaes also appear in the 'definitions',
            # anything else is considered 'orphan parameter', and should not be made
            # available to the instance of the submodel.
            new_instance_parameters = {
                k: eval_parameter(k, v, call_site_namespace, allow_empty=False)
                for k, v in instance_parameters.items()
                if k in params
            }
            # override the 'definitions' values with any 'modified' values.
            params.update(new_instance_parameters)

        diagram = ReferenceSubdiagram._registry[ref_id](
            *args, parameters=params, **kwargs
        )

        diagram.ref_id = ref_id
        diagram.instance_parameters = new_instance_parameters
        return diagram

    @staticmethod
    def register(
        ref_id: str,
        constructor: Callable[[Any], "Diagram"],
        parameter_definitions: list["ParameterDefinition"] = None,  # noqa: F821
    ):
        logging.debug("Registering ReferenceSubdiagram with ref_id %s", ref_id)
        if ref_id in ReferenceSubdiagram._registry:
            logging.warning(
                "ReferenceSubdiagram with ref_id %s already registered.",
                ref_id,
            )
        ReferenceSubdiagram._registry[ref_id] = constructor
        ReferenceSubdiagram._parameter_definitions[ref_id] = parameter_definitions

    @staticmethod
    def get_parameter_definitions(
        ref_id: str,
    ) -> list["ParameterDefinition"]:  # noqa: F821
        if ref_id not in ReferenceSubdiagram._parameter_definitions:
            raise ValueError(f"ReferenceSubdiagram with ref_id {ref_id} not found.")
        return ReferenceSubdiagram._parameter_definitions[ref_id]
