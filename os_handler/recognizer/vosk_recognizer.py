import os
from copy import copy

from vosk import KaldiRecognizer, Model

from config.class_config.audio_config import AudioConfig
from listener.listener import Listener
from recognizer.recognizer import Recognizer


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

    def recognize_voice(self):
        self.__listener.listen()
        self.__in_work = True
        print('Start voice recognition')

        while self.__in_work:
            if self.__recognizer.AcceptWaveform(self.__listener.read()):
                print(self.__recognizer.Result())
        print('Stop voice recognition')

        self.__listener.stop()

    def stop(self):
        self.__in_work = False
