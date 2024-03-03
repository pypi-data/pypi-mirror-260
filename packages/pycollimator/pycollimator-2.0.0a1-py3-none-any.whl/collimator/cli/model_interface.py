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

import glob
import json
import os
import warnings
from typing import TYPE_CHECKING

import numpy as np

from collimator import logging
from collimator.dashboard.serialization import (
    binary_results,
    model_json,
    from_model_json,
    ui_types,
)
from collimator.dashboard.serialization.time_mode import time_mode_node, time_mode_port
from ..framework import Diagram, IntegerTime, SystemBase
from ..simulation import SimulatorOptions, simulate

if TYPE_CHECKING:
    from ..framework import ContextBase
    from ..backend.typing import Array

__all__ = [
    "load_model",
]


def load_model(
    modeldir: str,
    model: str = "model.json",
    datadir: str = None,
    logsdir: str = None,
    npydir: str = None,
    block_overrides=None,
) -> AppInterface:
    # register reference submodels
    file_pattern = os.path.join(modeldir, "submodel-*-latest.json")
    submodel_files = glob.glob(file_pattern)
    for submodel_file in submodel_files:
        ref_id = os.path.basename(submodel_file).split("-")[1:-1]
        ref_id = "-".join(ref_id)
        with open(submodel_file, "r", encoding="utf-8") as f:
            submodel = model_json.Model.from_json(f)
            from_model_json.register_reference_submodel(ref_id, submodel)

    with open(os.path.join(modeldir, model), "r", encoding="utf-8") as f:
        model = model_json.Model.from_json(f)

    return AppInterface(
        model,
        datadir=datadir,
        logsdir=logsdir,
        npydir=npydir,
        block_overrides=block_overrides,
    )


def get_signal_types(
    namepath: list[str],
    uuidpath: list[str],
    signal_type_nodes: list[ui_types.Node],
    nodes: list[SystemBase],
    context: ContextBase,
    dep_graph,
):
    # iterate over the nested diagram and:
    #   1] determine each signal's dtype and dimension
    #   2] determine time_mode of nodes and signals
    #   3] generate the signal_types.json given to the frontend

    nodes_tm = []
    for node in nodes:
        blk_namepath = namepath + [node.name]
        blk_uuidpath = uuidpath + [node.ui_id]
        ports = []

        if isinstance(node, Diagram):
            signal_type_nodes, subdiagram_tm = get_signal_types(
                blk_namepath,
                blk_uuidpath,
                signal_type_nodes,
                node.nodes,
                context,
                dep_graph,
            )

        ports_tm = []
        for port_idx, out_port in enumerate(node.output_ports):
            val = out_port.eval(context)

            tm = time_mode_port(out_port)
            ports_tm.append(tm)

            # jp's trick. 'val' may have a Python type (int or float) in which
            # case it doesn't have a dtype. So turn it into an array and then
            # retrive the dtype. While a Python type doesn't have a dtype,
            # for some reason one can apply np.shape(..) to it. Go figure.

            # this data is returned to the UI
            port = ui_types.Port(
                index=port_idx,
                dtype=str(np.array(val).dtype),
                dimension=np.shape(val),
                time_mode=tm,
                discrete_interval=None,
                name=node.output_ports[port_idx].name,
            )
            ports.append(port.__dict__)

        # node time mode
        if isinstance(node, Diagram):
            node_tm = subdiagram_tm
        else:
            node_tm = time_mode_node(node, ports_tm)

        nodes_tm.append(node_tm)

        # this data is returned to the UI
        nd = ui_types.Node(
            namepath=blk_namepath,
            uuidpath=blk_uuidpath,
            outports=ports,
            time_mode=node_tm,
            discrete_interval=None,
        )
        signal_type_nodes.append(nd.__dict__)

    # diagram time mode
    diagram_tm = time_mode_node(node, nodes_tm)

    return signal_type_nodes, diagram_tm


class AppInterface:
    def __init__(
        self,
        model: model_json.Model,
        datadir: str = None,
        logsdir: str = None,
        npydir: str = None,
        block_overrides: dict[str, SystemBase] = None,
    ):
        self.context: ContextBase = None
        self.model = model
        self.block_overrides = block_overrides
        self.datadir = datadir
        self.logsdir = logsdir
        self.npydir = npydir

        # track whether "check" method has been run on this system
        self.static_analysis_complete = False

        # called here to maintain behavior expected by some tests,
        # i.e. some data created in statatic analysis is made available
        # in the object after only calling __init__.
        self.check()

    def check(self):
        # execute the all static analysis operations, raising errors/warnings
        # as appropriate.
        root_id = "root"

        # evaluate model params
        model_parameters = from_model_json.eval_parameters(
            default_parameters=self.model.parameter_definitions,
            instance_parameters=self.model.parameters,
            name_path=[],
            ui_id_path=[],
        )

        # evaluate model initialization script
        if self.model.configuration.workspace:
            # if it's not an empty dict, it should have ref to initscript
            # @am. this is not great but works for now.
            if self.model.configuration.workspace.init_scripts:
                filename = self.model.configuration.workspace.init_scripts[0][
                    "file_name"
                ]
                model_parameters = from_model_json.eval_init_script(
                    filename,
                    model_parameters,
                    name_path=[],
                    ui_id_path=[],
                )

        recorded_signals = {}

        # process and validate simulation and results settings
        (
            self.results_options,
            self.simulator_options,
        ) = from_model_json.simulation_settings(
            self.model.configuration, recorded_signals=recorded_signals
        )

        # build the model.
        # this step runs checks for:
        #   1] all inports connected
        #   2] no inports connected to multiple sources
        #   3] no algebraic loops
        #   4] all block "validate" functions
        self.diagram = from_model_json.make_subdiagram(
            root_id,
            self.model.diagram,
            self.model.subdiagrams,
            self.model.state_machines,
            ui_id=self.model.uuid,
            parent_path=[],
            parent_ui_id_path=[],
            namespace_params=model_parameters,
            block_overrides=self.block_overrides,
            global_discrete_interval=self.model.configuration.sample_time,
            record_mode=self.model.configuration.record_mode,
            recorded_signals=recorded_signals,
            start_time=float(self.model.configuration.start_time),
        )

        # TODO: ensure no top level inports/outports

        # initialized context and verify internal consistency
        try:
            self.context = self.diagram.create_context()
            logging.debug("Context created")

            # Most type errors will be caught when the context is created above.
            # See collimator.framework.context_factory._check_types. However, it
            # won't catch errors when there is a mismatch between an input type and
            # the state in stateful blocks. The call to check_types does that.
            self.diagram.check_types(self.context)
        except Exception as exc:
            # try / catch here only to provide a breakpoint site for inspection
            # from within the debugger. This may also become the site where
            # chained exceptions are parsed and normalized.
            raise exc

        # Write 'signal_types.json'
        if self.logsdir is not None:
            try:
                os.makedirs(self.logsdir, exist_ok=True)
                context = self.context
                signal_type_nodes, _root_tm = get_signal_types(
                    namepath=[],
                    uuidpath=[],
                    signal_type_nodes=[],
                    nodes=self.diagram.nodes,
                    context=context,
                    dep_graph=self.diagram._dependency_graph,
                )

                # signal types json to be returned to UI
                signal_types_file = os.path.join(self.logsdir, "signal_types.json")
                signal_types = ui_types.SignalTypes(nodes=signal_type_nodes)
                signal_types_dict = signal_types.to_api(omit_none=True)
                with open(signal_types_file, "w", encoding="utf-8") as outfile:
                    json.dump(signal_types_dict, outfile, indent=2, sort_keys=False)

            except Exception as exc:
                warnings.warn(
                    f"Failed to generate signal_types.json due to exception: {exc}."
                )

        # TODO: Write 'time_mode.json'

        self.static_analysis_complete = True

    def simulate(
        self,
        t=None,
        write_binary_results=False,
        record_outputs=True,
        simulator_options: SimulatorOptions = None,
    ) -> dict[str, Array]:
        if not self.static_analysis_complete:
            self.check()

        if t is None:
            t = self.model.configuration.stop_time

        start_time = float(self.model.configuration.start_time)

        options = self.simulator_options
        if simulator_options is not None:
            options = simulator_options

        # Usually the default integer time scale will work (up to ~0.3 years), but if
        # a longer simulation was requested, we need to use a larger integer time scale.
        # Note that this is also configurable via SimulatorOptions, but this is a more
        # robust automatic solution (though not amenable to JAX tracing).
        while float(t) > IntegerTime.max_float_time:
            IntegerTime.set_scale(1000 * IntegerTime.time_scale)
            logging.info(
                "Increasing integer time scale by a factor of 1000x to allow for "
                "representation of the specified end time."
            )

        print("Beginning simulation")

        results = simulate(
            self.diagram,
            self.context,
            (start_time, float(t)),
            options=options,
            results_options=self.results_options,
            recorded_signals=options.recorded_signals,
        )

        # Calls to model.simulate are expecting a dict of outputs including time.
        results.outputs["time"] = results.time

        if write_binary_results:
            if self.datadir is None:
                raise Exception("cannnot write binary results when datadir is None")
            binary_results.write_binary_results_f(
                results.outputs, self.datadir, self.logsdir
            )

        if self.npydir is not None:
            for name, val in results.outputs.items():
                if val is None:
                    logging.error(f"Output '{name}' is None, not writing npy file")
                    continue
                with open(os.path.join(self.npydir, f"{name}.npy"), "wb") as f:
                    np.lib.format.write_array(f, val, allow_pickle=False)
        else:
            logging.warning("npydir is None, not writing npy files")

        return results.outputs
