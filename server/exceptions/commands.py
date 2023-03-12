class InvalidCommandError(Exception):
    def __init__(self, command: str, *args):
        super().__init__(*args)
        self.command = command


class InvalidHotkeyError(Exception):
    def __init__(self, key: str, *args):
        super().__init__(*args)
        self.key = key
