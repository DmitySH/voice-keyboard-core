import signal

from recognizer.vosk_recognizer import VoskRecognizer

DEFAULT_START_POLL_TIME = 1


def bind_stop_signals(recognizer: VoskRecognizer):
    signal.signal(signal.SIGINT, lambda sig, frame: recognizer.stop())
    signal.signal(signal.SIGTERM, lambda sig, frame: recognizer.stop())
