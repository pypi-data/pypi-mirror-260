from google.protobuf import timestamp_pb2 as _timestamp_pb2
from truera.protobuf.public.common import data_kind_pb2 as _data_kind_pb2
from truera.protobuf.public.common import data_locator_pb2 as _data_locator_pb2
from truera.protobuf.public.common import schema_pb2 as _schema_pb2
from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OutputStreamInfo(_message.Message):
    __slots__ = ("schema", "kind", "score_type", "output_data_locator", "bad_data_locator", "persistence_locator")
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_DATA_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    BAD_DATA_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    PERSISTENCE_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    schema: _schema_pb2.Schema
    kind: _data_kind_pb2.DataKindDescribed
    score_type: _qoi_pb2.QuantityOfInterest
    output_data_locator: _data_locator_pb2.DataLocator
    bad_data_locator: _data_locator_pb2.DataLocator
    persistence_locator: _data_locator_pb2.DataLocator
    def __init__(self, schema: _Optional[_Union[_schema_pb2.Schema, _Mapping]] = ..., kind: _Optional[_Union[_data_kind_pb2.DataKindDescribed, str]] = ..., score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., output_data_locator: _Optional[_Union[_data_locator_pb2.DataLocator, _Mapping]] = ..., bad_data_locator: _Optional[_Union[_data_locator_pb2.DataLocator, _Mapping]] = ..., persistence_locator: _Optional[_Union[_data_locator_pb2.DataLocator, _Mapping]] = ...) -> None: ...

class DataStreamIngestion(_message.Message):
    __slots__ = ("ingestion_id", "project_id", "data_collection_id", "output_streams", "registered_on")
    INGESTION_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_STREAMS_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_ON_FIELD_NUMBER: _ClassVar[int]
    ingestion_id: str
    project_id: str
    data_collection_id: str
    output_streams: _containers.RepeatedCompositeFieldContainer[OutputStreamInfo]
    registered_on: _timestamp_pb2.Timestamp
    def __init__(self, ingestion_id: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., output_streams: _Optional[_Iterable[_Union[OutputStreamInfo, _Mapping]]] = ..., registered_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
