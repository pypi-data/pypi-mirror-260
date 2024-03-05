from google.protobuf import timestamp_pb2 as _timestamp_pb2
from truera.protobuf.public import common_pb2 as _common_pb2
from truera.protobuf.public.data_service import data_service_pb2 as _data_service_pb2
from truera.protobuf.public.data_service import data_service_messages_pb2 as _data_service_messages_pb2
from truera.protobuf.public.common import livy_pb2 as _livy_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LivySessionMetadata(_message.Message):
    __slots__ = ("session_id", "session_details", "created_on", "last_active", "expired_on")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_DETAILS_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    LAST_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    EXPIRED_ON_FIELD_NUMBER: _ClassVar[int]
    session_id: int
    session_details: _livy_pb2.LivyCreateSessionRequest
    created_on: _timestamp_pb2.Timestamp
    last_active: _timestamp_pb2.Timestamp
    expired_on: _timestamp_pb2.Timestamp
    def __init__(self, session_id: _Optional[int] = ..., session_details: _Optional[_Union[_livy_pb2.LivyCreateSessionRequest, _Mapping]] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_active: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., expired_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class LivyMaterializeOperation(_message.Message):
    __slots__ = ("operation_id", "idempotency_id", "materialize", "rowset_id", "started_on", "output_split_id", "outputs", "finished_on", "result", "failed_on", "error")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_ID_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZE_FIELD_NUMBER: _ClassVar[int]
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    STARTED_ON_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    FINISHED_ON_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    FAILED_ON_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    idempotency_id: str
    materialize: _data_service_pb2.MaterializeDataRequest
    rowset_id: str
    started_on: _timestamp_pb2.Timestamp
    output_split_id: str
    outputs: _containers.RepeatedCompositeFieldContainer[_data_service_messages_pb2.OutputOperationMetadata]
    finished_on: _timestamp_pb2.Timestamp
    result: _data_service_messages_pb2.MaterializeResult
    failed_on: _timestamp_pb2.Timestamp
    error: str
    def __init__(self, operation_id: _Optional[str] = ..., idempotency_id: _Optional[str] = ..., materialize: _Optional[_Union[_data_service_pb2.MaterializeDataRequest, _Mapping]] = ..., rowset_id: _Optional[str] = ..., started_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., output_split_id: _Optional[str] = ..., outputs: _Optional[_Iterable[_Union[_data_service_messages_pb2.OutputOperationMetadata, _Mapping]]] = ..., finished_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., result: _Optional[_Union[_data_service_messages_pb2.MaterializeResult, _Mapping]] = ..., failed_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., error: _Optional[str] = ...) -> None: ...

class FilterColumn(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class DataDeletionContainer(_message.Message):
    __slots__ = ("tableInfo", "filterColumn")
    TABLEINFO_FIELD_NUMBER: _ClassVar[int]
    FILTERCOLUMN_FIELD_NUMBER: _ClassVar[int]
    tableInfo: _common_pb2.TableLocationInfo
    filterColumn: FilterColumn
    def __init__(self, tableInfo: _Optional[_Union[_common_pb2.TableLocationInfo, _Mapping]] = ..., filterColumn: _Optional[_Union[FilterColumn, _Mapping]] = ...) -> None: ...

class DataDeletionContainerList(_message.Message):
    __slots__ = ("deletes",)
    DELETES_FIELD_NUMBER: _ClassVar[int]
    deletes: _containers.RepeatedCompositeFieldContainer[DataDeletionContainer]
    def __init__(self, deletes: _Optional[_Iterable[_Union[DataDeletionContainer, _Mapping]]] = ...) -> None: ...
