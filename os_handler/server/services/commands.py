import json
from typing import Dict

from pb.commands_pb2_grpc import CommandsServicer
from pb.commands_pb2 import AddCommandResponse


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

        try:
            commands[request.command] = request.hotkey

            with open(self.__commands_path, 'w', encoding='utf-8') as file:
                json.dump(commands, file, ensure_ascii=False)
        except Exception:
            return AddCommandResponse(status=500,
                                      error="can't read write file")

        self.__notify_observers('add_command')
        return AddCommandResponse(status=201, error='')
