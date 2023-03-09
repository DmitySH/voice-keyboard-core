import abc
from typing import NoReturn


class Recognizer(abc.ABC):
    def recognize_and_handle_command(self) -> NoReturn:
        raise NotImplementedError()

    def stop(self) -> NoReturn:
        raise NotImplementedError()

    def mute(self) -> NoReturn:
        raise NotImplementedError()

    def unmute(self) -> NoReturn:
        raise NotImplementedError()
