import os
from copy import copy
from threading import Lock
from typing import NoReturn

from vosk import KaldiRecognizer, Model

from config.class_config.audio_config import AudioConfig
from listener.base import Listener
from recognizer.base import Recognizer


class VoskRecognizer(Recognizer):
    def __init__(self, listener: Listener, model_path: str,
                 audio_cfg: AudioConfig) -> None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f'No directory with model at {model_path}')

        self.__audio_cfg = copy(audio_cfg)
        self.__recognizer = KaldiRecognizer(Model(model_path),
                                            self.__audio_cfg.frequency)
        self.__listener = listener
        self.__in_work = False
        self.__is_stopped = False

        self.__mu = Lock()

    @property
    def is_stopped(self) -> bool:
        return self.__is_stopped

    def recognize_voice(self) -> NoReturn:
        self.__mu.acquire()
        if self.__is_stopped:
            print('Recognizer is stopped already')
            return

        self.__listener.listen()
        self.__in_work = True
        print('Start voice recognition')
        self.__mu.release()

        while self.__in_work:
            if self.__recognizer.AcceptWaveform(self.__listener.read()):
                print(self.__recognizer.Result())
        print('Stop voice recognition')

        self.__listener.stop()
        self.__is_stopped = True

    def stop(self) -> NoReturn:
        self.__mu.acquire()
        if self.__in_work:
            self.__in_work = False
        else:
            self.__is_stopped = True
        self.__mu.release()
