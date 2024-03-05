from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class SplitMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPLIT_MODE_INVALID: _ClassVar[SplitMode]
    SPLIT_MODE_DATA_REQUIRED: _ClassVar[SplitMode]
    SPLIT_MODE_PREDS_REQUIRED: _ClassVar[SplitMode]
    SPLIT_MODE_NON_TABULAR: _ClassVar[SplitMode]
SPLIT_MODE_INVALID: SplitMode
SPLIT_MODE_DATA_REQUIRED: SplitMode
SPLIT_MODE_PREDS_REQUIRED: SplitMode
SPLIT_MODE_NON_TABULAR: SplitMode
