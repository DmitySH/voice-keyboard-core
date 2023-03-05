import abc
from typing import NoReturn


class Keyboard(abc.ABC):
    def handle_command(self, cmd: str) -> NoReturn:
        raise NotImplementedError()
