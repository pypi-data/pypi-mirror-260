from typing import Any

from syrius.commands.abstract import Command
from syrius.types import InputType


class TemplateCommand(Command):
    id: int = 21
    variables: InputType[dict[str, str | int | list[Any] | dict[str, Any]]]
    text: InputType[str]