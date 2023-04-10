from threading import Lock
from typing import NoReturn

from listener.base import Listener
from recognizer.base import Recognizer
from virtual_keyboard.base import Keyboard


class VoiceKeyboard:
    def __init__(self, recognizer: Recognizer, listener: Listener,
                 keyboard: Keyboard):
        self.__recognizer = recognizer
        self.__listener = listener
        self.__keyboard = keyboard
        self.__mu = Lock()

        self.__in_work = False
        self.__trigger = 'клава'
        self.__is_microphone_on = True

    def run(self):
        self.__mu.acquire()

        self.__listener.listen()
        self.__in_work = True
        print('Start voice recognition')
        self.__mu.release()

        while self.__in_work:
            recognized_text = self.__recognizer.recognize(self.__listener.read())
            if recognized_text:
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
