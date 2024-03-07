from enum import Enum

from prompts import DynamicSchema, PromptRole, Template, TurboSchema
from prompts.schemas import TurboSchema
from pydantic import BaseModel, Field

from melting_schemas.completion.chat import ChatModelSettings
from melting_schemas.meta import Creator

# ====== Create Schemas ======


class ChatPromptTemplate(TurboSchema):
    settings: ChatModelSettings

    class Config:
        examples = {
            "Minimal Prompt Template": {
                "value": {
                    "assistant_templates": "<text>",
                    "description": "Single of its kind, example app, teia org.",
                    "name": "teia.example_app.single.example01",
                    "system_templates": "<text>",
                    "user_templates": "<text>",
                    "settings": {"model": "gpt-3.5-turbo"},
                }
            },
            "Time-aware Prompt Template": {
                "value": {
                    "assistant_templates": "<text>",
                    "description": "Single of its kind, example app, teia org.",
                    "name": "teia.example.1",
                    "system_templates": "Current timestamp: <now>\nYou are a helpful chatbot.",
                    "user_templates": "<text>",
                    "settings": {
                        "model": "gpt-3.5-turbo",
                    },
                }
            },
            "Many Templates": {
                "value": {
                    "name": "teia.example.2",
                    "description": "A development example.",
                    "settings": {
                        "model": "gpt-3.5-turbo",
                        "max_tokens": 200,
                        "temperature": 0.25,
                    },
                    "system_templates": [
                        {"template_name": "plugin_prompt", "template": "<plugin_data>"},
                    ],
                    "user_templates": [
                        {"template_name": "user_prompt", "template": "<question>"}
                    ],
                    "assistant_templates": [
                        {"template_name": "assistant_prompt", "template": "<message>"}
                    ],
                }
            },
        }


class CreateCompletionPrompt(DynamicSchema):
    pass


# ====== Get Schemas ======


class GeneratedFields(BaseModel):
    created_at: str
    created_by: Creator
    id: str = Field(alias="_id")


class ChatPrompt(GeneratedFields, TurboSchema):
    pass


class GetCompletionPrompt(GeneratedFields, DynamicSchema):
    pass
