import json
from typing import Dict, Tuple, NoReturn, Set, List

from pb.commands.commands_pb2 import DefaultResponse, GetCommandsResponse
from pb.commands.commands_pb2_grpc import CommandsServicer
from server.exceptions.commands import InvalidHotkeyError, InvalidCommandError
from virtual_keyboard.base import Keyboard


class CommandsService(CommandsServicer):
    def __init__(self, commands_path: str, vk_codes_path: str,
                 keyboard: Keyboard) -> None:
        self.__commands_path = commands_path
        self.__keyboard = keyboard
        self.__supported_vk_keys: Set[str] = set()

        with open(vk_codes_path, encoding='utf-8') as file:
            self.__supported_vk_keys = set(json.load(file).keys())

    @staticmethod
    def __read_commands_file(path: str) -> Tuple[Dict, Dict]:
        try:
            with open(path, encoding='utf-8') as file:
                commands = json.load(file)
        except FileNotFoundError:
            return {}, {'status': 404, 'error': "commands file not found"}
        except OSError:
            return {}, {'status': 500, 'error': "can't read commands file"}
        except json.JSONDecodeError:
            return {}, {'status': 400, 'error': "incorrect json in file"}

        return commands, {}

    @staticmethod
    def __write_commands_file(path: str, commands: Dict) -> Dict:
        try:
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(commands, file, ensure_ascii=False)
        except FileNotFoundError:
            return {'status': 404, 'error': "commands file not found"}
        except OSError:
            return {'status': 500, 'error': "can't read commands file"}

    def __check_keys_supported(self, vk_keys: List[str]) -> NoReturn:
        for key in vk_keys:
            if key not in self.__supported_vk_keys:
                raise InvalidHotkeyError(key)

    @staticmethod
    def __check_type_command(cmd: str) -> NoReturn:
        first_space_symbol_idx = cmd.find(' ')
        if first_space_symbol_idx != -1 \
                and first_space_symbol_idx < 12 \
                and cmd[:first_space_symbol_idx].startswith('напечата'):
            raise InvalidCommandError(cmd)

    def AddCommand(self, request, context):
        print(f'Add command: {request}')

        commands, err_dict = self.__read_commands_file(self.__commands_path)
        if err_dict:
            return DefaultResponse(**err_dict)

        try:
            self.__check_type_command(request.command)
            self.__check_keys_supported(request.hotkey.split('+'))
        except InvalidCommandError as ex:
            return DefaultResponse(
                status=400,
                error=f"first word in {ex.command} can't be like 'напечатай'")
        except InvalidHotkeyError as ex:
            return DefaultResponse(
                status=400,
                error=f"key {ex.key} is not supported")

        if request.command in commands:
            return DefaultResponse(
                status=400,
                error=f"command {request.command} already exists")

        commands[request.command] = request.hotkey

        err_dict = self.__write_commands_file(self.__commands_path, commands)
        if err_dict:
            return DefaultResponse(**err_dict)

        self.__keyboard.update()

        return DefaultResponse(status=201, error='')

    def DeleteCommand(self, request, context):
        print(f'Delete command: {request}')

        commands, err_dict = self.__read_commands_file(self.__commands_path)
        if err_dict:
            return DefaultResponse(**err_dict)

        if request.command not in commands:
            return DefaultResponse(
                status=404,
                error=f"command {request.command} is not exists")

        commands.pop(request.command)

        commands, err_dict = self.__write_commands_file(self.__commands_path,
                                                        commands)
        if err_dict:
            return DefaultResponse(**err_dict)

        self.__keyboard.update()

        return DefaultResponse(status=200, error='')

    def GetCommands(self, request, context):
        print('Get commands')

        commands, err_dict = self.__read_commands_file(self.__commands_path)
        if err_dict:
            return GetCommandsResponse(commands=None, **err_dict)

        return GetCommandsResponse(status=200, error='', commands=commands)

    def ImportCommands(self, request, context):
        print(f'Import commands: {request}')

        new_commands, err_dict = self.__read_commands_file(request.path)
        if err_dict:
            return DefaultResponse(**err_dict)

        for command, hotkey in new_commands.items():
            try:
                self.__check_type_command(request.command)
                self.__check_keys_supported(hotkey.split('+'))
            except InvalidCommandError as ex:
                return DefaultResponse(
                    status=400,
                    error=f"first word in {ex.command} can't be like 'напечатай'")
            except InvalidHotkeyError as ex:
                return DefaultResponse(
                    status=400,
                    error=f"key {ex.key} is not supported")

        err_dict = self.__write_commands_file(self.__commands_path,
                                              new_commands)
        if err_dict:
            return DefaultResponse(**err_dict)

        self.__keyboard.update()

        return DefaultResponse(status=200, error='')

    def ExportCommands(self, request, context):
        print(f'Export commands: {request}')

        commands, err_dict = self.__read_commands_file(self.__commands_path)
        if err_dict:
            return DefaultResponse(**err_dict)

        err_dict = self.__write_commands_file(request.path,
                                              commands)
        if err_dict:
            return DefaultResponse(**err_dict)

        return DefaultResponse(status=200, error='')
