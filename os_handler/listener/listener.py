import abc
from typing import NoReturn


class Listener(abc.ABC):
    def listen(self) -> NoReturn:
        raise NotImplementedError()

    def stop(self) -> NoReturn:
        raise NotImplementedError()

    def read(self) -> bytes:
        raise NotImplementedError()
