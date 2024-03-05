from truera.protobuf.public.data import filter_pb2 as _filter_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BackgroundDataSplitInfo(_message.Message):
    __slots__ = ("id", "all", "index", "filter_expression")
    ID_FIELD_NUMBER: _ClassVar[int]
    ALL_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    FILTER_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    id: str
    all: bool
    index: int
    filter_expression: _filter_pb2.FilterExpression
    def __init__(self, id: _Optional[str] = ..., all: bool = ..., index: _Optional[int] = ..., filter_expression: _Optional[_Union[_filter_pb2.FilterExpression, _Mapping]] = ...) -> None: ...
