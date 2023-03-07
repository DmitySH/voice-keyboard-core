from concurrent import futures
from typing import NoReturn

import grpc

from server.base import Server


class GrpcServer(Server):
    def __init__(self, address: str) -> None:
        self.__address = address
        self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        self.__server.add_insecure_port(self.__address)

    @property
    def server(self) -> grpc.Server:
        return self.__server

    def serve(self) -> NoReturn:
        self.__server.start()
        print(f'Server started on {self.__address}')
        self.__server.wait_for_termination()

    def stop(self) -> NoReturn:
        self.__server.stop(grace=1)
        print('Server stopped')
