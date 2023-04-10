import json
import os
import sys

import click
import yaml

from app.voice_keyboard import VoiceKeyboard
from listener.microphone_listener import MicrophoneListener, AudioConfig
from pb.app_control import app_control_pb2_grpc
from pb.commands import commands_pb2_grpc
from recognizer.vosk_recognizer import VoskRecognizer
from server.grpc_server import GrpcServer
from server.services.app_control import AppControlService
from server.services.commands import CommandsService
from threads.controller import ThreadController
from virtual_keyboard.pynput_keyboard import PynputKeyboard

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


def create_paths_for_commands(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

    path = os.path.join(path, 'commands.json')
    if not os.path.exists(path):
        with open(path, 'w') as file:
            json.dump({}, file)

    return path


def get_commands_file_path(platform: str):
    if platform == 'windows':
        if not os.getenv('APPDATA'):
            print('No appdata path is os.env')
            exit(-1)
        initial_path = os.path.join(os.getenv('APPDATA'), 'VoiceKeyboard')

        return create_paths_for_commands(initial_path)

    elif platform == 'macos':
        initial_path = os.path.join(os.path.expanduser("~"), 'Library',
                                    'VoiceKeyboard')

        return create_paths_for_commands(initial_path)
    else:
        raise OSError('Unknown platform. Should be one of: [windows, macos]')


@click.option("-p", "--platform", required=True,
              help="Platform where core will be running",
              type=click.Choice(["windows", "macos"]))
@click.command()
def main(platform: str):
    os.chdir(sys._MEIPASS)
    config = load_config()

    audio_config = AudioConfig(**config['audio'])
    listener = MicrophoneListener(audio_config)

    vk_codes_filename = 'vk_codes_windows.json' if platform == 'windows' \
        else 'vk_codes_macos.json'
    vk_codes_path = os.path.join('config', vk_codes_filename)

    commands_path = get_commands_file_path(platform)

    virtual_keyboard = PynputKeyboard(
        commands_path,
        vk_codes_path,
        config['virtual_keyboard']['similarity_threshold']
    )

    recognizer = VoskRecognizer(config['model']['path'], audio_config)
    app = VoiceKeyboard(recognizer, listener, virtual_keyboard)

    server = GrpcServer(config['server']['address'])
    commands_pb2_grpc.add_CommandsServicer_to_server(
        CommandsService(commands_path, vk_codes_path, virtual_keyboard),
        server.server
    )
    app_control_pb2_grpc.add_AppControlServicer_to_server(
        AppControlService(app),
        server.server
    )

    thread_controller = ThreadController(app, server, 3)

    thread_controller.bind_stop_signals()
    thread_controller.start_all()
    thread_controller.wait_everything_for_finish()

    virtual_keyboard.save_commands_file(commands_path)


if __name__ == '__main__':
    main()
