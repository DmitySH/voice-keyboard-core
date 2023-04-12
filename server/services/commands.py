import json
import os
from typing import Dict, NoReturn, Set, List

from google.protobuf import empty_pb2
from google.rpc import code_pb2

from pb.commands.commands_pb2 import GetCommandsResponse
from pb.commands.commands_pb2_grpc import CommandsServicer
from server.exceptions.commands import InvalidHotkeyError, InvalidCommandError
from server.grpc_server import abort
from virtual_keyboard.base import Keyboard


class CommandsService(CommandsServicer):
    def __init__(self, commands_path: str, vk_codes_path: str,
                 keyboard: Keyboard) -> None:
        self.__commands_path = commands_path
        self.__keyboard = keyboard
        self.__supported_vk_keys: Set[str] = set()

        allowed_symbols = [letter for letter in
                           ' абвгдеёжзийклмнопрстуфхцчшщъыьэюя']
        self.__allowed_command_symbols = set(allowed_symbols)

        with open(vk_codes_path, encoding='utf-8') as file:
            self.__supported_vk_keys = set(json.load(file).keys())

    @staticmethod
    def __read_commands_file(ctx, path: str) -> Dict:
        try:
            with open(path, encoding='utf-8') as file:
                commands = json.load(file)
        except FileNotFoundError:
            abort(ctx, code_pb2.NOT_FOUND, "Файл с командами не найден")
        except json.JSONDecodeError:
            abort(ctx, code_pb2.INVALID_ARGUMENT, "Некорректный JSON файл")
        except OSError:
            abort(ctx, code_pb2.INTERNAL, "Невозможно прочитать файл с командами")

        return commands

    @staticmethod
    def __write_commands_file(ctx, path: str, commands: Dict) -> NoReturn:
        try:
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(commands, file, ensure_ascii=False)
        except OSError:
            abort(ctx, code_pb2.INTERNAL, "Невозможно записать файл с командами")

    def __check_command_and_hotkey(self, context, command: str,
                                   hotkey: str) -> NoReturn:
        try:
            self.__check_command_is_correct(command)
            self.__check_type_command(command)
            self.__check_keys_supported(hotkey.split('+'))
        except (InvalidCommandError, InvalidHotkeyError) as ex:
            abort(context, code_pb2.INVALID_ARGUMENT, ex.message)

    @staticmethod
    def __check_type_command(cmd: str) -> NoReturn:
        first_space_symbol_idx = cmd.find(' ')
        if first_space_symbol_idx != -1 \
                and first_space_symbol_idx < 12 \
                and cmd[:first_space_symbol_idx].startswith('напечата'):
            raise InvalidCommandError(
                f"Первое слово в команде не может быть похоже на 'напечатай'")

    def __check_command_is_correct(self, cmd: str) -> NoReturn:
        for sym in cmd:
            if sym not in self.__allowed_command_symbols:
                raise InvalidCommandError(
                    f"Символ {sym} в команде {cmd} не разрешен")

    def __check_keys_supported(self, vk_keys: List[str]) -> NoReturn:
        for key in vk_keys:
            if key not in self.__supported_vk_keys:
                raise InvalidHotkeyError(f"Клавиша {key} не поддерживается")

    def AddCommand(self, request, context):
        print(f'Add command: {request}')

        commands = self.__read_commands_file(context, self.__commands_path)

        self.__check_command_and_hotkey(context, request.command,
                                        request.hotkey)

        if request.command in commands:
            abort(context, code_pb2.ALREADY_EXISTS,
                  f"Команда {request.command} уже существует")

        commands[request.command] = request.hotkey

        self.__write_commands_file(context, self.__commands_path, commands)
        self.__keyboard.update()

        return empty_pb2.Empty()

    def DeleteCommand(self, request, context):
        print(f'Delete command: {request}')

        commands = self.__read_commands_file(context, self.__commands_path)

        if request.command not in commands:
            abort(context, code_pb2.NOT_FOUND,
                  f"Команда {request.command} не существует")

        commands.pop(request.command)

        self.__write_commands_file(context, self.__commands_path, commands)
        self.__keyboard.update()

        return empty_pb2.Empty()

    def GetCommands(self, request, context):
        print('Get commands')

        commands = self.__read_commands_file(context, self.__commands_path)

        return GetCommandsResponse(commands=commands)

    def ImportCommands(self, request, context):
        print(f'Import commands: {request}')

        new_commands = self.__read_commands_file(context, request.path)

        for command, hotkey in new_commands.items():
            self.__check_command_and_hotkey(context, command, hotkey)

        self.__write_commands_file(context, self.__commands_path, new_commands)
        self.__keyboard.update()

        return empty_pb2.Empty()

    def ExportCommands(self, request, context):
        print(f'Export commands: {request}')

        commands = self.__read_commands_file(context, self.__commands_path)
        self.__write_commands_file(context, request.path, commands)

        return empty_pb2.Empty()
