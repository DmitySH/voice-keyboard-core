import signal
from threading import Thread, Event, Lock
from typing import List

from recognizer.vosk_recognizer import VoskRecognizer
from server.grpc_server import GrpcServer


class ThreadController:
    def __init__(self, recognizer: VoskRecognizer, server: GrpcServer,
                 stop_poll_time: int) -> None:
        self.__recognizer = recognizer
        self.__server = server

        self.__active_threads: List[Thread] = []
        self.__mu = Lock()

        self.__stop_poll_time = stop_poll_time
        self.__exit = Event()

    def start_all(self):
        server_thread = Thread(target=self.__server.serve)
        recognizer_thread = Thread(
            target=self.__recognizer.recognize_and_handle_command)

        self.__mu.acquire()
        server_thread.start()
        recognizer_thread.start()

        self.__active_threads.extend([
            recognizer_thread,
            server_thread
        ])
        self.__mu.release()

    def stop_all(self):
        self.__recognizer.stop()
        self.__server.stop()
        self.__exit.set()

    def bind_stop_signals(self):
        signal.signal(signal.SIGINT, lambda sig, frame: self.stop_all())
        signal.signal(signal.SIGTERM, lambda sig, frame: self.stop_all())

    def wait_everything_for_finish(self):
        while not self.__exit.is_set():
            self.__exit.wait(self.__stop_poll_time)

        for active_thread in self.__active_threads:
            active_thread.join()
