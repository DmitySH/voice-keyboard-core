import signal
import threading
import time
from typing import List

from recognizer.vosk_recognizer import VoskRecognizer
from server.grpc_server import GrpcServer


class ThreadPair:
    def __init__(self, obj, thread: threading.Thread) -> None:
        if not hasattr(obj, 'is_stopped'):
            raise AttributeError(f'{obj} has no is_stopped attribute')

        self.obj = obj
        self.thread = thread


class ThreadController:
    def __init__(self, recognizer: VoskRecognizer, server: GrpcServer,
                 stop_poll_time: int) -> None:
        self.__recognizer = recognizer
        self.__server = server

        self.__active_thread_pairs: List[ThreadPair] = []
        self.__mu = threading.Lock()

        self.__stop_poll_time = stop_poll_time

    def start_all(self):
        server_thread = threading.Thread(target=self.__server.serve)
        recognizer_thread = threading.Thread(
            target=self.__recognizer.recognize_and_handle_command)

        self.__mu.acquire()
        server_thread.start()
        recognizer_thread.start()

        self.__active_thread_pairs.extend([
            ThreadPair(self.__recognizer, recognizer_thread),
            ThreadPair(self.__server, server_thread)
        ])
        self.__mu.release()

    def stop_all(self):
        self.__recognizer.stop()
        self.__server.stop()

    def bind_stop_signals(self):
        signal.signal(signal.SIGINT, lambda sig, frame: self.stop_all())
        signal.signal(signal.SIGTERM, lambda sig, frame: self.stop_all())

    def wait_everything_for_finish(self):
        for active_thread_pair in self.__active_thread_pairs:
            while not active_thread_pair.obj.is_stopped:
                time.sleep(self.__stop_poll_time)
            active_thread_pair.thread.join()
