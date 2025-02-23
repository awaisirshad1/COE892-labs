from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class mine_serial_number(_message.Message):
    __slots__ = ("serial_number",)
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    serial_number: str
    def __init__(self, serial_number: _Optional[str] = ...) -> None: ...

class mine_pin(_message.Message):
    __slots__ = ("pin",)
    PIN_FIELD_NUMBER: _ClassVar[int]
    pin: str
    def __init__(self, pin: _Optional[str] = ...) -> None: ...
