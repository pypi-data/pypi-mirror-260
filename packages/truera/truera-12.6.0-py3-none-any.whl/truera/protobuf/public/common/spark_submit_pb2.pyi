from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SparkSubmitOptions(_message.Message):
    __slots__ = ("name", "className", "jarPath", "args", "jars", "packages")
    class ArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    CLASSNAME_FIELD_NUMBER: _ClassVar[int]
    JARPATH_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    JARS_FIELD_NUMBER: _ClassVar[int]
    PACKAGES_FIELD_NUMBER: _ClassVar[int]
    name: str
    className: str
    jarPath: str
    args: _containers.ScalarMap[str, str]
    jars: _containers.RepeatedScalarFieldContainer[str]
    packages: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., className: _Optional[str] = ..., jarPath: _Optional[str] = ..., args: _Optional[_Mapping[str, str]] = ..., jars: _Optional[_Iterable[str]] = ..., packages: _Optional[_Iterable[str]] = ...) -> None: ...
