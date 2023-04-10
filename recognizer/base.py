import abc


class Recognizer(abc.ABC):
    def recognize(self, audio_stream) -> str:
        raise NotImplementedError()
