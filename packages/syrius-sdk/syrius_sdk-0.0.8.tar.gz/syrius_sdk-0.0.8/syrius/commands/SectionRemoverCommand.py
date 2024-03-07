from typing import Any

from syrius.commands.abstract import Command
from syrius.types import InputType


class SectionRemoverCommand(Command):
    id: int = 24
    words: InputType[list[dict[str, Any]]]
    text: InputType[str]