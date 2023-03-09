class AudioConfig:
    def __init__(self, sample_format: int, chunk_size: int, channels: int,
                 frequency: int):
        self.chunk_size = chunk_size
        self.sample_format = sample_format
        self.channels = channels
        self.frequency = frequency
