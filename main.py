import os
import sys
from typing import NoReturn

import click
import yaml

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


def check_commands_path(commands_path: str) -> NoReturn:
    if not os.path.exists(commands_path):
        print('Incorrect commands path')
        exit(-2)


@click.option("-p", "--platform", required=True,
              help="Platform where core will be running",
              type=click.Choice(["windows", "macos"]))
@click.option("-c", "--commands-path", required=True,
              help="Path to file in JSON format where to store commands",
              type=str)
@click.command()
def main(platform: str, commands_path: str):
    check_commands_path(commands_path)

    os.chdir(sys._MEIPASS)
    config = load_config()

    audio_config = AudioConfig(**config['audio'])
    listener = MicrophoneListener(audio_config)

    vk_codes_filename = ' vk_codes_windows.json' if platform == 'windows' \
        else 'vk_codes_macos.json'
    vk_codes_path = os.path.join('config', vk_codes_filename)

    virtual_keyboard = PynputKeyboard(
        commands_path,
        vk_codes_path,
        config['virtual_keyboard']['similarity_threshold']
    )

    recognizer = VoskRecognizer(listener, config['model']['path'],
                                virtual_keyboard,
                                audio_config)

    server = GrpcServer(config['server']['address'])
    commands_pb2_grpc.add_CommandsServicer_to_server(
        CommandsService(commands_path, vk_codes_path, virtual_keyboard),
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

    virtual_keyboard.save_commands_file(commands_path)


if __name__ == '__main__':
    # main()
    print(os.path.join('config', 'vk_codes_windows.json'))
