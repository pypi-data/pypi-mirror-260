from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ModelOutputType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_MODELOUTPUTTYPE: _ClassVar[ModelOutputType]
    CLASSIFICATION: _ClassVar[ModelOutputType]
    REGRESSION: _ClassVar[ModelOutputType]
    RANKING: _ClassVar[ModelOutputType]
    TEXT_OUTPUT: _ClassVar[ModelOutputType]
UNKNOWN_MODELOUTPUTTYPE: ModelOutputType
CLASSIFICATION: ModelOutputType
REGRESSION: ModelOutputType
RANKING: ModelOutputType
TEXT_OUTPUT: ModelOutputType
