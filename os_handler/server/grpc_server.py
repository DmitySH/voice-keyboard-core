from concurrent import futures
from typing import NoReturn

import grpc
from pb import commands_pb2_grpc

from server.base import Server
from server.services.commands import CommandsService


class GrpcServer(Server):
    def __init__(self, address: str) -> None:
        self.__address = address
        self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
        self.__server.add_insecure_port(self.__address)
        commands_pb2_grpc.add_CommandsServicer_to_server(
            CommandsService(), self.__server)

    def serve(self) -> NoReturn:
        self.__server.start()
        print(f'Server started on {self.__address}')
        self.__server.wait_for_termination()

    def stop(self) -> NoReturn:
        self.__server.stop()
