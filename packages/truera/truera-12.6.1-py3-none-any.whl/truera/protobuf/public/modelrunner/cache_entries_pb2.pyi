from truera.protobuf.public.util import elementary_types_pb2 as _elementary_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PartialDependenceCache(_message.Message):
    __slots__ = ("prefeatures", "xs", "ys")
    class XsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _elementary_types_pb2.ValueList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_elementary_types_pb2.ValueList, _Mapping]] = ...) -> None: ...
    class YsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _elementary_types_pb2.FloatList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_elementary_types_pb2.FloatList, _Mapping]] = ...) -> None: ...
    PREFEATURES_FIELD_NUMBER: _ClassVar[int]
    XS_FIELD_NUMBER: _ClassVar[int]
    YS_FIELD_NUMBER: _ClassVar[int]
    prefeatures: _containers.RepeatedScalarFieldContainer[str]
    xs: _containers.MessageMap[str, _elementary_types_pb2.ValueList]
    ys: _containers.MessageMap[str, _elementary_types_pb2.FloatList]
    def __init__(self, prefeatures: _Optional[_Iterable[str]] = ..., xs: _Optional[_Mapping[str, _elementary_types_pb2.ValueList]] = ..., ys: _Optional[_Mapping[str, _elementary_types_pb2.FloatList]] = ...) -> None: ...
