from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class DataKindDescribed(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATA_KIND_INVALID: _ClassVar[DataKindDescribed]
    DATA_KIND_PRE: _ClassVar[DataKindDescribed]
    DATA_KIND_POST: _ClassVar[DataKindDescribed]
    DATA_KIND_EXTRA: _ClassVar[DataKindDescribed]
    DATA_KIND_LABEL: _ClassVar[DataKindDescribed]
    DATA_KIND_PREDICTIONS: _ClassVar[DataKindDescribed]
    DATA_KIND_FEATURE_INFLUENCES: _ClassVar[DataKindDescribed]
    DATA_KIND_ALL: _ClassVar[DataKindDescribed]
    DATA_KIND_SCHEMA_MISMATCH_PRE: _ClassVar[DataKindDescribed]
    DATA_KIND_SCHEMA_MISMATCH_POST: _ClassVar[DataKindDescribed]
    DATA_KIND_SCHEMA_MISMATCH_EXTRA: _ClassVar[DataKindDescribed]
    DATA_KIND_SCHEMA_MISMATCH_LABEL: _ClassVar[DataKindDescribed]
    DATA_KIND_SCHEMA_MISMATCH_PREDICTIONS: _ClassVar[DataKindDescribed]
    DATA_KIND_SCHEMA_MISMATCH_FEATURE_INFLUENCES: _ClassVar[DataKindDescribed]
    DATA_KIND_SCHEMA_MISMATCH_ALL: _ClassVar[DataKindDescribed]
    DATA_KIND_TRACE: _ClassVar[DataKindDescribed]
    DATA_KIND_FEEDBACK: _ClassVar[DataKindDescribed]
DATA_KIND_INVALID: DataKindDescribed
DATA_KIND_PRE: DataKindDescribed
DATA_KIND_POST: DataKindDescribed
DATA_KIND_EXTRA: DataKindDescribed
DATA_KIND_LABEL: DataKindDescribed
DATA_KIND_PREDICTIONS: DataKindDescribed
DATA_KIND_FEATURE_INFLUENCES: DataKindDescribed
DATA_KIND_ALL: DataKindDescribed
DATA_KIND_SCHEMA_MISMATCH_PRE: DataKindDescribed
DATA_KIND_SCHEMA_MISMATCH_POST: DataKindDescribed
DATA_KIND_SCHEMA_MISMATCH_EXTRA: DataKindDescribed
DATA_KIND_SCHEMA_MISMATCH_LABEL: DataKindDescribed
DATA_KIND_SCHEMA_MISMATCH_PREDICTIONS: DataKindDescribed
DATA_KIND_SCHEMA_MISMATCH_FEATURE_INFLUENCES: DataKindDescribed
DATA_KIND_SCHEMA_MISMATCH_ALL: DataKindDescribed
DATA_KIND_TRACE: DataKindDescribed
DATA_KIND_FEEDBACK: DataKindDescribed
