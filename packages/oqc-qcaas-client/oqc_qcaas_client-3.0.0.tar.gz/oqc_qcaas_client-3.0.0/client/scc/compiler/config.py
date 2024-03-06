from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, is_dataclass
from enum import Enum, Flag, IntEnum, auto
from importlib import import_module
from json import JSONEncoder
from typing import List, Optional


# Set of common methods so we don't have to add/remove the custom serializer.
def json_dumps(*args, **kwargs):
    kwargs.setdefault("cls", CustomJSONEncoder)
    return json.dumps(*args, **kwargs)


def json_loads(*args, **kwargs):
    kwargs.setdefault("object_hook", _deserialize)
    return json.loads(*args, **kwargs)


def json_dump(*args, **kwargs):
    kwargs.setdefault("cls", CustomJSONEncoder)
    return json.dump(*args, **kwargs)


def json_load(*args, **kwargs):
    kwargs.setdefault("object_hook", _deserialize)
    return json.load(*args, **kwargs)


class CustomJSONEncoder(JSONEncoder):
    """
    It is a customised JSON encoder, which allows the serialization of
    the more complex objects. There are four major cases, based on the
    provided object to be serialized:

    - if the type of the object is supported by the default JSONEncoder,
      than the default method is used
    - if the class of the object is a dataclass, then the serialization
      will contain the name of the type, 'dataclass' flag in order to help
      at the deserialization, and the dictionary of the fields
    - if the object is none from the above, then the type name is saved,
      and the interior data using __dict__
    - if an exception is encountered from any cases from above
      (e.g. __dict__ is not available in case of complex numbers), then the
      type name is saved, and the data is the string representation of the
      object
    """

    def default(self, o):
        try:
            type_str = str(type(o))
            if is_dataclass(o):
                return {
                    "$type": type_str,
                    "$dataclass": True,
                    "$data": self.default(asdict(o)),
                }
            elif isinstance(o, Enum):
                typ = type(o)
                return {
                    "$type": f"<enum '{typ.__module__}.{typ.__name__}'>",
                    "$value": o.value,
                }
            elif hasattr(o, "__dict__"):
                return {
                    "$type": type_str,
                    "$data": {
                        key: self.default(value) for key, value in o.__dict__.items()
                    },
                }
            elif isinstance(o, complex):
                return {"$type": type_str, "$data": str(o)}
            elif isinstance(o, tuple):
                return {
                    "$type": type_str,
                    "$data": tuple(self.default(val) for val in o),
                }
        except (TypeError, AttributeError):
            pass

        return o


_type_name_matcher = r"<(?:class|enum) '((?:\w+\.)*)(\w+)'>"


def _get_type(s: str):
    match = re.match(_type_name_matcher, s)
    if match:
        namespace = match.group(1)
        if namespace != "":
            expanded_namespace = namespace[:-1].split(".")
            module_name = expanded_namespace.pop(0)
            imported_module = import_module(module_name)
            for item in expanded_namespace:
                module_name = f"{module_name}.{item}"
                try:
                    imported_module = getattr(imported_module, item)
                except AttributeError:
                    import_module(module_name)
                    imported_module = getattr(imported_module, item)
        else:
            imported_module = sys.modules["builtins"]
        try:
            return getattr(imported_module, match.group(2))
        except AttributeError:
            raise AttributeError(
                f"Class {s} not found in built-in modules or namespace '{namespace}'"
            )
    return None


def _deserialize(o):
    if not isinstance(o, dict) or "$type" not in o:
        return o

    typ = _get_type(o["$type"])
    if typ is None:
        return o

    if issubclass(typ, Enum):
        return typ(o["$value"])

    if issubclass(typ, tuple):
        return typ(o["$data"])

    if "$data" in o:
        data = o["$data"]
        if o.get("$dataclass", False):
            fields = _deserialize(data)
            return typ(**fields)
        elif isinstance(data, dict):
            obj = object.__new__(typ)
            obj.__dict__ = {key: _deserialize(value) for key, value in data.items()}
            return obj
        elif isinstance(data, str):
            return typ(data)
        else:
            return data

    return o


class InlineResultsProcessing(Flag):
    """
    Results transforms applied directly to the read-out value on the QPU.
    In most situations applied post-execution, but can also be interwoven.
    """

    # Raw readout from the QPU. Normally Z-axis values for each shot.
    Raw = auto()

    # Shot results averaged out to get a single 0/1 value for each qubit.
    Binary = auto()

    # Return the values in numpy arrays not Python lists.
    NumpyArrays = auto()

    Experiment = Raw | NumpyArrays
    Program = Binary

    def __repr__(self):
        return self.name


class ResultsFormatting(Flag):
    """ """

    # Transforms each shot into binary then counts the instances.
    # Example for two qubits: { '00': 15, '01': 2524, '10': 250, '11': 730 }
    BinaryCount = auto()

    # Change results value based on conditions for ease-of-use. Set as a flag because
    # it means that return values from execution may change format unexpectedly, so
    # should have a way to disable it for certain uses.
    DynamicStructureReturn = auto()

    # If your qubit results are lists of binary, squash to one string representation.
    # Changes 1: [1, 0, 0, 1] to 1: '1001'.
    # Only works when Binary format is returned.
    SquashBinaryResultArrays = auto()

    def __repr__(self):
        return self.name


class QuantumResultsFormat:
    def __init__(self):
        self.format: Optional[InlineResultsProcessing] = None
        self.transforms: Optional[
            ResultsFormatting
        ] = ResultsFormatting.DynamicStructureReturn

    def raw(self) -> QuantumResultsFormat:
        self.format = InlineResultsProcessing.Raw
        return self

    def binary(self) -> QuantumResultsFormat:
        self.format = InlineResultsProcessing.Binary
        return self

    def binary_count(self):
        """
        Returns a count of each instance of measured qubit registers.
        Switches result format to raw.
        """
        self.transforms = (
            ResultsFormatting.BinaryCount | ResultsFormatting.DynamicStructureReturn
        )
        self.format = InlineResultsProcessing.Raw
        return self

    def squash_binary_result_arrays(self):
        """
        Squashes binary result list into a singular bit string.
        Switches results to binary.
        """
        self.transforms = (
            ResultsFormatting.SquashBinaryResultArrays
            | ResultsFormatting.DynamicStructureReturn
        )
        self.format = InlineResultsProcessing.Binary
        return self

    def __contains__(self, other):
        if isinstance(other, ResultsFormatting):
            return self.transforms.__contains__(other)
        elif isinstance(other, InlineResultsProcessing):
            return self.format.__contains__(other)
        return False

    def __or__(self, other):
        if isinstance(other, ResultsFormatting):
            self.transforms = self.transforms.__or__(other)
        elif isinstance(other, InlineResultsProcessing):
            self.format = self.format.__or__(other)
        return self

    def __and__(self, other):
        if isinstance(other, ResultsFormatting):
            self.transforms = self.transforms.__and__(other)
        elif isinstance(other, InlineResultsProcessing):
            self.format = self.format.__and__(other)
        return self

    def __xor__(self, other):
        if isinstance(other, ResultsFormatting):
            self.transforms = self.transforms.__xor__(other)
        elif isinstance(other, InlineResultsProcessing):
            self.format = self.format.__xor__(other)
        return self

    def __repr__(self):
        return f"Format: {str(self.format)}. Transforms: {str(self.transforms)}."

    def __eq__(self, other):
        return self.format == other.format and self.transforms == other.transforms


class TketOptimizations(Flag):
    """Flags for the various Tket optimizations we can apply."""

    Empty = auto()
    DefaultMappingPass = auto()
    FullPeepholeOptimise = auto()
    ContextSimp = auto()
    DirectionalCXGates = auto()
    CliffordSimp = auto()
    DecomposeArbitrarilyControlledGates = auto()
    # EulerAngleReduction = auto()
    GlobalisePhasedX = auto()
    # GuidedPauliSimp = auto()
    KAKDecomposition = auto()
    # OptimisePhaseGadgets = auto()
    # PauliSimp = auto()
    # PauliSquash = auto()
    PeepholeOptimise2Q = auto()
    RemoveDiscarded = auto()
    RemoveBarriers = auto()
    RemoveRedundancies = auto()
    ThreeQubitSquash = auto()
    SimplifyMeasured = auto()

    One = DefaultMappingPass | DirectionalCXGates
    Two = One | FullPeepholeOptimise | ContextSimp


class QiskitOptimizations(Flag):
    """Flags for the various Qiskit optimizations we can apply."""

    Empty = auto()


class QatOptimizations(Flag):
    """Flags for the various Qat optimizations we can apply."""

    Empty = auto()


class MetricsType(Flag):
    Empty = auto()

    # Returns circuit after optimizations have been run.
    OptimizedCircuit = auto()

    # Count of transformed instructions after all forms of optimizations have
    # been performed.
    OptimizedInstructionCount = auto()

    # Set of basic metrics that should be returned at all times.
    Default = OptimizedCircuit | OptimizedInstructionCount

    def is_composite(self):
        """
        Any flags that are only composed of other ones should be signaled here. This
        is used for automatic metric generation and whether to build/validate this
        particular value.
        """
        return self == self.Default or self == self.Empty

    def snake_case_name(self):
        """
        Generate the Python field name that'll be used to hold the results of this
        metric.
        """
        name = self.name
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


class CompilerConfig:
    """
    Full settings for the compiler. All values are defaulted on initialization.

    If no explicit optimizations are passed then the default set of optimization for the
    language you're attempting to compile will be applied.
    """

    def __init__(
        self,
        repeats=None,
        repetition_period=None,
        results_format: QuantumResultsFormat = None,
        metrics=MetricsType.Default,
        active_calibrations=None,
        optimizations: "OptimizationConfig" = None,
    ):
        self.repeats: Optional[int] = repeats
        self.repetition_period: Optional = repetition_period
        self.results_format: QuantumResultsFormat = (
            results_format or QuantumResultsFormat()
        )
        self.metrics: MetricsType = metrics
        self.active_calibrations: List[CalibrationArguments] = active_calibrations or []
        self.optimizations: Optional[OptimizationConfig] = optimizations

    def to_json(self):
        return json_dumps(self)

    def from_json(self, json: str):
        vars(self).update(vars(json_loads(json)))
        return self

    @classmethod
    def create_from_json(cls, json: str):
        return CompilerConfig().from_json(json)


class CalibrationArguments:
    """Base class for individual calibration arguments."""

    def to_json(self):
        return json_dumps(self)

    def from_json(self, json: str):
        self.from_dict(json_loads(json))

    def _get_field_names(self):
        """Get existing field names for all attributes and properties"""
        existing_field_names = set(vars(self).keys())
        # Include class properties
        class_type = type(self)
        for prop in dir(class_type):
            if isinstance(getattr(class_type, prop), property):
                existing_field_names.add(prop)

        return existing_field_names

    def from_dict(self, dict_values):
        """Loads this dictionary into the arguments.
        Throws if key dosen't exist on the object."""

        valid_names = self._get_field_names()
        invalid_fields = [val for val in dict_values.keys() if val not in valid_names]
        if any(invalid_fields):
            raise ValueError(
                f"Field(s) {','.join(invalid_fields)} "
                f"are not valid for {self.__class__.__name__}."
            )

        vars(self).update(dict_values)


class Languages(IntEnum):
    Empty, Qasm2, Qasm3, QIR = range(4)

    def __repr__(self):
        return self.name


class OptimizationConfig:
    """
    Base class for instantiated optimizations as well as mix-in classes.
    Built this way so we can mix and match optimization objects across
    multiple setups and languages without duplication.
    """

    def __init__(self):
        super().__init__()

    def default(self):
        """Apply default set of optimizations to the current set."""
        return self

    def disable(self):
        """Disable all optimizations."""
        return self

    def minimum(self):
        """
        Apply minimum working set for current optimizations.
        """
        return self

    def __contains__(self, item):
        return False


class Tket(OptimizationConfig):
    def __init__(self, tket_optimization=None):
        super().__init__()
        self.tket_optimizations: TketOptimizations = TketOptimizations.Empty
        if tket_optimization is not None:
            self.tket_optimizations = tket_optimization

    def default(self):
        self.tket_optimizations = TketOptimizations.One
        return self

    def disable(self):
        self.tket_optimizations = TketOptimizations.Empty
        return self

    def minimum(self):
        self.tket_optimizations = TketOptimizations.DefaultMappingPass
        return self

    def __contains__(self, item):
        if isinstance(item, TketOptimizations) and item in self.tket_optimizations:
            return True
        return super().__contains__(item)


class Qiskit(OptimizationConfig):
    def __init__(self):
        super().__init__()
        self.qiskit_optimizations: QiskitOptimizations = QiskitOptimizations.Empty

    def default(self):
        self.qiskit_optimizations = QiskitOptimizations.Empty
        return self

    def __contains__(self, item):
        if isinstance(item, QiskitOptimizations) and item in self.qiskit_optimizations:
            return True
        return super().__contains__(item)


class Qasm2Optimizations(Tket, Qiskit):
    def __init__(self):
        super().__init__()
        self.default()

    def __repr__(self):
        return f"Qiskit: {self.qiskit_optimizations}. Tket: {self.tket_optimizations}."


class Qasm3Optimizations(OptimizationConfig):
    pass


class QIROptimizations(OptimizationConfig):
    pass


def get_optimizer_config(lang: Languages) -> Optional[OptimizationConfig]:
    """
    Returns the optimization config for this particular language. None if no valid ones
    found.
    """
    if lang == Languages.Qasm2:
        return Qasm2Optimizations()
    elif lang == Languages.Qasm3:
        return Qasm3Optimizations()
    elif lang == Languages.QIR:
        return QIROptimizations()
    return None


def get_config(lang: Languages, **kwargs):
    """
    Helper method to build a compiler config for a particular language.
    Forwards keywords to the CompilerConfig constructor.
    """
    config = CompilerConfig(**kwargs)
    config.optimizations = get_optimizer_config(lang)
    return config
