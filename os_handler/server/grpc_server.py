from concurrent import futures
from typing import NoReturn, List

import grpc
from pb import commands_pb2_grpc

from server.base import Server


class GrpcServer(Server):
    def __init__(self, address: str,
                 services: List[commands_pb2_grpc.CommandsServicer]) -> None:
        self.__address = address
        self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        self.__server.add_insecure_port(self.__address)

        for service in services:
            commands_pb2_grpc.add_CommandsServicer_to_server(
                service, self.__server)

    def serve(self) -> NoReturn:
        self.__server.start()
        print(f'Server started on {self.__address}')
        self.__server.wait_for_termination()

    def stop(self) -> NoReturn:
        self.__server.stop(grace=1)
        print('Server stopped')
