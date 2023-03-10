import json
from typing import Dict, Tuple, NoReturn, Set, List

from pb.commands.commands_pb2 import DefaultResponse, GetCommandsResponse
from pb.commands.commands_pb2_grpc import CommandsServicer


class CommandsService(CommandsServicer):
    def __init__(self, commands_path: str, vk_codes_path: str,
                 observers: Dict) -> None:
        self.__commands_path = commands_path
        self.__observers = observers
        self.__supported_vk_keys: Set[str] = set()

        with open(vk_codes_path, encoding='utf-8') as file:
            self.__supported_vk_keys = set(json.load(file).keys())

    def __notify_observers(self, method: str) -> NoReturn:
        if method in self.__observers:
            for observer in self.__observers[method]:
                observer()

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

    def __check_key_is_supported(self, vk_keys: List[str]) -> NoReturn:
        for key in vk_keys:
            if key not in self.__supported_vk_keys:
                return DefaultResponse(
                    status=400,
                    error=f"key {key} is not supported")

    def AddCommand(self, request, context):
        print(f'Add command: {request}')

        commands, err_dict = self.__read_commands_file(self.__commands_path)
        if err_dict:
            return DefaultResponse(**err_dict)

        self.__check_key_is_supported(request.hotkey.split('+'))

        if request.command in commands:
            return DefaultResponse(
                status=400,
                error=f"command {request.command} already exists")

        commands[request.command] = request.hotkey

        err_dict = self.__write_commands_file(self.__commands_path, commands)
        if err_dict:
            return DefaultResponse(**err_dict)

        self.__notify_observers('add_command')

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

        self.__notify_observers('delete_command')

        return DefaultResponse(status=200, error='')

    def GetCommands(self, request, context):
        print('Get commands')

        commands, err_dict = self.__read_commands_file(self.__commands_path)
        if err_dict:
            return GetCommandsResponse(commands=None, **err_dict)

        self.__notify_observers('get_commands')

        return GetCommandsResponse(status=200, error='', commands=commands)

    def ImportCommands(self, request, context):
        print(f'Import commands: {request}')

        new_commands, err_dict = self.__read_commands_file(request.path)
        if err_dict:
            return DefaultResponse(**err_dict)

        for hotkey in new_commands.values():
            self.__check_key_is_supported(hotkey.split('+'))

        err_dict = self.__write_commands_file(self.__commands_path,
                                              new_commands)
        if err_dict:
            return DefaultResponse(**err_dict)

        self.__notify_observers('import_commands')

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

        self.__notify_observers('export_commands')

        return DefaultResponse(status=200, error='')
