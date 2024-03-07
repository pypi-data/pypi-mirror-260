from typing import Any, Generic, TypeVar

from pydantic import GetJsonSchemaHandler, GetCoreSchemaHandler
from pydantic_core import core_schema, PydanticCustomError
from typing_extensions import get_args

from syrius.commands.abstract import Command, LocalCommand
from syrius.exceptions import SyriusTypeException


def check_inputs(inputs: Any) -> Any:
    if isinstance(inputs, dict):
        # must parse the entire dict to check if have some command or specific input on in
        input_validated = {}
        for key, value in inputs.items():
            input_validated[key] = check_inputs(value)
        return input_validated
    elif isinstance(inputs, list):
        input_validated = []
        for value in inputs:
            input_validated.append(check_inputs(value))
        return input_validated
    elif isinstance(inputs, str) or isinstance(inputs, int) or isinstance(inputs, bool) or isinstance(inputs, float):
        return inputs
    elif isinstance(inputs, Command) or isinstance(inputs, LocalCommand):
        return inputs
    else:
        raise SyriusTypeException()


T = TypeVar("T")


class InputType(Generic[T]):
    @classmethod
    def __get_pydantic_json_schema__(
            cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'format': 'input'})
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        tuple_result = get_args(source)
        item_tp = tuple_result[0]
        item_schema = handler.generate_schema(item_tp)
        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            core_schema.union_schema([
                item_schema,
                handler.generate_schema(Command)
            ])
        )
    @classmethod
    def _validate(cls, inputs: Any, _:Any) -> Any:
        try:
            value = check_inputs(inputs)
        except SyriusTypeException:
            raise PydanticCustomError('value_error', 'value is not a valid supported type')
        return value
