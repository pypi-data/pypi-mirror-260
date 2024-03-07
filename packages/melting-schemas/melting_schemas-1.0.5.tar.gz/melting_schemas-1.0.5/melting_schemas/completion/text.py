from typing import TypedDict, Required


class TextModelSettings(TypedDict, total=False):
    """
    Change these settings to tweak the model's behavior.

    Heavily inspired by https://platform.openai.com/docs/api-reference/completions/create
    """

    model: Required[str]
    max_tokens: int  # defaults to inf
    temperature: float  # ValueRange(0, 2)
    top_p: float  # ValueRange(0, 1)
    logit_bias: dict[str, int]  # valmap(ValueRange(-100, 100))
    stop: list[str]  # MaxLen(4)
    n: int  # defaults to 1
