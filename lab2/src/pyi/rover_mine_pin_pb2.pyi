import mines_pb2 as _mines_pb2
import rovers_pb2 as _rovers_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class rover_mine_serial_pin(_message.Message):
    __slots__ = ("num", "serial_number", "pin")
    NUM_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PIN_FIELD_NUMBER: _ClassVar[int]
    num: _rovers_pb2.rover_number
    serial_number: _mines_pb2.mine_serial_number
    pin: _mines_pb2.mine_pin
    def __init__(self, num: _Optional[_Union[_rovers_pb2.rover_number, _Mapping]] = ..., serial_number: _Optional[_Union[_mines_pb2.mine_serial_number, _Mapping]] = ..., pin: _Optional[_Union[_mines_pb2.mine_pin, _Mapping]] = ...) -> None: ...
