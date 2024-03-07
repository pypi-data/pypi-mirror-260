"""
There are good reasons the package has separate schemas from the rest of the app
1. We don't necessarily want to expose the underlying schema
2. The package requires quite different objects - notably all input parameters need to be defined in the app parameter
"""

from typing import List, Union, Any, Optional, Literal
import uuid
import enum
import json
from dataclasses import dataclass, asdict


################################
# Exceptions
################################
class ComposoException(Exception):
    pass


class ComposoUserException(ComposoException):
    pass


class ComposoCriticalException(ComposoException):
    pass


class ComposoDeveloperException(ComposoException):
    pass


################################
# Types
################################
################################
# PACKAGE TYPES
################################
class ParameterType(str, enum.Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    MULTICHOICESTRING = "MULTICHOICESTRING"
    CONVERSATIONHISTORY = "CONVERSATIONHISTORY"


class NativeType(str, enum.Enum):
    STR = "str"
    INT = "int"
    FLOAT = "float"


@dataclass
class FixedParameter:
    name: str
    is_kwarg: bool
    live_working_value: Any


@dataclass
class ParameterBase:
    name: str
    is_kwarg: bool
    demo_value: Any = None
    description: Optional[str] = None
    kwarg_value: Optional[Any] = None

    param_type: ParameterType = None

    def validate(self, item):
        return item

    def cast(self, item):
        return item


@dataclass
class StrParam(ParameterBase):
    param_type: Literal[ParameterType.STRING] = ParameterType.STRING

    def __init__(self, description=None):
        self.description = description

    def cast(self, value):
        return str(value)


@dataclass
class IntParam(ParameterBase):
    param_type: Literal[ParameterType.INTEGER] = ParameterType.INTEGER

    allowableMin: Optional[int] = None
    allowableMax: Optional[int] = None

    def __init__(self, description=None, min=None, max=None):
        # Create an instance of the IntParam class
        self.description = description

        self.allowableMin: int = min
        self.allowableMax: int = max

    def validate(self, value):
        if self.allowableMin and not value >= self.allowableMin:
            raise ComposoUserException(
                f"Parameter is invalid. Value {value} does not exceed minimum value: {self.allowableMin}"
            )

        if self.allowableMax and not value <= self.allowableMax:
            raise ComposoUserException(
                f"Parameter is invalid. Value {value} exceeds maximum value: {self.allowableMax}"
            )

        return value

    def cast(self, item):
        return int(item)


@dataclass
class FloatParam(ParameterBase):
    param_type: Literal[ParameterType.FLOAT] = ParameterType.FLOAT

    allowableMin: Optional[float] = None
    allowableMax: Optional[float] = None

    def __init__(self, description=None, min=None, max=None):
        self.description = description

        self.allowableMin: float = min
        self.allowableMax: float = max

    def validate(self, value):
        if self.allowableMin and not value >= self.allowableMin:
            raise ComposoUserException(
                f"Parameter is invalid. Value {value} does not exceed minimum value: {self.allowableMin}"
            )

        if self.allowableMax and not value <= self.allowableMax:
            raise ComposoUserException(
                f"Parameter is invalid. Value {value} exceeds maximum value: {self.allowableMax}"
            )

        return value

    def cast(self, item):
        return float(item)


@dataclass
class MultiChoiceStrParam(ParameterBase):
    param_type: Literal[ParameterType.MULTICHOICESTRING] = (
        ParameterType.MULTICHOICESTRING
    )
    choices: List[str] = None

    def __init__(self, choices: List[str] = None, description=None):
        self.description = description
        self.choices = choices

    def validate(self, value):
        if self.choices is not None:
            if value not in self.choices:
                raise ComposoUserException(
                    f"Parameter is invalid. Value {value} is not in the list of allowable values: {self.choices}"
                )

        return value

    def cast(self, item):
        return str(item)


@dataclass
class ConversationHistoryParam(ParameterBase):
    param_type: Literal[ParameterType.CONVERSATIONHISTORY] = (
        ParameterType.CONVERSATIONHISTORY
    )

    def __init__(self, description=None):
        self.description = description

    def validate(self, value):
        if not isinstance(value, list):
            raise ComposoUserException(
                f"ConversationHistoryParam is invalid. Must be a list"
            )
        if not all(isinstance(item, dict) for item in value):
            raise ComposoUserException(
                f"ConversationHistoryParam is invalid. Must be a list of dicts"
            )
        return value

    def cast(self, item):
        return item


WORKABLE_TYPES = Union[
    StrParam, IntParam, FloatParam, MultiChoiceStrParam, ConversationHistoryParam
]


@dataclass
class CaseTrigger:
    case_id: uuid.UUID
    vars: dict


@dataclass
class RunTrigger:
    run_id: uuid.UUID
    cases: List[CaseTrigger]


@dataclass
class AppDeletionEvent:
    message: str
    obj_type: str = "app_deletion"


@dataclass
class PollResponse:
    registered_apps: List[uuid.UUID]
    payload: Union[None, RunTrigger, AppDeletionEvent] = None


@dataclass
class CaseResult:
    case_id: uuid.UUID
    value: Optional[Any] = None
    error: Optional[str] = None
    output_stream_incomplete: bool = False

    @staticmethod
    def is_jsonable(x):
        try:
            json.dumps(x)
            return True
        except:
            return False

    def __post_init__(self):
        if self.value is not None and not self.is_jsonable(self.value):
            self.value = None
            self.error = "The app's return value was not jsonable"


@dataclass
class RunResult:
    run_id: uuid.UUID
    results: Optional[List[CaseResult]] = None
    error: Optional[str] = None


@dataclass
class AppRegistration:
    api_key: str
    runner_type: Literal["python", "golang"]
    runner_version: str
    raw_name: str
    parameters: List[WORKABLE_TYPES]
    docstring: Optional[str] = None
