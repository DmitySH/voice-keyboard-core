from typing import ClassVar as _ClassVar, Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor


class ChangeMicrophoneStatusRequest(_message.Message):
    __slots__ = ["on"]
    ON_FIELD_NUMBER: _ClassVar[int]
    on: bool

    def __init__(self, on: bool = ...) -> None: ...


class DefaultResponse(_message.Message):
    __slots__ = ["error", "status"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    error: str
    status: int

    def __init__(self, status: _Optional[int] = ...,
                 error: _Optional[str] = ...) -> None: ...
