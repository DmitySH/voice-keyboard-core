from google.protobuf import empty_pb2

from pb.app_control.app_control_pb2_grpc import AppControlServicer
from recognizer.base import Recognizer


class AppControlService(AppControlServicer):
    def __init__(self, recognizer: Recognizer) -> None:
        self.__recognizer = recognizer

    def ChangeMicrophoneStatus(self, request, context):
        if request.on:
            self.__recognizer.unmute()
        else:
            self.__recognizer.mute()

        return empty_pb2.Empty()
