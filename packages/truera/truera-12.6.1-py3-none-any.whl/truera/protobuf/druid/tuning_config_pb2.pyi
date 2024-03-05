from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GeneralTuningConfig(_message.Message):
    __slots__ = ("max_rows_in_memory", "max_bytes_in_memory")
    MAX_ROWS_IN_MEMORY_FIELD_NUMBER: _ClassVar[int]
    MAX_BYTES_IN_MEMORY_FIELD_NUMBER: _ClassVar[int]
    max_rows_in_memory: int
    max_bytes_in_memory: int
    def __init__(self, max_rows_in_memory: _Optional[int] = ..., max_bytes_in_memory: _Optional[int] = ...) -> None: ...
