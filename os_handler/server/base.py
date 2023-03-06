import abc
from typing import NoReturn


class Server(abc.ABC):
    @abc.abstractmethod
    def serve(self) -> NoReturn:
        raise NotImplementedError()

    @abc.abstractmethod
    def stop(self) -> NoReturn:
        raise NotImplementedError()
