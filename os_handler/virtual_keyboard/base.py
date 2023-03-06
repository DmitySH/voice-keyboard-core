import abc
from typing import NoReturn, List


class Keyboard(abc.ABC):
    def handle_commands(self, cmd: List[str]) -> NoReturn:
        raise NotImplementedError()

    def update(self) -> NoReturn:
        raise NotImplementedError()
