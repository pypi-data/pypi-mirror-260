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

from .generic import (
    SourceBlock,
    FeedthroughBlock,
    ReduceBlock,
)
from .primitives import (
    Abs,
    Adder,
    Chirp,
    Clock,
    Comparator,
    Constant,
    CrossProduct,
    DeadZone,
    Demultiplexer,
    DerivativeDiscrete,
    DiscreteClock,
    DiscreteInitializer,
    DotProduct,
    EdgeDetection,
    Exponent,
    FilterDiscrete,
    Gain,
    IfThenElse,
    Integrator,
    IntegratorDiscrete,
    IOPort,
    Logarithm,
    LogicalOperator,
    LogicalReducer,
    LookupTable1d,
    LookupTable2d,
    MatrixConcatenation,
    MatrixInversion,
    MatrixMultiplication,
    MatrixTransposition,
    MinMax,
    Multiplexer,
    Offset,
    PIDDiscrete,
    Power,
    Product,
    ProductOfElements,
    Pulse,
    Quantizer,
    Ramp,
    RateLimiter,
    Reciprocal,
    Relay,
    Saturate,
    Sawtooth,
    ScalarBroadcast,
    Sine,
    Slice,
    SquareRoot,
    Stack,
    Step,
    Stop,
    SumOfElements,
    Trigonometric,
    UnitDelay,
    ZeroOrderHold,
)
from .battery_cell import BatteryCell
from .custom import (
    CustomJaxBlock,
    CustomPythonBlock,
)
from .wrappers import (
    ode_block,
    feedthrough_block,
)
from .linear_system import (
    LTISystem,
    TransferFunction,
    linearize,
    PID,
    Derivative,
    LTISystemDiscrete,
    TransferFunctionDiscrete,
)

from .mpc import (
    LinearDiscreteTimeMPC,
    LinearDiscreteTimeMPC_OSQP,
)

from .nmpc import (
    DirectShootingNMPC,
    DirectTranscriptionNMPC,
    HermiteSimpsonNMPC,
)

from .lqr import (
    LinearQuadraticRegulator,
    DiscreteTimeLinearQuadraticRegulator,
    FiniteHorizonLinearQuadraticRegulator,
)

from .nn import (
    MLP,
    QuadraticCost,
)

from .fmu_import import (
    ModelicaFMU,
)

from .random import (
    RandomNumber,
    WhiteNoise,
)

from .rotations import (
    CoordinateRotation,
    CoordinateRotationConversion,
    RigidBody,
)

from .sindy import (
    ContinuousTimeSindyWithControl,
)

from .data_source import (
    DataSource,
)
from .state_machine import (
    StateMachine,
)

from .reference_subdiagram import ReferenceSubdiagram

__all__ = [
    "SourceBlock",
    "FeedthroughBlock",
    "ReduceBlock",
    "Abs",
    "Constant",
    "Sine",
    "BatteryCell",
    "Clock",
    "Comparator",
    "CoordinateRotation",
    "CoordinateRotationConversion",
    "CrossProduct",
    "CustomJaxBlock",
    "CustomPythonBlock",
    "DataSource",
    "DeadZone",
    "Derivative",
    "DerivativeDiscrete",
    "DiscreteInitializer",
    "DotProduct",
    "DiscreteClock",
    "EdgeDetection",
    "Exponent",
    "FilterDiscrete",
    "Gain",
    "IfThenElse",
    "Offset",
    "Reciprocal",
    "LogicalOperator",
    "LogicalReducer",
    "MatrixConcatenation",
    "MatrixInversion",
    "MatrixMultiplication",
    "MatrixTransposition",
    "ModelicaFMU",
    "MinMax",
    "Multiplexer",
    "Demultiplexer",
    "Adder",
    "PID",
    "Product",
    "ProductOfElements",
    "Power",
    "Integrator",
    "IntegratorDiscrete",
    "IOPort",
    "Logarithm",
    "LookupTable1d",
    "LookupTable2d",
    "Chirp",
    "Pulse",
    "Quantizer",
    "RandomNumber",
    "Relay",
    "RigidBody",
    "Sawtooth",
    "ScalarBroadcast",
    "ContinuousTimeSindyWithControl",
    "SumOfElements",
    "Slice",
    "StateMachine",
    "Stack",
    "Step",
    "Stop",
    "SquareRoot",
    "Ramp",
    "RateLimiter",
    "Saturate",
    "PIDDiscrete",
    "WhiteNoise",
    "ZeroOrderHold",
    "UnitDelay",
    "ode_block",
    "feedthrough_block",
    "LTISystem",
    "LTISystemDiscrete",
    "TransferFunction",
    "TransferFunctionDiscrete",
    "linearize",
    "LinearDiscreteTimeMPC",
    "LinearDiscreteTimeMPC_OSQP",
    "DirectShootingNMPC",
    "DirectTranscriptionNMPC",
    "HermiteSimpsonNMPC",
    "MLP",
    "QuadraticCost",
    "Trigonometric",
    "ReferenceSubdiagram",
    "LinearQuadraticRegulator",
    "DiscreteTimeLinearQuadraticRegulator",
    "FiniteHorizonLinearQuadraticRegulator",
]
