from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AddCommandRequest(_message.Message):
    __slots__ = ["command", "hotkey"]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    HOTKEY_FIELD_NUMBER: _ClassVar[int]
    command: str
    hotkey: str
    def __init__(self, command: _Optional[str] = ..., hotkey: _Optional[str] = ...) -> None: ...

class AddCommandResponse(_message.Message):
    __slots__ = ["error", "status"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    error: str
    status: int
    def __init__(self, status: _Optional[int] = ..., error: _Optional[str] = ...) -> None: ...

class DeleteCommandRequest(_message.Message):
    __slots__ = ["command"]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    command: str
    def __init__(self, command: _Optional[str] = ...) -> None: ...

class DeleteCommandResponse(_message.Message):
    __slots__ = ["error", "status"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    error: str
    status: int
    def __init__(self, status: _Optional[int] = ..., error: _Optional[str] = ...) -> None: ...
