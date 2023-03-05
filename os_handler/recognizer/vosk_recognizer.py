import os
from copy import copy
from threading import Lock
from typing import NoReturn
import json

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
        self.__is_stopped = False

        self.__mu = Lock()

        self.__trigger = 'клава'

    @property
    def is_stopped(self) -> bool:
        return self.__is_stopped

    def recognize_and_handle_command(self) -> NoReturn:
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
                cmd: str = json.loads(self.__recognizer.Result())['text']
                if cmd:
                    trigger_index = cmd.find(self.__trigger)
                    if trigger_index != -1:
                        cmd = cmd[trigger_index + len(self.__trigger):].strip()
                        print(cmd)
                        self.__keyboard.handle_command(cmd)
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
