from google.api import annotations_pb2 as _annotations_pb2
from truera.protobuf.public.read_optimized_table_service import read_optimized_table_messages_pb2 as _read_optimized_table_messages_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateRotRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "split_id", "model_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    split_id: str
    model_id: str
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., split_id: _Optional[str] = ..., model_id: _Optional[str] = ...) -> None: ...

class CreateRotResponse(_message.Message):
    __slots__ = ("operation_id",)
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    def __init__(self, operation_id: _Optional[str] = ...) -> None: ...

class GetRotMetadataRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "split_id", "model_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    split_id: str
    model_id: str
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., split_id: _Optional[str] = ..., model_id: _Optional[str] = ...) -> None: ...

class GetRotMetadataResponse(_message.Message):
    __slots__ = ("rot_metadata",)
    ROT_METADATA_FIELD_NUMBER: _ClassVar[int]
    rot_metadata: _read_optimized_table_messages_pb2.RotMetadata
    def __init__(self, rot_metadata: _Optional[_Union[_read_optimized_table_messages_pb2.RotMetadata, _Mapping]] = ...) -> None: ...

class GetLatestRotOperationRequest(_message.Message):
    __slots__ = ("query_metadata",)
    QUERY_METADATA_FIELD_NUMBER: _ClassVar[int]
    query_metadata: _read_optimized_table_messages_pb2.RotQueryMetadata
    def __init__(self, query_metadata: _Optional[_Union[_read_optimized_table_messages_pb2.RotQueryMetadata, _Mapping]] = ...) -> None: ...

class GetLatestRotOperationResponse(_message.Message):
    __slots__ = ("operations_metadata",)
    OPERATIONS_METADATA_FIELD_NUMBER: _ClassVar[int]
    operations_metadata: _read_optimized_table_messages_pb2.RotOperationsMetadata
    def __init__(self, operations_metadata: _Optional[_Union[_read_optimized_table_messages_pb2.RotOperationsMetadata, _Mapping]] = ...) -> None: ...

class UpdateRotRequest(_message.Message):
    __slots__ = ("rot_id", "query_metadata")
    ROT_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_METADATA_FIELD_NUMBER: _ClassVar[int]
    rot_id: str
    query_metadata: _read_optimized_table_messages_pb2.RotQueryMetadata
    def __init__(self, rot_id: _Optional[str] = ..., query_metadata: _Optional[_Union[_read_optimized_table_messages_pb2.RotQueryMetadata, _Mapping]] = ...) -> None: ...

class UpdateRotResponse(_message.Message):
    __slots__ = ("operation_id",)
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    def __init__(self, operation_id: _Optional[str] = ...) -> None: ...
