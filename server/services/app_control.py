from google.protobuf import empty_pb2

from app.voice_keyboard import VoiceKeyboard
from pb.app_control.app_control_pb2_grpc import AppControlServicer


class AppControlService(AppControlServicer):
    def __init__(self, app: VoiceKeyboard) -> None:
        self.__app = app

    def ChangeMicrophoneStatus(self, request, context):
        if request.on:
            self.__app.unmute()
        else:
            self.__app.mute()

        return empty_pb2.Empty()
