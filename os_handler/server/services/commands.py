import json
from typing import Dict

from pb.commands_pb2_grpc import CommandsServicer
from pb.commands_pb2 import AddCommandResponse, DeleteCommandResponse, \
    GetCommandsResponse


class CommandsService(CommandsServicer):
    def __init__(self, commands_path: str, observers: Dict) -> None:
        self.__commands_path = commands_path
        self.__observers = observers

    def __notify_observers(self, method: str):
        if method in self.__observers:
            for observer in self.__observers[method]:
                observer()

    def AddCommand(self, request, context):
        print(f'Add command: {request}')

        try:
            with open(self.__commands_path, encoding='utf-8') as file:
                commands = json.load(file)
        except Exception:
            return AddCommandResponse(status=500,
                                      error="can't read commands file")

        if request.command in commands:
            return AddCommandResponse(
                status=400,
                error=f"command {request.command} already exists")

        commands[request.command] = request.hotkey

        try:
            with open(self.__commands_path, 'w', encoding='utf-8') as file:
                json.dump(commands, file, ensure_ascii=False)
        except Exception:
            return AddCommandResponse(status=500,
                                      error="can't write commands file")

        self.__notify_observers('add_command')

        return AddCommandResponse(status=201, error='')

    def DeleteCommand(self, request, context):
        print(f'Delete command: {request}')

        try:
            with open(self.__commands_path, encoding='utf-8') as file:
                commands = json.load(file)
        except Exception:
            return DeleteCommandResponse(status=500,
                                         error="can't read commands file")

        if request.command not in commands:
            return DeleteCommandResponse(
                status=404,
                error=f"command {request.command} is not exists")

        commands.pop(request.command)

        try:
            with open(self.__commands_path, 'w', encoding='utf-8') as file:
                json.dump(commands, file, ensure_ascii=False)
        except Exception:
            return DeleteCommandResponse(status=500,
                                         error="can't write commands file")

        self.__notify_observers('delete_command')

        return DeleteCommandResponse(status=200, error='')

    def GetCommands(self, request, context):
        print(f'Get commands')

        try:
            with open(self.__commands_path, encoding='utf-8') as file:
                commands = json.load(file)
        except Exception:
            return GetCommandsResponse(status=500,
                                       error="can't read commands file",
                                       commands=None)

        self.__notify_observers('get_commands')

        return GetCommandsResponse(status=200,
                                   error='',
                                   commands=commands)
