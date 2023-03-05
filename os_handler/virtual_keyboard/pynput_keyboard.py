import json
from typing import NoReturn, Dict, List, Tuple

from pynput import keyboard

from virtual_keyboard.base import Keyboard
from pynput.keyboard import Controller, KeyCode
from Levenshtein import ratio

VK_CODES_PATH = 'vk_codes.json'
DEBUG = False


def print_pressed_keys(key):
    try:
        print(key.vk)
        print(key)
    except Exception as ex:
        print(f'Error on listening keyboard: {ex}')


class PynputKeyboard(Keyboard):
    def __init__(self, commands_path: str,
                 vk_codes_path: str,
                 similarity_threshold: float) -> None:
        self.__keyboard = Controller()
        self.__commands: Dict[str, str] = dict()
        self.__vk_codes: Dict[str, str] = dict()
        self.__similarity_threshold = similarity_threshold

        try:
            with open(commands_path, encoding='utf-8') as file:
                self.__commands = json.load(file)
        except Exception:
            print("Can't read file with commands. "
                  "Commands dictionary is empty")

        with open(vk_codes_path, encoding='utf-8') as file:
            self.__vk_codes = json.load(file)

        if DEBUG:
            listener = keyboard.Listener(
                on_press=print_pressed_keys)
            listener.start()

    def handle_command(self, cmd: str) -> NoReturn:
        max_similarity, max_similarity_cmd = \
            self.__compare_commands_by_levenshtein(cmd)

        if max_similarity < self.__similarity_threshold:
            print(f'Command {cmd} not found')
            return

        hotkey = self.__commands[max_similarity_cmd]
        self.__activate_hotkey(hotkey)

    def __compare_commands_by_levenshtein(self, cmd: str) -> Tuple[float, str]:
        max_similarity, max_similarity_cmd = -1, ''
        for known_cmd in self.__commands:
            similarity = ratio(cmd, known_cmd)
            if similarity > max_similarity:
                max_similarity, max_similarity_cmd = similarity, known_cmd

        print(f'Max command similarity: {round(max_similarity, 2)} '
              f'for {max_similarity_cmd} command')

        return max_similarity, max_similarity_cmd

    def __activate_hotkey(self, hotkey: str) -> NoReturn:
        keys = hotkey.split('+')
        if not self.__check_keys(keys):
            return

        print(f'Executing {hotkey}')

        for key in keys:
            self.__keyboard.press(KeyCode.from_vk(self.__vk_codes[key]))
        for key in keys[::-1]:
            self.__keyboard.release(KeyCode.from_vk(self.__vk_codes[key]))

    def __check_keys(self, keys: List[str]) -> bool:
        for key in keys:
            if key not in self.__vk_codes:
                print(f'Unknown key {key}')
                return False

        return True
