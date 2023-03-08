import json
import os
from copy import copy
from threading import Lock
from typing import NoReturn

from vosk import KaldiRecognizer, Model

from config.class_config.audio_config import AudioConfig
from listener.base import Listener
from recognizer.base import Recognizer
from virtual_keyboard.base import Keyboard


class VoskRecognizer(Recognizer):
    def __init__(self, listener: Listener, model_path: str,
                 keyboard: Keyboard, audio_cfg: AudioConfig) -> None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f'No directory with model at {model_path}')

        self.__audio_cfg = copy(audio_cfg)
        self.__recognizer = KaldiRecognizer(Model(model_path),
                                            self.__audio_cfg.frequency)
        self.__listener = listener
        self.__keyboard = keyboard

        self.__in_work = False
        self.__mu = Lock()

        self.__trigger = 'клава'

        self.__is_microphone_on = True

    def recognize_and_handle_command(self) -> NoReturn:
        self.__mu.acquire()

        self.__listener.listen()
        self.__in_work = True
        print('Start voice recognition')
        self.__mu.release()

        while self.__in_work:
            if self.__recognizer.AcceptWaveform(self.__listener.read()):
                recognized_text: str = json.loads(self.__recognizer.Result())[
                    'text']
                if recognized_text and self.__is_microphone_on:
                    commands = [cmd.strip() for cmd in
                                recognized_text.split(self.__trigger)[1:]]

                    print(commands)
                    self.__keyboard.handle_commands(commands)
        print('Stop voice recognition')

        self.__listener.stop()

    def stop(self) -> NoReturn:
        self.__mu.acquire()
        self.__in_work = False
        self.__mu.release()

    def mute(self) -> NoReturn:
        self.__is_microphone_on = False

    def unmute(self) -> NoReturn:
        self.__is_microphone_on = True
