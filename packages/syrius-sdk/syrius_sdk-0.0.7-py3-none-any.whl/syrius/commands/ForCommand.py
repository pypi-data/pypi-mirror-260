from typing import List

from syrius.commands.abstract import Command, Loop, Logical, LocalCommand


class ForCommand(Loop):
    id: int = 1
    array: Command
    then: Command | List[Command] | Loop | Logical | LocalCommand
