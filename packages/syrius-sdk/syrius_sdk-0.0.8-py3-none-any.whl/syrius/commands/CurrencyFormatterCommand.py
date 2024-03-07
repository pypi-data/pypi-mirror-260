from syrius.commands.abstract import Command
from syrius.types import InputType


class CurrencyFormatterCommand(Command):
    id: int = 9
    quantity: InputType[str]
