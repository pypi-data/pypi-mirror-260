from typing import Any, Literal, NotRequired, TypedDict


class Property(TypedDict):
    type: str
    description: str
    default: NotRequired[str]


class FunctionParameters(TypedDict):
    type: Literal["object"]
    properties: dict[str, Property]
    required: list[str]


class FunctionJSONSchema(TypedDict):
    name: str
    description: str
    parameters: dict[str, Any]  # FunctionParameters is incomplete
