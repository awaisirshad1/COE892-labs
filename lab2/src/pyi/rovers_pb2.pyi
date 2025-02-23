from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class rover_number(_message.Message):
    __slots__ = ("rover_number",)
    ROVER_NUMBER_FIELD_NUMBER: _ClassVar[int]
    rover_number: int
    def __init__(self, rover_number: _Optional[int] = ...) -> None: ...

class rover_commands(_message.Message):
    __slots__ = ("commands",)
    COMMANDS_FIELD_NUMBER: _ClassVar[int]
    commands: str
    def __init__(self, commands: _Optional[str] = ...) -> None: ...
