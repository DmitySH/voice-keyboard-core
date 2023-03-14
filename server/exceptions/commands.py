class InvalidCommandError(Exception):
    def __init__(self, message: str, *args) -> None:
        super().__init__(*args)
        self.message = message


class InvalidHotkeyError(Exception):
    def __init__(self, message: str, *args) -> None:
        super().__init__(*args)
        self.message = message
