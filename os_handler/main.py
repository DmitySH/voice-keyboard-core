import yaml

from listener.microphone_listener import MicrophoneListener, AudioConfig
from recognizer.vosk_recognizer import VoskRecognizer
from server.grpc_server import GrpcServer
from server.services.app_control import AppControlService
from server.services.commands import CommandsService
from threads.controller import ThreadController
from virtual_keyboard.pynput_keyboard import PynputKeyboard

from pb.commands import commands_pb2_grpc
from pb.app_control import app_control_pb2_grpc

CONFIG_PATH = 'config/config.yaml'


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
        config['virtual_keyboard']['vk_codes_path'],
        config['virtual_keyboard']['similarity_threshold']
    )

    recognizer = VoskRecognizer(listener, config['model']['path'],
                                virtual_keyboard,
                                audio_config)

    commands_service_observers = {
        'add_command': [virtual_keyboard.update],
        'delete_command': [virtual_keyboard.update],
        'import_commands': [virtual_keyboard.update],
        'export_commands': [virtual_keyboard.update],
    }

    server = GrpcServer(config['server']['address'])
    commands_pb2_grpc.add_CommandsServicer_to_server(
        CommandsService(config['virtual_keyboard']['commands_path'],
                        commands_service_observers),
        server.server
    )
    app_control_pb2_grpc.add_AppControlServicer_to_server(
        AppControlService(recognizer),
        server.server
    )

    thread_controller = ThreadController(recognizer, server, 3)

    thread_controller.bind_stop_signals()
    thread_controller.start_all()
    thread_controller.wait_everything_for_finish()


if __name__ == '__main__':
    main()
