from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IntArray(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class TwoDimensionalIntArray(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[IntArray]
    def __init__(self, rows: _Optional[_Iterable[_Union[IntArray, _Mapping]]] = ...) -> None: ...

class RoverNumber(_message.Message):
    __slots__ = ("number",)
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    number: int
    def __init__(self, number: _Optional[int] = ...) -> None: ...

class String(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ("statusCode", "message")
    STATUSCODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    statusCode: int
    message: str
    def __init__(self, statusCode: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class RoverNumberWithMineSerialAndPin(_message.Message):
    __slots__ = ("roverNumber", "mineSerialNumber", "minePin")
    ROVERNUMBER_FIELD_NUMBER: _ClassVar[int]
    MINESERIALNUMBER_FIELD_NUMBER: _ClassVar[int]
    MINEPIN_FIELD_NUMBER: _ClassVar[int]
    roverNumber: int
    mineSerialNumber: str
    minePin: str
    def __init__(self, roverNumber: _Optional[int] = ..., mineSerialNumber: _Optional[str] = ..., minePin: _Optional[str] = ...) -> None: ...
