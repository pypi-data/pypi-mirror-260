# syrius/commands/abstract.py

"""Provide abstract class and base classes for Command, Loop and Logical.

The module contains the following classes:

- `AbstractCommand` - Abstract Class for Command, Loop and Logical.
- `Command` - Parent class for Commands.
- `Loop` - Parent class for Loops commands.
- `Logical` - Parent class for Logical commands.
"""
import uuid
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class LocalCommand(BaseModel):

    def run(self):
        raise Exception("Not implemented")


class AbstractCommand(BaseModel):
    """Abstract Class for Commands
    Attributes:
        id: define the unique identifier of the command or loop or logical
        type: Literal that identify the Command type, the accepted values are: Command, Loop, Logical
        ref: the unique reference number ( UUID ) of the command or loop or logical
    """
    model_config = ConfigDict(extra='allow')
    id: int = 0
    type: Literal["Command", "Loop", "Logical"]
    ref: str = Field(default_factory=lambda: str(uuid.uuid4().hex))


class Command(AbstractCommand):
    """Command parent class

    That class is the parent class for all the commands

    """
    type: Literal["Command", "Loop", "Logical"] = "Command"


class Loop(AbstractCommand):
    """Loop parent class

    That class is the parent class for all the Loop Commands

    """
    type: Literal["Command", "Loop", "Logical"] = "Loop"


class Logical(AbstractCommand):
    """Logical parent class

    That class is the parent class for all the Logical Commands

    """
    type: Literal["Command", "Loop", "Logical"] = "Logical"
