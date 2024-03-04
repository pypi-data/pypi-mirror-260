from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectDocumentation(_message.Message):
    __slots__ = ("documentation",)
    class DocumentationEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DOCUMENTATION_FIELD_NUMBER: _ClassVar[int]
    documentation: _containers.ScalarMap[str, str]
    def __init__(self, documentation: _Optional[_Mapping[str, str]] = ...) -> None: ...
