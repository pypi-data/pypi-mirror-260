from typing import Literal

from syrius.commands.abstract import Command
from syrius.types import InputType


class FileTextExtractCommand(Command):
    id: int = 5
    file_type: InputType[Literal["local", "s3"]]
    filepath: InputType[str]
    remove_breaks: InputType[bool]
    remove_multi_whitespaces: InputType[bool]