from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AddCommandRequest(_message.Message):
    __slots__ = ["command", "hotkey"]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    HOTKEY_FIELD_NUMBER: _ClassVar[int]
    command: str
    hotkey: str
    def __init__(self, command: _Optional[str] = ..., hotkey: _Optional[str] = ...) -> None: ...

class DeleteCommandRequest(_message.Message):
    __slots__ = ["command"]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    command: str
    def __init__(self, command: _Optional[str] = ...) -> None: ...

class ExportCommandsRequest(_message.Message):
    __slots__ = ["path"]
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: str
    def __init__(self, path: _Optional[str] = ...) -> None: ...

class GetCommandsResponse(_message.Message):
    __slots__ = ["commands"]
    class CommandsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    COMMANDS_FIELD_NUMBER: _ClassVar[int]
    commands: _containers.ScalarMap[str, str]
    def __init__(self, commands: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ImportCommandsRequest(_message.Message):
    __slots__ = ["path"]
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: str
    def __init__(self, path: _Optional[str] = ...) -> None: ...
