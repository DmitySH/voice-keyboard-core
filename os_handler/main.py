import threading
import time

import yaml

from listener.microphone_listener import MicrophoneListener, AudioConfig
from os_handler.recognizer.vosk_recognizer import VoskRecognizer

CONFIG_PATH = 'config/config.yaml'


def load_config():
    config = None
    with open(CONFIG_PATH) as cfg:
        try:
            config = yaml.safe_load(cfg)
        except yaml.YAMLError as err:
            exit(err)
    if not config:
        print('Config is not loaded')
        exit(-1)

    return config


def main():
    config = load_config()
    audio_config = AudioConfig(**config['audio'])

    listener = MicrophoneListener(audio_config)
    recognizer = VoskRecognizer(listener, config['model']['path'],
                                audio_config)

    t = threading.Thread(target=recognizer.recognize_voice)
    t.start()

    time.sleep(5)
    recognizer.stop()


if __name__ == '__main__':
    main()
