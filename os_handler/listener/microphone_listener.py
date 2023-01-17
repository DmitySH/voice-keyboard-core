from copy import copy
from typing import NoReturn

import pyaudio

from os_handler.config.class_config.audio_config import AudioConfig
from os_handler.listener.listener import Listener


class MicrophoneListener(Listener):
    def __init__(self, audio_cfg: AudioConfig) -> None:
        self.__audio_cfg = copy(audio_cfg)

        self.__audio = pyaudio.PyAudio()
        self.__stream = self.__audio.open(
            format=self.__audio_cfg.sample_format,
            channels=self.__audio_cfg.channels,
            rate=self.__audio_cfg.frequency,
            frames_per_buffer=self.__audio_cfg.chunk_size,
            input=True)

    def listen(self) -> NoReturn:
        print('Start recording microphone')
        self.__stream.start_stream()

    def stop(self) -> NoReturn:
        self.__stream.stop_stream()
        self.__stream.close()

        self.__audio.terminate()
        self.__audio = pyaudio.PyAudio()
        print('Stop recording microphone')

    def read(self) -> bytes:
        return self.__stream.read(self.__audio_cfg.chunk_size,
                                  exception_on_overflow=False)
