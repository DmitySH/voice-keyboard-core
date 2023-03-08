import json
import os
from threading import Lock
from typing import NoReturn, Dict, List, Tuple

from Levenshtein import ratio
from pynput import keyboard
from pynput.keyboard import Controller, KeyCode

from virtual_keyboard.base import Keyboard

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
        self.__commands_path = commands_path
        self.__mu = Lock()

        self.__read_commands_file()

        with open(vk_codes_path, encoding='utf-8') as file:
            self.__vk_codes = json.load(file)

        if DEBUG:
            listener = keyboard.Listener(on_press=print_pressed_keys)
            listener.start()

    def save_commands_file(self, path: str) -> NoReturn:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(self.__commands, file, ensure_ascii=False)

    def __read_commands_file(self) -> NoReturn:
        try:
            with open(self.__commands_path, encoding='utf-8') as file:
                self.__mu.acquire()
                self.__commands = json.load(file)
                self.__mu.release()
        except OSError:
            try:
                basedir = os.path.dirname(self.__commands_path)
                if not os.path.exists(basedir):
                    os.makedirs(basedir)
                with open(self.__commands_path, 'w') as file:
                    json.dump({}, file)
            except OSError as ex:
                print("Can't create commands file")
                raise ex

    def handle_commands(self, commands: List[str]) -> NoReturn:
        for cmd in commands:
            self.__handle_command(cmd)

    def __handle_command(self, cmd: str) -> NoReturn:
        if self.__is_type_command(cmd):
            self.__handle_type_command(cmd)
            return

        max_similarity, max_similarity_cmd = \
            self.__compare_commands_by_levenshtein(cmd)

        if max_similarity < self.__similarity_threshold:
            print(f'Command {cmd} not found')
            return

        self.__mu.acquire()
        hotkey = self.__commands[max_similarity_cmd]
        self.__mu.release()

        self.__activate_hotkey(hotkey)

    @staticmethod
    def __is_type_command(cmd: str) -> bool:
        first_space_symbol_idx = cmd.find(' ')
        return first_space_symbol_idx != -1 \
               and first_space_symbol_idx < 11 \
               and cmd[:first_space_symbol_idx].startswith('напечата')

    def __handle_type_command(self, cmd: str) -> NoReturn:
        first_space_symbol_idx = cmd.find(' ')
        text_to_type = cmd[first_space_symbol_idx + 1:]
        print(f'Typing: {text_to_type}')

        self.__keyboard.type(text_to_type)

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

        print(f'Executing: {hotkey}')

        for key in keys:
            self.__keyboard.press(KeyCode.from_vk(self.__vk_codes[key]))
        for key in keys[::-1]:
            self.__keyboard.release(KeyCode.from_vk(self.__vk_codes[key]))

    def __check_keys(self, keys: List[str]) -> bool:
        for key in keys:
            if key not in self.__vk_codes:
                print(f'Unknown key: {key}')
                return False

        return True

    def update(self) -> NoReturn:
        self.__read_commands_file()
