import concurrent.futures
import json
from collections import deque
from copy import deepcopy
from time import sleep
from typing import Any, List, Dict, Callable
from zlib import adler32

from syrius.api import SyriusAPI
from syrius.commands.abstract import Command, Loop, Logical, LocalCommand


def _check_if_is_a_command(element: Any) -> bool:
    if isinstance(element, Command) and element.type == "Command":
        return True
    return False


def _check_if_is_a_local_command(element: Any) -> bool:
    if isinstance(element, LocalCommand):
        return True
    return False


def _check_if_is_a_loop(element: Any) -> bool:
    if isinstance(element, Loop) and element.type == "Loop":
        return True
    return False


def _check_if_is_a_logical(element: Any) -> bool:
    if isinstance(element, Logical) and element.type == "Logical":
        return True
    return False


def _check_if_is_a_list(element) -> bool:
    if isinstance(element, list):
        return True
    return False


def _check_if_is_a_dict(element) -> bool:
    if isinstance(element, dict):
        return True
    return False


def _extract_input_fields(element: Command):
    attributes = []
    json_schema = element.model_json_schema()
    for name_attribute, value_attribute in json_schema['properties'].items():
        if "format" in value_attribute and value_attribute["format"] == "input":
            attributes.append(name_attribute)
    return attributes


def _get_attribute_value(attribute_name: str, command: Command) -> Any:
    return getattr(command, attribute_name)


class TreeTraverse:
    _execute_list_of_commands: list[str]
    _selected_command: Command | None

    def __init__(self, list_to_traverse: list[Any]):
        self._list_to_traverse = list_to_traverse
        self._execute_list_of_commands = []
        self._selected_command = None

    def _traverse(self, value: dict | list | Command | Loop) -> list[Command] | None:
        if _check_if_is_a_command(value):
            command = self._traverse_a_command(value)
            return command
        elif _check_if_is_a_loop(value):
            result_values = []
            loop_array = value.array
            then_array = value.then
            command = self._traverse(loop_array)
            then_command = self._traverse(then_array)
            value.then = then_command
            result_values.extend(command)
            result_values.append(value)
            return result_values
        elif _check_if_is_a_logical(value):
            result_values = []
            condition = value.condition
            then_command = value.then
            command = self._traverse(condition)
            then_command = self._traverse(then_command)
            value.then = then_command
            result_values.extend(command)
            result_values.append(value)
            return result_values
        elif isinstance(value, list):
            return self._traverse_a_list(value)
        elif isinstance(value, dict):
            return self._traverse_a_dict(value)
        return None

    def _traverse_a_dict(self, dict_to_traverse: dict[str, Any]):
        ending_list = []
        for key, value in dict_to_traverse.items():
            result = self._traverse(value)
            if result is not None:
                ending_list.extend(result)
        return ending_list

    def _traverse_a_list(self, list_to_traverse: list[Any]):
        ending_list = []
        for element in list_to_traverse:
            result = self._traverse(element)
            if result is not None:
                ending_list.extend(result)
        return ending_list

    def _traverse_a_command(self, command: Command):
        result_values = []
        if command.ref not in self._execute_list_of_commands:
            list_of_inputs_attributes = _extract_input_fields(command)
            inputs_values: list[Any] = []
            for input_attribute_name in list_of_inputs_attributes:
                value_of_attribute = _get_attribute_value(input_attribute_name, command)
                inputs_values.append(value_of_attribute)
            result_values.extend(self._traverse_a_list(inputs_values))
            result_values.append(command)
        return result_values

    def run(self):
        returned_list = deque()
        for element in self._list_to_traverse:
            result = self._traverse(element)
            if result is not None:
                returned_list.extend(result)
        return returned_list


class RefGenerator:
    _list_of_ordered_commands: deque

    def __init__(self, ordered_commands: deque):
        self._list_of_ordered_commands = ordered_commands

    def _traverse(self, list_of_values) -> Any:
        if isinstance(list_of_values, Command):
            return f"ref@{list_of_values.ref}"
        elif isinstance(list_of_values, LocalCommand):
            return list_of_values.run()
        elif isinstance(list_of_values, list):
            modified_list_of_values = []
            for sub_value_of_attribute in list_of_values:
                modified_list_of_values.append(self._traverse(sub_value_of_attribute))
            return modified_list_of_values
        elif isinstance(list_of_values, dict):
            modified_dict_of_values = {}
            for sub_key, sub_value in list_of_values.items():
                modified_dict_of_values[sub_key] = self._traverse(sub_value)
            return modified_dict_of_values
        else:
            return list_of_values

    def _traverse_command(self, command) -> Command:
        list_of_inputs_attributes = _extract_input_fields(command)
        for input_attribute_name in list_of_inputs_attributes:
            value_of_attribute = _get_attribute_value(input_attribute_name, command)
            attribute_real_value = self._traverse(value_of_attribute)
            setattr(command, input_attribute_name, attribute_real_value)
        return command

    def _traverse_loop(self, loop: Loop) -> Loop:
        array_of_loop = loop.array
        then_of_loop = loop.then
        value_of_array = self._traverse(array_of_loop)
        formatted_then_commands = []
        if isinstance(then_of_loop, list):
            for command_then in then_of_loop:
                formatted_then_commands.append(self._recurse(command_then))
        else:
            formatted_then_commands.append(self._recurse(then_of_loop))
        loop.array = value_of_array
        loop.then = formatted_then_commands
        return loop

    def _traverse_logical(self, logical: Logical) -> Logical:
        condition_of_logical = logical.condition
        then_of_logical = logical.then
        value_of_condition = self._traverse(condition_of_logical)
        formatted_then_commands = []
        if isinstance(then_of_logical, list):
            for command_then in then_of_logical:
                formatted_then_commands.append(self._recurse(command_then))
        else:
            formatted_then_commands.append(self._recurse(then_of_logical))
        logical.condition = value_of_condition
        logical.then = formatted_then_commands
        return logical

    def _recurse(self, command: Logical | Command | Loop) -> Command | Loop | Logical:
        if isinstance(command, Command):
            return self._traverse_command(command)
        elif isinstance(command, LocalCommand):
            return command.run()
        elif isinstance(command, Loop):
            return self._traverse_loop(command)
        elif isinstance(command, Logical):
            return self._traverse_logical(command)

    def run(self):
        final_list = deque()
        for command in self._list_of_ordered_commands:
            final_list.append(self._recurse(command))
        return final_list


class Flow:
    commands: List[Dict[str, Any]]
    name: str
    hash: str
    api_client: SyriusAPI

    def __init__(self, name: str):
        self.commands = []
        self.name = name
        self.hash = ""
        self.api_client = SyriusAPI()

    @staticmethod
    def build(name: str, commands: list[Command | Loop | Logical]) -> "Flow":
        flow = Flow(name)
        traverser = TreeTraverse(commands)
        list_of_commands = traverser.run()
        ref_gen = RefGenerator(list_of_commands)
        list_ref_commands = ref_gen.run()
        flow.set_commands(list_ref_commands)
        return flow

    def _parse_element(self, element: Command | Loop | Logical) -> dict[str, Any]:
        if isinstance(element, Command):
            return element.model_dump()
        elif isinstance(element, Loop) or isinstance(element, Logical):
            then_list_commands = element.then
            command_dumped = element.model_dump()
            new_list = []
            for then in then_list_commands:
                new_list.append(self._parse_element(then))
            command_dumped['then'] = new_list
            return command_dumped

    def set_commands(self, commands: deque) -> None:
        # check if the ref already exist
        for command in commands:
            self.commands.append(self._parse_element(command))
        self.hash = self._get_hash()

    def get_json(self) -> str:
        dict_flow = {
            "name": self.name,
            "hash": self.hash,
            "commands": self.commands
        }
        return json.dumps(dict_flow)

    def get_dict(self) -> dict[str, str | list[Command]]:
        return {
            "name": self.name,
            "hash": self.hash,
            "commands": self.commands
        }

    def get_hash(self) -> str:
        return self.hash

    def get_list(self) -> list[dict[str, Any]]:
        return self.commands

    def _is_not_a_ref(self, value: Any):
        if isinstance(value, str) and "ref@" in value:
            return False
        return True

    def _traverse_list_del_ref(self, list_to_traverse: list[Any]) -> list[Any]:
        new_list = []
        for value in list_to_traverse:
            if isinstance(value, list):
                new_list.append(self._traverse_list_del_ref(value))
            elif isinstance(value, dict):
                new_list.append(self._traverse_dict_del_ref(value))
            else:
                if self._is_not_a_ref(value):
                    new_list.append(value)
        return new_list

    def _traverse_dict_del_ref(self, dict_to_traverse: dict[str, Any]) -> dict[str, Any]:
        new_dict = {}
        if "ref" in dict_to_traverse:
            del dict_to_traverse["ref"]
        for key, value in dict_to_traverse.items():
            if isinstance(value, list):
                new_dict[key] = self._traverse_list_del_ref(value)
            elif isinstance(value, dict):
                new_dict[key] = self._traverse_dict_del_ref(value)
            else:
                if self._is_not_a_ref(value):
                    new_dict[key] = value
        return new_dict

    def _get_hash(self) -> str:
        list_of_strings_command: list[str] = []
        list_of_commands = deepcopy(self.commands)
        for command in list_of_commands:
            del command['ref']
            new_command = self._traverse_dict_del_ref(command)
            list_of_strings_command.append(json.dumps(new_command))
        final_string = "".join(list_of_strings_command)
        return str(adler32(final_string.encode('utf-8')))

    def _check_status(self, runner: str, callback: Callable[[Any], None]):
        status_answer = self.api_client.check_flow_status(runner)
        status = status_answer["status"]
        while True:
            new_status_answer = self.api_client.check_flow_status(runner)
            status = new_status_answer["status"]
            if status == "COMPLETED":
                context = new_status_answer["context"]
                callback(context=context)
                break
            sleep(1)

    def _start_thread(self, runner: str, callback: Callable[[Any], None]):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(self._check_status, runner, callback)

    def run(self, callback: Callable[[Any], None]):
        # check if the following flow already exist
        flow_exist = self.api_client.flow_exist(self.name, self.hash)
        if flow_exist:
            runner_code = self.api_client.run(name=self.name, hash=self.hash)
            self._start_thread(runner_code, callback)
        else:
            self.api_client.add_flow(self.get_dict())
            runner_code = self.api_client.run(name=self.name, hash=self.hash)
            self._start_thread(runner_code, callback)
