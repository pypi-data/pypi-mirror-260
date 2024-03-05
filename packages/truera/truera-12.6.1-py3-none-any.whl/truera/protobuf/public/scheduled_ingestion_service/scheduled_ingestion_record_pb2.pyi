from google.protobuf import timestamp_pb2 as _timestamp_pb2
from truera.protobuf.public.scheduled_ingestion_service import scheduled_ingestion_service_pb2 as _scheduled_ingestion_service_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduledIngestionRecord(_message.Message):
    __slots__ = ("id", "request", "project_id", "data_collection_id", "canceled_on")
    ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CANCELED_ON_FIELD_NUMBER: _ClassVar[int]
    id: str
    request: _scheduled_ingestion_service_pb2.ScheduleIngestionRequest
    project_id: str
    data_collection_id: str
    canceled_on: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., request: _Optional[_Union[_scheduled_ingestion_service_pb2.ScheduleIngestionRequest, _Mapping]] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., canceled_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
