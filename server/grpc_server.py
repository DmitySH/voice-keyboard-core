from concurrent import futures
from typing import NoReturn, List

import grpc
from google.rpc import code_pb2, status_pb2
from grpc_status import rpc_status

from server.base import Server


def abort(ctx, code: code_pb2.Code, msg: str = '',
          details: List = None) -> NoReturn:
    if details is None:
        details = []

    ctx.abort_with_status(rpc_status.to_status(status_pb2.Status(
        code=code,
        message=msg,
        details=details,
    )))


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
