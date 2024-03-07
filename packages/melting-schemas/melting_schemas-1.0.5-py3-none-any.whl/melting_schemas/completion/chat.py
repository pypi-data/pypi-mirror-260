from datetime import datetime
from typing import Literal, NotRequired, Optional, Required, TypedDict

from pydantic import BaseModel, Field

from melting_schemas.utils import StreamTimings, Timings

from ..meta import Creator


class ChatMLMessage(TypedDict):
    content: str
    name: NotRequired[Optional[str]]  # MaxLen(64) TextMatch(r"^[a-zA-Z0-9_]*$")
    role: Literal["user", "assistant", "system"]


class ChatModelSettings(TypedDict, total=False):
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
    logit_bias: dict[int, int]  # valmap(ValueRange(-100, 100))
    stop: list[str]  # MaxLen(4)


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


class Templating(TypedDict):
    prompt_inputs: list[TemplateInputs | dict]
    prompt_id: str
    prompt_name: str


class ChatCompletionCreationResponse(BaseModel):
    created_at: datetime
    created_by: Creator
    finish_reason: Literal["stop", "length"]
    id: str = Field(..., alias="_id")
    messages: list[ChatMLMessage]
    output: ChatMLMessage
    settings: ChatModelSettings
    templating: Optional[Templating]
    timings: Timings | StreamTimings
    usage: TokenUsage


class StreamedChatCompletionCreationResponse(BaseModel):
    finish_reason: Optional[Literal["stop", "length"]]
    delta: str
    acc_usage: TokenUsage


class RawChatCompletionRequest(BaseModel):
    history: str | None = None
    messages: list[ChatMLMessage]
    settings: ChatModelSettings

    class Config:
        examples = {
            "Raw": {
                "value": {
                    "messages": [
                        {"content": "You are a helpful chatbot.", "role": "system"},
                        {"content": "What does bequeath mean?", "role": "user"},
                    ],
                    "settings": {"model": "openai/gpt-3.5-turbo-1106"},
                }
            },
            "Named raw": {
                "value": {
                    "messages": [
                        {"content": "You are a helpful chatbot.", "role": "system"},
                        {
                            "content": "What does my name mean?",
                            "name": "John",
                            "role": "user",
                        },
                    ],
                    "settings": {"model": "openai/gpt-4-0613"},
                },
            },
        }


class ChatCompletionRequest(BaseModel):
    history: str | None = None
    prompt_inputs: list[TemplateInputs]
    prompt_name: str
    settings: Optional[ChatModelSettings] = None

    class Config:
        examples = {
            "Prompted": {
                "value": {
                    "prompt_inputs": [
                        {"role": "system", "inputs": {"now": str(datetime.now())}},
                        {"role": "user", "inputs": {"text": "What day is today?"}},
                    ],
                    "prompt_name": "teia.example.1",
                },
            },
            "Many templates": {
                "value": {
                    "prompt_inputs": [
                        {
                            "role": "system",
                            "inputs": {"plugin_data": "Secret number is 42"},
                            "template_name": "plugin_prompt",
                        },
                        {
                            "role": "user",
                            "inputs": {"question": "What is the secret number???"},
                            "template_name": "user_prompt",
                        },
                    ],
                    "prompt_name": "teia.example.2",
                },
            },
        }


class HybridChatCompletionRequest(BaseModel):
    history: str | None = None
    prompt_name: str
    messages: list[ChatMLMessage | TemplateInputs]
    settings: Optional[ChatModelSettings] = None

    class Config:
        examples = {
            "Hybrid": {
                "value": {
                    "messages": [
                        {"content": "You are a helpful chatbot.", "role": "system"},
                        {"role": "user", "inputs": {"text": "What day is today?"}},
                    ],
                    "prompt_name": "teia.example.1",
                },
            }
        }
