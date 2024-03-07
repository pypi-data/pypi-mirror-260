from typing import Any

from syrius.commands.abstract import Command
from syrius.types import InputType


class GrtCommand(Command):
    id: int = 7
    number: InputType[int]
    greater: InputType[int]
