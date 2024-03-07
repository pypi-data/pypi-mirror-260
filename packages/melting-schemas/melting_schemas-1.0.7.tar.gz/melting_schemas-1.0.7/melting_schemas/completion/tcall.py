import datetime
from typing import Literal, Optional, Required, TypedDict
from pydantic import BaseModel

from melting_schemas.meta import Creator

from ..completion.chat import ChatMLMessage, Templating

from ..json_schema import FunctionJSONSchema
from datetime import datetime
from pydantic import BaseModel, Field
from melting_schemas.utils import Timings, StreamTimings

from ..completion.chat import ChatModelSettings
from ..json_schema import FunctionJSONSchema
from ..meta import Creator


class TCallModelSettings(TypedDict, total=False):
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


class ToolCall(TypedDict):
    name: str  # MaxLen(64) TextMatch(r"^[a-zA-Z0-9_]*$")
    arguments: str


class ToolCallMLMessage(TypedDict):
    content: Optional[None]
    tool_call: list[ToolCall]
    role: Literal["assistant"]


class ToolMLMessage(TypedDict):
    content: str
    name: str
    role: Literal["tool"]


class ToolJSONSchema(TypedDict):
    type: Literal["function"]
    function: FunctionJSONSchema


class RawTCallRequest(BaseModel):
    tools: list[ToolJSONSchema]
    messages: list[ChatMLMessage | ToolCallMLMessage | ToolMLMessage]
    settings: TCallModelSettings

    class Config:
        smart_unions = True
        examples = {
            "Tool calling": {
                "tools": [
                    {
                        "type": "function",
                        "function": {
                            "name": "my_function",
                            "description": "This is my function",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "my_param": {
                                        "type": "string",
                                        "description": "This is my parameter",
                                    }
                                },
                                "required": ["my_param"],
                            },
                        },
                    }
                ],
                "messages": [
                    {
                        "content": "Hello",
                        "role": "user",
                    },
                    {
                        "content": "my_function",
                        "function_call": {
                            "name": "my_function",
                            "arguments": '{"my_param": "my_value"}',
                        },
                        "role": "assistant",
                    },
                ],
            }
        }


class TokenUsage(TypedDict):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class TCallCompletionCreationResponse(BaseModel):
    created_at: datetime
    created_by: Creator
    finish_reason: Literal["stop", "length", "function_call", "tool_calls"]
    id: str = Field(..., alias="_id")
    messages: list[ChatMLMessage | ToolCallMLMessage | ToolMLMessage]
    output: ChatMLMessage | ToolMLMessage | ToolCallMLMessage
    settings: ChatModelSettings
    templating: Optional[Templating]
    timings: Timings | StreamTimings
    usage: TokenUsage

    class Config:
        smart_unions = True
