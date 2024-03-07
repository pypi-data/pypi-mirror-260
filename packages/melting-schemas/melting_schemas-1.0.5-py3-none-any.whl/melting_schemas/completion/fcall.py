from datetime import datetime
from typing import Literal, NotRequired, Optional, Required, TypedDict, Type

from pydantic import BaseModel, Field
from melting_schemas.utils import Timings, StreamTimings

from ..completion.chat import ChatModelSettings
from ..json_schema import FunctionJSONSchema
from ..meta import Creator


class FCallModelSettings(TypedDict, total=False):
    """
    Change these settings to tweak the model's behavior.

    Heavily inspired by https://platform.openai.com/docs/api-reference/chat/create
    """

    model: Required[str]
    max_tokens: int  # defaults to inf
    temperature: float  # ValueRange(0, 2)
    top_p: float  # ValueRange(0, 1)
    frequency_penalty: float  # ValueRange(-2, 2) defaults to 0
    presence_penalty: float  # ValueRange(-2, 2) defaults to 0
    logit_bias: dict[str, int]  # valmap(ValueRange(-100, 100))
    stop: list[str]  # MaxLen(4)


class FunctionCall(TypedDict):
    name: str  # MaxLen(64) TextMatch(r"^[a-zA-Z0-9_]*$")
    arguments: str


class FunctionCallMLMessage(TypedDict):
    content: Optional[None]
    function_call: FunctionCall
    role: Literal["assistant"]


class FunctionMLMessage(TypedDict):
    content: str
    name: str
    role: Literal["function"]


class ChatMLMessage(TypedDict):
    content: str
    name: NotRequired[str]
    role: Literal["user", "assistant", "system"]


class RawFCallRequest(BaseModel):
    functions: list[FunctionJSONSchema]
    messages: list[ChatMLMessage | FunctionCallMLMessage | FunctionMLMessage]
    settings: FCallModelSettings

    class Config:
        smart_unions = True
        examples = {
            "Function calling": {
                "value": {
                    "messages": [
                        {
                            "content": "What is the weather like in Boston?",
                            "role": "user",
                        },
                    ],
                    "functions": [
                        {
                            "name": "get_current_weather",
                            "description": "Get the current weather in a given location",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "location": {
                                        "type": "string",
                                        "description": "The city and state, e.g. San Francisco, CA",
                                    },
                                },
                                "required": ["location"],
                            },
                        }
                    ],
                    "settings": {"model": "gpt-3.5-turbo-0613"},
                },
            },
            "Function completion": {
                "value": {
                    "messages": [
                        {
                            "content": "What is the weather like in Boston?",
                            "role": "user",
                        },
                        {
                            "content": None,
                            "function_call": {
                                "name": "get_current_weather",
                                "arguments": '{"location": "Boston, MA"}',
                            },
                            "role": "assistant",
                        },
                        {
                            "content": '{"temperature": "22", "unit": "celsius", "description": "Sunny"}',
                            "name": "get_current_weather",
                            "role": "function",
                        },
                    ],
                    "functions": [
                        {
                            "name": "get_current_weather",
                            "description": "Get the current weather in a given location",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "location": {
                                        "type": "string",
                                        "description": "The city and state, e.g. San Francisco, CA",
                                    },
                                },
                                "required": ["location"],
                            },
                        }
                    ],
                    "settings": {"model": "gpt-3.5-turbo-0613"},
                },
            },
        }


class TokenUsage(TypedDict):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class TemplateInputs(TypedDict):
    inputs: dict[str, str]
    name: NotRequired[str]
    role: Literal["user", "system"]
    # advanced usage: select sub-templates
    template_name: NotRequired[str]


class Templating(BaseModel):
    prompt_inputs: list[TemplateInputs]
    prompt_id: str
    prompt_name: str


class FCallCompletionCreationResponse(BaseModel):
    created_at: datetime
    created_by: Creator
    finish_reason: Literal["stop", "length", "function_call"]
    id: str = Field(..., alias="_id")
    messages: list[
        ChatMLMessage
        | FunctionCallMLMessage
        | FunctionMLMessage
        # | ToolCallMLMessage
        # | ToolMLMessage
    ]
    output: ChatMLMessage | FunctionCallMLMessage | FunctionMLMessage
    settings: ChatModelSettings
    templating: Optional[Templating]
    timings: Timings | StreamTimings
    usage: TokenUsage

    class Config:
        smart_unions = True


class PluginStreamedResponse(BaseModel):
    op_type: Literal["step", "result", "start", "stop", "execution_id"]
    plugin_name: Optional[str] = None
    method: Optional[str] = None
    content: str


class StartPluginStreamedResponse(PluginStreamedResponse):
    params: dict
    selection_id: Optional[str] = None


class StopPluginStreamedResponse(PluginStreamedResponse):
    response_time: str
    error: str
