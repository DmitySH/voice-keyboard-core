import json
import os
from copy import copy

from vosk import KaldiRecognizer, Model

from config.class_config.audio_config import AudioConfig
from recognizer.base import Recognizer


class VoskRecognizer(Recognizer):
    def __init__(self, model_path: str, audio_cfg: AudioConfig) -> None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f'No directory with model at {model_path}')

        self.__audio_cfg = copy(audio_cfg)
        self.__recognizer = KaldiRecognizer(Model(model_path),
                                            self.__audio_cfg.frequency)

    def recognize(self, audio_bytes) -> str:
        if self.__recognizer.AcceptWaveform(audio_bytes):
            return json.loads(self.__recognizer.Result())['text']
