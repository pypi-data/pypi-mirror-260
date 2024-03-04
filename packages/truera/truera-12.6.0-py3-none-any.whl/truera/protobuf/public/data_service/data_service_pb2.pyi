from google.api import annotations_pb2 as _annotations_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from truera.protobuf.public.common import data_kind_pb2 as _data_kind_pb2
from truera.protobuf.public.common import row_pb2 as _row_pb2
from truera.protobuf.public.common import schema_pb2 as _schema_pb2
from truera.protobuf.public.data import filter_pb2 as _filter_pb2
from truera.protobuf.public.data_service import data_service_messages_pb2 as _data_service_messages_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataServicePingRequest(_message.Message):
    __slots__ = ("ping_string",)
    PING_STRING_FIELD_NUMBER: _ClassVar[int]
    ping_string: str
    def __init__(self, ping_string: _Optional[str] = ...) -> None: ...

class DataServicePingResponse(_message.Message):
    __slots__ = ("ping_response",)
    PING_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ping_response: str
    def __init__(self, ping_response: _Optional[str] = ...) -> None: ...

class GetAwsAccountIdRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAwsAccountIdResponse(_message.Message):
    __slots__ = ("aws_account_id",)
    AWS_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    aws_account_id: str
    def __init__(self, aws_account_id: _Optional[str] = ...) -> None: ...

class PutCredentialRequest(_message.Message):
    __slots__ = ("credentials", "replace_if_exists")
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    REPLACE_IF_EXISTS_FIELD_NUMBER: _ClassVar[int]
    credentials: _data_service_messages_pb2.Credentials
    replace_if_exists: bool
    def __init__(self, credentials: _Optional[_Union[_data_service_messages_pb2.Credentials, _Mapping]] = ..., replace_if_exists: bool = ...) -> None: ...

class PutCredentialResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetCredentialMetadataRequest(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class GetCredentialMetadataResponse(_message.Message):
    __slots__ = ("credential_metadata",)
    CREDENTIAL_METADATA_FIELD_NUMBER: _ClassVar[int]
    credential_metadata: _data_service_messages_pb2.CredentialMetadata
    def __init__(self, credential_metadata: _Optional[_Union[_data_service_messages_pb2.CredentialMetadata, _Mapping]] = ...) -> None: ...

class DeleteCredentialRequest(_message.Message):
    __slots__ = ("id_to_delete",)
    ID_TO_DELETE_FIELD_NUMBER: _ClassVar[int]
    id_to_delete: str
    def __init__(self, id_to_delete: _Optional[str] = ...) -> None: ...

class DeleteCredentialResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LoadDataRequest(_message.Message):
    __slots__ = ("data_source_info",)
    DATA_SOURCE_INFO_FIELD_NUMBER: _ClassVar[int]
    data_source_info: _data_service_messages_pb2.LoadDataInfo
    def __init__(self, data_source_info: _Optional[_Union[_data_service_messages_pb2.LoadDataInfo, _Mapping]] = ...) -> None: ...

class RowsetStatusResponse(_message.Message):
    __slots__ = ("rowset_id", "rowset_state")
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    ROWSET_STATE_FIELD_NUMBER: _ClassVar[int]
    rowset_id: str
    rowset_state: _data_service_messages_pb2.RowsetState
    def __init__(self, rowset_id: _Optional[str] = ..., rowset_state: _Optional[_Union[_data_service_messages_pb2.RowsetState, _Mapping]] = ...) -> None: ...

class StartStreamingIngestionRequest(_message.Message):
    __slots__ = ("input_topic_name", "project_id", "data_collection_id")
    INPUT_TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    input_topic_name: str
    project_id: str
    data_collection_id: str
    def __init__(self, input_topic_name: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ...) -> None: ...

class StartStreamingIngestionResponse(_message.Message):
    __slots__ = ("streaming_ingestion_id", "token")
    STREAMING_INGESTION_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    streaming_ingestion_id: str
    token: str
    def __init__(self, streaming_ingestion_id: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class GetStreamingIngestionStatusRequest(_message.Message):
    __slots__ = ("streaming_ingestion_id",)
    STREAMING_INGESTION_ID_FIELD_NUMBER: _ClassVar[int]
    streaming_ingestion_id: str
    def __init__(self, streaming_ingestion_id: _Optional[str] = ...) -> None: ...

class GetStreamingIngestionStatusResponse(_message.Message):
    __slots__ = ("streaming_ingestion_id",)
    STREAMING_INGESTION_ID_FIELD_NUMBER: _ClassVar[int]
    streaming_ingestion_id: str
    def __init__(self, streaming_ingestion_id: _Optional[str] = ...) -> None: ...

class StopStreamingIngestionRequest(_message.Message):
    __slots__ = ("streaming_ingestion_id", "project_id")
    STREAMING_INGESTION_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    streaming_ingestion_id: str
    project_id: str
    def __init__(self, streaming_ingestion_id: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...

class StopStreamingIngestionResponse(_message.Message):
    __slots__ = ("streaming_ingestion_id",)
    STREAMING_INGESTION_ID_FIELD_NUMBER: _ClassVar[int]
    streaming_ingestion_id: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, streaming_ingestion_id: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteRowsetRequest(_message.Message):
    __slots__ = ("rowset_id", "including_children")
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDING_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    rowset_id: str
    including_children: bool
    def __init__(self, rowset_id: _Optional[str] = ..., including_children: bool = ...) -> None: ...

class DeleteRowsetResponse(_message.Message):
    __slots__ = ("deleted_rowset_ids",)
    DELETED_ROWSET_IDS_FIELD_NUMBER: _ClassVar[int]
    deleted_rowset_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, deleted_rowset_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteMaterializeOperationRequest(_message.Message):
    __slots__ = ("materialize_operation_id",)
    MATERIALIZE_OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    materialize_operation_id: str
    def __init__(self, materialize_operation_id: _Optional[str] = ...) -> None: ...

class DeleteMaterializeOperationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetRowsetStatusRequest(_message.Message):
    __slots__ = ("rowset_id", "data_source_name", "project_id")
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    rowset_id: str
    data_source_name: str
    project_id: str
    def __init__(self, rowset_id: _Optional[str] = ..., data_source_name: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...

class GetRowsetMetadataRequest(_message.Message):
    __slots__ = ("rowset_id",)
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    rowset_id: str
    def __init__(self, rowset_id: _Optional[str] = ...) -> None: ...

class GetRowsetMetadataResponse(_message.Message):
    __slots__ = ("rowset",)
    ROWSET_FIELD_NUMBER: _ClassVar[int]
    rowset: _data_service_messages_pb2.Rowset
    def __init__(self, rowset: _Optional[_Union[_data_service_messages_pb2.Rowset, _Mapping]] = ...) -> None: ...

class ApplyFilterRequest(_message.Message):
    __slots__ = ("rowset_id", "project_id", "filter")
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    rowset_id: str
    project_id: str
    filter: _filter_pb2.FilterExpression
    def __init__(self, rowset_id: _Optional[str] = ..., project_id: _Optional[str] = ..., filter: _Optional[_Union[_filter_pb2.FilterExpression, _Mapping]] = ...) -> None: ...

class RowsetResponse(_message.Message):
    __slots__ = ("rowset_id",)
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    rowset_id: str
    def __init__(self, rowset_id: _Optional[str] = ...) -> None: ...

class GetRowsetColumnsRequest(_message.Message):
    __slots__ = ("rowset_id", "project_id")
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    rowset_id: str
    project_id: str
    def __init__(self, rowset_id: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...

class GetRowsetColumnsRequestResponse(_message.Message):
    __slots__ = ("columns", "error", "status")
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.RepeatedCompositeFieldContainer[_schema_pb2.ColumnDetails]
    error: str
    status: _data_service_messages_pb2.RowsetStatus
    def __init__(self, columns: _Optional[_Iterable[_Union[_schema_pb2.ColumnDetails, _Mapping]]] = ..., error: _Optional[str] = ..., status: _Optional[_Union[_data_service_messages_pb2.RowsetStatus, str]] = ...) -> None: ...

class GetRowsRequest(_message.Message):
    __slots__ = ("rowset_id", "project_id", "count")
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    rowset_id: str
    project_id: str
    count: int
    def __init__(self, rowset_id: _Optional[str] = ..., project_id: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class GetRowsResponse(_message.Message):
    __slots__ = ("schema", "rows", "status", "error")
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    schema: _containers.RepeatedCompositeFieldContainer[_schema_pb2.ColumnDetails]
    rows: _containers.RepeatedCompositeFieldContainer[_row_pb2.Row]
    status: _data_service_messages_pb2.RowsetStatus
    error: str
    def __init__(self, schema: _Optional[_Iterable[_Union[_schema_pb2.ColumnDetails, _Mapping]]] = ..., rows: _Optional[_Iterable[_Union[_row_pb2.Row, _Mapping]]] = ..., status: _Optional[_Union[_data_service_messages_pb2.RowsetStatus, str]] = ..., error: _Optional[str] = ...) -> None: ...

class JoinRequest(_message.Message):
    __slots__ = ("rowsets", "perform_column_rename", "join_type")
    ROWSETS_FIELD_NUMBER: _ClassVar[int]
    PERFORM_COLUMN_RENAME_FIELD_NUMBER: _ClassVar[int]
    JOIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    rowsets: _containers.RepeatedCompositeFieldContainer[_data_service_messages_pb2.RowsetWithId]
    perform_column_rename: bool
    join_type: _data_service_messages_pb2.JoinType
    def __init__(self, rowsets: _Optional[_Iterable[_Union[_data_service_messages_pb2.RowsetWithId, _Mapping]]] = ..., perform_column_rename: bool = ..., join_type: _Optional[_Union[_data_service_messages_pb2.JoinType, str]] = ...) -> None: ...

class CreateEmptySplitRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "split_name")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    split_name: str
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., split_name: _Optional[str] = ...) -> None: ...

class CreateEmptySplitResponse(_message.Message):
    __slots__ = ("split_id",)
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    split_id: str
    def __init__(self, split_id: _Optional[str] = ...) -> None: ...

class MaterializeDataRequest(_message.Message):
    __slots__ = ("rowset_id", "idempotency_id", "sample_strategy", "approx_max_rows", "sample_seed", "data_info", "uniquified_columns_expected")
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_ID_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    APPROX_MAX_ROWS_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_SEED_FIELD_NUMBER: _ClassVar[int]
    DATA_INFO_FIELD_NUMBER: _ClassVar[int]
    UNIQUIFIED_COLUMNS_EXPECTED_FIELD_NUMBER: _ClassVar[int]
    rowset_id: str
    idempotency_id: str
    sample_strategy: _data_service_messages_pb2.SampleStrategy
    approx_max_rows: int
    sample_seed: int
    data_info: _data_service_messages_pb2.MaterializeDataInfo
    uniquified_columns_expected: bool
    def __init__(self, rowset_id: _Optional[str] = ..., idempotency_id: _Optional[str] = ..., sample_strategy: _Optional[_Union[_data_service_messages_pb2.SampleStrategy, str]] = ..., approx_max_rows: _Optional[int] = ..., sample_seed: _Optional[int] = ..., data_info: _Optional[_Union[_data_service_messages_pb2.MaterializeDataInfo, _Mapping]] = ..., uniquified_columns_expected: bool = ...) -> None: ...

class MaterializeDataResponse(_message.Message):
    __slots__ = ("materialize_operation_id", "idempotency_id", "rowset_id", "project_id", "output_split_data_collection_id", "output_split_id", "output_split_name", "operation_started_time", "output_size_kb", "status", "error", "original_request")
    MATERIALIZE_OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_ID_FIELD_NUMBER: _ClassVar[int]
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SPLIT_DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    OPERATION_STARTED_TIME_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SIZE_KB_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    materialize_operation_id: str
    idempotency_id: str
    rowset_id: str
    project_id: str
    output_split_data_collection_id: str
    output_split_id: str
    output_split_name: str
    operation_started_time: _timestamp_pb2.Timestamp
    output_size_kb: int
    status: _data_service_messages_pb2.MaterializeStatus
    error: str
    original_request: MaterializeDataRequest
    def __init__(self, materialize_operation_id: _Optional[str] = ..., idempotency_id: _Optional[str] = ..., rowset_id: _Optional[str] = ..., project_id: _Optional[str] = ..., output_split_data_collection_id: _Optional[str] = ..., output_split_id: _Optional[str] = ..., output_split_name: _Optional[str] = ..., operation_started_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., output_size_kb: _Optional[int] = ..., status: _Optional[_Union[_data_service_messages_pb2.MaterializeStatus, str]] = ..., error: _Optional[str] = ..., original_request: _Optional[_Union[MaterializeDataRequest, _Mapping]] = ...) -> None: ...

class GetMaterializeDataStatusRequest(_message.Message):
    __slots__ = ("materialize_operation_id", "project_id", "idempotency_id")
    MATERIALIZE_OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_ID_FIELD_NUMBER: _ClassVar[int]
    materialize_operation_id: str
    project_id: str
    idempotency_id: str
    def __init__(self, materialize_operation_id: _Optional[str] = ..., project_id: _Optional[str] = ..., idempotency_id: _Optional[str] = ...) -> None: ...

class GetCredentialsRequest(_message.Message):
    __slots__ = ("project_id", "last_key", "limit")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_KEY_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    last_key: str
    limit: int
    def __init__(self, project_id: _Optional[str] = ..., last_key: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class GetCredentialsResponse(_message.Message):
    __slots__ = ("credential_metadata", "has_more_data")
    CREDENTIAL_METADATA_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_DATA_FIELD_NUMBER: _ClassVar[int]
    credential_metadata: _containers.RepeatedCompositeFieldContainer[_data_service_messages_pb2.CredentialMetadata]
    has_more_data: bool
    def __init__(self, credential_metadata: _Optional[_Iterable[_Union[_data_service_messages_pb2.CredentialMetadata, _Mapping]]] = ..., has_more_data: bool = ...) -> None: ...

class GetRowsetsRequest(_message.Message):
    __slots__ = ("project_id", "root_rowset_id", "only_root_rowsets", "only_with_creation_reasons", "last_key", "limit")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ROOT_ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    ONLY_ROOT_ROWSETS_FIELD_NUMBER: _ClassVar[int]
    ONLY_WITH_CREATION_REASONS_FIELD_NUMBER: _ClassVar[int]
    LAST_KEY_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    root_rowset_id: str
    only_root_rowsets: bool
    only_with_creation_reasons: _containers.RepeatedScalarFieldContainer[_data_service_messages_pb2.CreationReason]
    last_key: str
    limit: int
    def __init__(self, project_id: _Optional[str] = ..., root_rowset_id: _Optional[str] = ..., only_root_rowsets: bool = ..., only_with_creation_reasons: _Optional[_Iterable[_Union[_data_service_messages_pb2.CreationReason, str]]] = ..., last_key: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class GetRowsetsResponse(_message.Message):
    __slots__ = ("rowsets", "has_more_data")
    ROWSETS_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_DATA_FIELD_NUMBER: _ClassVar[int]
    rowsets: _containers.RepeatedCompositeFieldContainer[_data_service_messages_pb2.RowsetMetadata]
    has_more_data: bool
    def __init__(self, rowsets: _Optional[_Iterable[_Union[_data_service_messages_pb2.RowsetMetadata, _Mapping]]] = ..., has_more_data: bool = ...) -> None: ...

class SchemaToRegister(_message.Message):
    __slots__ = ("columns", "data_kind")
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    DATA_KIND_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.RepeatedCompositeFieldContainer[_schema_pb2.ColumnDetails]
    data_kind: _data_kind_pb2.DataKindDescribed
    def __init__(self, columns: _Optional[_Iterable[_Union[_schema_pb2.ColumnDetails, _Mapping]]] = ..., data_kind: _Optional[_Union[_data_kind_pb2.DataKindDescribed, str]] = ...) -> None: ...

class RegisterSchemaRequest(_message.Message):
    __slots__ = ("schemas", "project_id", "data_collection_id", "force", "start_streaming")
    SCHEMAS_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    START_STREAMING_FIELD_NUMBER: _ClassVar[int]
    schemas: _containers.RepeatedCompositeFieldContainer[SchemaToRegister]
    project_id: str
    data_collection_id: str
    force: bool
    start_streaming: bool
    def __init__(self, schemas: _Optional[_Iterable[_Union[SchemaToRegister, _Mapping]]] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., force: bool = ..., start_streaming: bool = ...) -> None: ...

class RegisterSchemaResponse(_message.Message):
    __slots__ = ("schemas",)
    SCHEMAS_FIELD_NUMBER: _ClassVar[int]
    schemas: _containers.RepeatedCompositeFieldContainer[_schema_pb2.Schema]
    def __init__(self, schemas: _Optional[_Iterable[_Union[_schema_pb2.Schema, _Mapping]]] = ...) -> None: ...

class GetSchemaRequest(_message.Message):
    __slots__ = ("schema_id",)
    SCHEMA_ID_FIELD_NUMBER: _ClassVar[int]
    schema_id: str
    def __init__(self, schema_id: _Optional[str] = ...) -> None: ...

class GetSchemaResponse(_message.Message):
    __slots__ = ("schema",)
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    schema: _schema_pb2.Schema
    def __init__(self, schema: _Optional[_Union[_schema_pb2.Schema, _Mapping]] = ...) -> None: ...

class DeleteSchemaRequest(_message.Message):
    __slots__ = ("schema_id", "force")
    SCHEMA_ID_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    schema_id: str
    force: bool
    def __init__(self, schema_id: _Optional[str] = ..., force: bool = ...) -> None: ...

class DeleteSchemaResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetMaterializeOperationsRequest(_message.Message):
    __slots__ = ("project_id", "root_rowset_id", "filter_to_operations_with_status", "last_key", "limit")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ROOT_ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    FILTER_TO_OPERATIONS_WITH_STATUS_FIELD_NUMBER: _ClassVar[int]
    LAST_KEY_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    root_rowset_id: str
    filter_to_operations_with_status: _data_service_messages_pb2.MaterializeStatus
    last_key: str
    limit: int
    def __init__(self, project_id: _Optional[str] = ..., root_rowset_id: _Optional[str] = ..., filter_to_operations_with_status: _Optional[_Union[_data_service_messages_pb2.MaterializeStatus, str]] = ..., last_key: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class GetMaterializeOperationsResponse(_message.Message):
    __slots__ = ("materialize_operations", "has_more_data")
    MATERIALIZE_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_DATA_FIELD_NUMBER: _ClassVar[int]
    materialize_operations: _containers.RepeatedCompositeFieldContainer[_data_service_messages_pb2.MaterializedIdAndStatus]
    has_more_data: bool
    def __init__(self, materialize_operations: _Optional[_Iterable[_Union[_data_service_messages_pb2.MaterializedIdAndStatus, _Mapping]]] = ..., has_more_data: bool = ...) -> None: ...

class DeleteIcebergDataRequest(_message.Message):
    __slots__ = ("tenant_id",)
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    def __init__(self, tenant_id: _Optional[str] = ...) -> None: ...

class DeleteIcebergDataResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
