import pyaudio


class AudioConfig:
    def __init__(self):
        self.chunk_size: int = 2048
        self.sample_format: int = pyaudio.paInt16
        self.channels: int = 1
        self.frequency: int = 16_000
