from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from truera.protobuf.public.common import data_kind_pb2 as _data_kind_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SplitDataContentMetadata(_message.Message):
    __slots__ = ("data_kinds", "rows_written")
    DATA_KINDS_FIELD_NUMBER: _ClassVar[int]
    ROWS_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    data_kinds: _containers.RepeatedScalarFieldContainer[_data_kind_pb2.DataKindDescribed]
    rows_written: int
    def __init__(self, data_kinds: _Optional[_Iterable[_Union[_data_kind_pb2.DataKindDescribed, str]]] = ..., rows_written: _Optional[int] = ...) -> None: ...

class ModelContentMetadata(_message.Message):
    __slots__ = ("prediction_score_types", "fi_hashes", "prediction_hashes")
    PREDICTION_SCORE_TYPES_FIELD_NUMBER: _ClassVar[int]
    FI_HASHES_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_HASHES_FIELD_NUMBER: _ClassVar[int]
    prediction_score_types: _containers.RepeatedScalarFieldContainer[_qoi_pb2.QuantityOfInterest]
    fi_hashes: _containers.RepeatedScalarFieldContainer[str]
    prediction_hashes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, prediction_score_types: _Optional[_Iterable[_Union[_qoi_pb2.QuantityOfInterest, str]]] = ..., fi_hashes: _Optional[_Iterable[str]] = ..., prediction_hashes: _Optional[_Iterable[str]] = ...) -> None: ...
