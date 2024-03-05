import enum
from dataclasses import dataclass, field

__all__ = ["Tag", "EnvType", "AnnotationType", "Interaction", "Step", "StepType"]

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import pytz


class Tag(str, enum.Enum):
    """
    Namespace for useful tags that deepchecks case use
    You can use `dc_client.set_tag()` to pass user tags to deepchecks

    INPUT
        Relevant only for auto_collect=True, should contain the input as the user supply it

    INFORMATION_RETRIEVAL
        Relevant only for auto_collect=True, should contain the "information retrieval" if exist

    USER_ID
        The external user that used the AI model

    USER_INTERACTION_ID
        An unique id the user can set (in the context of a specific version), this id can be used later on
        to annotate the interaction, and also to find similar interactions cross-versions
        if USER_INTERACTION_ID was not supplied by the user, deepchecks will try to capture openai response id
        (i.e. - {"id": <openai unique id>, ...} and will set it as the "user_interaction_id" of the logged interaction
        elsewhere, deepchecks will generate a unique id for the interaction.
    """

    INPUT = "input"
    INFORMATION_RETRIEVAL = "information_retrieval"
    USER_ID = "user_id"
    USER_INTERACTION_ID = "user_interaction_id"


class EnvType(str, enum.Enum):
    PROD = "PROD"
    EVAL = "EVAL"


class AnnotationType(str, enum.Enum):
    GOOD = "good"
    BAD = "bad"
    UNKNOWN = "unknown"


@dataclass
class Interaction:
    user_interaction_id: str
    input: str
    information_retrieval: str
    full_prompt: str
    output: str
    topic: str
    output_properties: Dict[str, Any]
    input_properties: Dict[str, Any]
    custom_properties: Dict[str, Any]
    llm_properties: Dict[str, Any]
    llm_properties_reasons: Dict[str, Any]
    created_at: datetime


class StepType(str, enum.Enum):
    LLM = "LLM"
    INFORMATION_RETRIEVAL = "INFORMATION_RETRIEVAL"
    TRANSFORMATION = "TRANSFORMATION"
    FILTER = "FILTER"
    FINE_TUNING = "FINE_TUNING"
    PII_REMOVAL = "PII_REMOVAL"
    UDF = "UDF"


@dataclass
class Step:
    name: str
    type: StepType
    attributes: Dict[str, Any]
    started_at: datetime = field(default_factory=lambda: datetime.now(tz=pytz.UTC))
    annotation: Union[AnnotationType, None] = None
    finished_at: Union[datetime, None] = None
    input: Union[str, None] = None
    output: Union[str, None] = None
    error: Union[str, None] = None

    def to_json(self):
        return {
            "name": self.name,
            "annotation": self.annotation.value
            if self.annotation is not None
            else None,
            "type": self.type.value,
            "attributes": self.attributes,
            "started_at": self.started_at.astimezone().isoformat(),
            "finished_at": self.finished_at.astimezone().isoformat()
            if self.finished_at
            else None,
            "input": self.input,
            "output": self.output,
            "error": self.error,
        }

    @classmethod
    def as_jsonl(cls, steps):
        if steps is None:
            return None
        return [step.to_json() for step in steps]


@dataclass
class LogInteractionType:
    input: str
    output: str
    full_prompt: Union[str, None] = None
    annotation: Union[AnnotationType, None] = None
    user_interaction_id: Union[str, None] = None
    steps: Union[List[Step], None] = None
    custom_props: Union[Dict[str, Any], None] = None
    information_retrieval: Union[str, None] = None
    raw_json_data: Dict[str, Any] = None
    annotation_reason: Optional[str] = None
    started_at: Union[datetime, None] = None
    finished_at: Union[datetime, None] = None

    def to_json(self):
        data = {
            "input": self.input,
            "output": self.output,
            "full_prompt": self.full_prompt,
            "information_retrieval": self.information_retrieval,
            "annotation": self.annotation.value if self.annotation else None,
            "user_interaction_id": self.user_interaction_id,
            "steps": [step.to_json() for step in self.steps] if self.steps else None,
            "custom_props": self.custom_props,
            "raw_json_data": self.raw_json_data,
            "annotation_reason": self.annotation_reason,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
        }
        return data
