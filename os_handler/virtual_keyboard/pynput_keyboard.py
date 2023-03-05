import json
from typing import NoReturn, Dict

from pynput import keyboard

from virtual_keyboard.base import Keyboard
from pynput.keyboard import Controller, Key, KeyCode

CHAR_TO_VK_CODE = {
    'ctrl': 17,
    'c': 67,
    'с': 67,
    'v': 86,
    'м': 86,
}

# DEBUG
DEBUG = False


def print_pressed_keys(key):
    if DEBUG:
        try:
            print(key.vk)
            print(key)
        except Exception as ex:
            print(f'Error on listening keyboard: {ex}')


class PynputKeyboard(Keyboard):
    def __init__(self, commands_path: str) -> None:
        self.__keyboard = Controller()
        self.__commands: Dict[str, str] = dict()

        try:
            with open(commands_path, encoding='utf-8') as file:
                self.__commands = json.load(file)
        except Exception:
            print("Can't read file with commands. "
                  "Commands dictionary is empty")

        print(self.__commands)

        listener = keyboard.Listener(
            on_press=print_pressed_keys)
        listener.start()

    def handle_command(self, cmd: str) -> NoReturn:
        hotkey = self.__commands.get(cmd)
        if not hotkey:
            print(f'Command {cmd} not found')
            return

        print(f'Executing {hotkey}')
        self.__hotkey(hotkey)

    def __hotkey(self, hotkey: str):
        keys = hotkey.split('+')
        for key in keys:
            self.__keyboard.press(KeyCode.from_vk(CHAR_TO_VK_CODE[key]))
        for key in keys[::-1]:
            self.__keyboard.release(KeyCode.from_vk(CHAR_TO_VK_CODE[key]))
