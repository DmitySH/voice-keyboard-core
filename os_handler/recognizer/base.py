import abc
from typing import NoReturn


class Recognizer(abc.ABC):
    def recognize_voice(self) -> NoReturn:
        raise NotImplementedError()

    def stop(self) -> NoReturn:
        raise NotImplementedError()
