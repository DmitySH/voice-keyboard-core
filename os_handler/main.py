import threading
import time

import yaml

from listener.microphone_listener import MicrophoneListener, AudioConfig
from recognizer.vosk_recognizer import VoskRecognizer
from virtual_keyboard.pynput_keyboard import PynputKeyboard
from shutdown.graceful import bind_stop_signals

CONFIG_PATH = 'config/config.yaml'

DEFAULT_STOP_POLL_TIME = 3


def load_config():
    config = None
    with open(CONFIG_PATH) as cfg:
        try:
            config = yaml.safe_load(cfg)
        except yaml.YAMLError as ex:
            exit(ex)
    if not config:
        print('Config is not loaded')
        exit(-1)

    return config


def main():
    config = load_config()
    audio_config = AudioConfig(**config['audio'])

    listener = MicrophoneListener(audio_config)
    virtual_keyboard = PynputKeyboard(
        config['virtual_keyboard']['commands_path'],
        config['virtual_keyboard']['vk_codes_path']
    )
    recognizer = VoskRecognizer(listener, config['model']['path'],
                                virtual_keyboard,
                                audio_config)

    bind_stop_signals(recognizer)

    recognizer_thread = threading.Thread(
        target=recognizer.recognize_and_handle_command)
    recognizer_thread.start()

    while not recognizer.is_stopped:
        time.sleep(DEFAULT_STOP_POLL_TIME)
    recognizer_thread.join()


if __name__ == '__main__':
    main()
