from typing import Any

from syrius.commands.abstract import Command
from syrius.types import InputType


class OpenAICompletionCommand(Command):
    id: int = 18
    messages: InputType[list[dict[str, str]]]
    api_key: InputType[str]
    model: InputType[str]
    temperature: InputType[float]
    tools: dict[str, Any]
    extract: str
