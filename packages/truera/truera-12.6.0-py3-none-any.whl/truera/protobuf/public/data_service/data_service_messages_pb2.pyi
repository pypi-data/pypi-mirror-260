from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2
from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from truera.protobuf.public.common import data_kind_pb2 as _data_kind_pb2
from truera.protobuf.public.common import row_pb2 as _row_pb2
from truera.protobuf.public.common import schema_pb2 as _schema_pb2
from truera.protobuf.public.common import data_locator_pb2 as _data_locator_pb2
from truera.protobuf.public.data import filter_pb2 as _filter_pb2
from truera.protobuf.public.util import split_mode_pb2 as _split_mode_pb2
from truera.protobuf.public.util import time_range_pb2 as _time_range_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from truera.protobuf.public import common_pb2 as _common_pb2
from truera.protobuf.public import model_output_type_pb2 as _model_output_type_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreationReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DS_CR_INVALID: _ClassVar[CreationReason]
    DS_CR_USER_REQUESTED: _ClassVar[CreationReason]
    DS_CR_SYSTEM_REQUESTED: _ClassVar[CreationReason]

class DataSourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DS_INVALID: _ClassVar[DataSourceType]
    DS_LOCAL: _ClassVar[DataSourceType]
    DS_WASB_BLOB: _ClassVar[DataSourceType]
    DS_MYSQL: _ClassVar[DataSourceType]
    DS_S3_BUCKET: _ClassVar[DataSourceType]
    DS_JDBC: _ClassVar[DataSourceType]
    DS_HIVE: _ClassVar[DataSourceType]
    DS_BIGQUERY: _ClassVar[DataSourceType]

class JoinType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DS_JT_INVALID: _ClassVar[JoinType]
    DS_JT_INNER: _ClassVar[JoinType]
    DS_JT_LEFT_OUTER: _ClassVar[JoinType]

class RowsetOperationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RO_INVALID: _ClassVar[RowsetOperationType]
    RO_FILTER: _ClassVar[RowsetOperationType]
    RO_JOIN: _ClassVar[RowsetOperationType]

class FileType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FT_INVALID: _ClassVar[FileType]
    FT_TEXT: _ClassVar[FileType]
    FT_PARQUET: _ClassVar[FileType]
    FT_SAGEMAKER_MONITORING_LOG: _ClassVar[FileType]

class RowsetStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RS_STATUS_INVALID: _ClassVar[RowsetStatus]
    RS_STATUS_STARTED: _ClassVar[RowsetStatus]
    RS_STATUS_OK: _ClassVar[RowsetStatus]
    RS_STATUS_FAILED: _ClassVar[RowsetStatus]

class MaterializeStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MATERIALIZE_STATUS_INVALID: _ClassVar[MaterializeStatus]
    MATERIALIZE_STATUS_PREPARING: _ClassVar[MaterializeStatus]
    MATERIALIZE_STATUS_RUNNING: _ClassVar[MaterializeStatus]
    MATERIALIZE_STATUS_SUCCEDED: _ClassVar[MaterializeStatus]
    MATERIALIZE_STATUS_FAILED: _ClassVar[MaterializeStatus]

class SampleStrategy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SAMPLE_INVALID: _ClassVar[SampleStrategy]
    SAMPLE_FIRST_N: _ClassVar[SampleStrategy]
    SAMPLE_RANDOM: _ClassVar[SampleStrategy]
DS_CR_INVALID: CreationReason
DS_CR_USER_REQUESTED: CreationReason
DS_CR_SYSTEM_REQUESTED: CreationReason
DS_INVALID: DataSourceType
DS_LOCAL: DataSourceType
DS_WASB_BLOB: DataSourceType
DS_MYSQL: DataSourceType
DS_S3_BUCKET: DataSourceType
DS_JDBC: DataSourceType
DS_HIVE: DataSourceType
DS_BIGQUERY: DataSourceType
DS_JT_INVALID: JoinType
DS_JT_INNER: JoinType
DS_JT_LEFT_OUTER: JoinType
RO_INVALID: RowsetOperationType
RO_FILTER: RowsetOperationType
RO_JOIN: RowsetOperationType
FT_INVALID: FileType
FT_TEXT: FileType
FT_PARQUET: FileType
FT_SAGEMAKER_MONITORING_LOG: FileType
RS_STATUS_INVALID: RowsetStatus
RS_STATUS_STARTED: RowsetStatus
RS_STATUS_OK: RowsetStatus
RS_STATUS_FAILED: RowsetStatus
MATERIALIZE_STATUS_INVALID: MaterializeStatus
MATERIALIZE_STATUS_PREPARING: MaterializeStatus
MATERIALIZE_STATUS_RUNNING: MaterializeStatus
MATERIALIZE_STATUS_SUCCEDED: MaterializeStatus
MATERIALIZE_STATUS_FAILED: MaterializeStatus
SAMPLE_INVALID: SampleStrategy
SAMPLE_FIRST_N: SampleStrategy
SAMPLE_RANDOM: SampleStrategy

class LoadDataInfo(_message.Message):
    __slots__ = ("name", "description", "project_id", "data_collection_id", "describes_file_kind", "creation_reason", "type", "uri", "credentials", "credential_id", "format", "db_info", "file_time_range")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIBES_FILE_KIND_FIELD_NUMBER: _ClassVar[int]
    CREATION_REASON_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    DB_INFO_FIELD_NUMBER: _ClassVar[int]
    FILE_TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    project_id: str
    data_collection_id: str
    describes_file_kind: _data_kind_pb2.DataKindDescribed
    creation_reason: CreationReason
    type: DataSourceType
    uri: str
    credentials: Credentials
    credential_id: str
    format: Format
    db_info: DatabaseInfo
    file_time_range: _time_range_pb2.TimeRange
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., describes_file_kind: _Optional[_Union[_data_kind_pb2.DataKindDescribed, str]] = ..., creation_reason: _Optional[_Union[CreationReason, str]] = ..., type: _Optional[_Union[DataSourceType, str]] = ..., uri: _Optional[str] = ..., credentials: _Optional[_Union[Credentials, _Mapping]] = ..., credential_id: _Optional[str] = ..., format: _Optional[_Union[Format, _Mapping]] = ..., db_info: _Optional[_Union[DatabaseInfo, _Mapping]] = ..., file_time_range: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ...) -> None: ...

class Rowset(_message.Message):
    __slots__ = ("id", "root_data", "description", "immediate_parent_id", "root_rowset_id", "is_root", "op_type", "filter", "join_details", "created_at", "name", "project_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    ROOT_DATA_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IMMEDIATE_PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    ROOT_ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    IS_ROOT_FIELD_NUMBER: _ClassVar[int]
    OP_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    JOIN_DETAILS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    root_data: _containers.RepeatedCompositeFieldContainer[LoadDataInfo]
    description: str
    immediate_parent_id: _containers.RepeatedScalarFieldContainer[str]
    root_rowset_id: _containers.RepeatedScalarFieldContainer[str]
    is_root: bool
    op_type: RowsetOperationType
    filter: _filter_pb2.FilterExpression
    join_details: JoinDetails
    created_at: _timestamp_pb2.Timestamp
    name: str
    project_id: str
    def __init__(self, id: _Optional[str] = ..., root_data: _Optional[_Iterable[_Union[LoadDataInfo, _Mapping]]] = ..., description: _Optional[str] = ..., immediate_parent_id: _Optional[_Iterable[str]] = ..., root_rowset_id: _Optional[_Iterable[str]] = ..., is_root: bool = ..., op_type: _Optional[_Union[RowsetOperationType, str]] = ..., filter: _Optional[_Union[_filter_pb2.FilterExpression, _Mapping]] = ..., join_details: _Optional[_Union[JoinDetails, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., name: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...

class RowsetWithId(_message.Message):
    __slots__ = ("rowset_id", "id_column", "join_type", "delimited_format")
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    ID_COLUMN_FIELD_NUMBER: _ClassVar[int]
    JOIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    DELIMITED_FORMAT_FIELD_NUMBER: _ClassVar[int]
    rowset_id: str
    id_column: _containers.RepeatedScalarFieldContainer[str]
    join_type: JoinType
    delimited_format: FormatOptions
    def __init__(self, rowset_id: _Optional[str] = ..., id_column: _Optional[_Iterable[str]] = ..., join_type: _Optional[_Union[JoinType, str]] = ..., delimited_format: _Optional[_Union[FormatOptions, _Mapping]] = ...) -> None: ...

class JoinDetails(_message.Message):
    __slots__ = ("join_type", "perform_column_rename", "join_inputs")
    JOIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    PERFORM_COLUMN_RENAME_FIELD_NUMBER: _ClassVar[int]
    JOIN_INPUTS_FIELD_NUMBER: _ClassVar[int]
    join_type: JoinType
    perform_column_rename: bool
    join_inputs: _containers.RepeatedCompositeFieldContainer[RowsetWithId]
    def __init__(self, join_type: _Optional[_Union[JoinType, str]] = ..., perform_column_rename: bool = ..., join_inputs: _Optional[_Iterable[_Union[RowsetWithId, _Mapping]]] = ...) -> None: ...

class CredentialMetadata(_message.Message):
    __slots__ = ("id", "name", "storage_key", "projects_with_access", "credential_type")
    class CredentialType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CT_UNKNOWN: _ClassVar[CredentialMetadata.CredentialType]
        CT_KEY: _ClassVar[CredentialMetadata.CredentialType]
        CT_AWS_IAM_ROLE: _ClassVar[CredentialMetadata.CredentialType]
    CT_UNKNOWN: CredentialMetadata.CredentialType
    CT_KEY: CredentialMetadata.CredentialType
    CT_AWS_IAM_ROLE: CredentialMetadata.CredentialType
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STORAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    PROJECTS_WITH_ACCESS_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    storage_key: str
    projects_with_access: _containers.RepeatedScalarFieldContainer[str]
    credential_type: CredentialMetadata.CredentialType
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., storage_key: _Optional[str] = ..., projects_with_access: _Optional[_Iterable[str]] = ..., credential_type: _Optional[_Union[CredentialMetadata.CredentialType, str]] = ...) -> None: ...

class Credentials(_message.Message):
    __slots__ = ("identity", "secret", "metadata", "token")
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    identity: str
    secret: str
    metadata: CredentialMetadata
    token: str
    def __init__(self, identity: _Optional[str] = ..., secret: _Optional[str] = ..., metadata: _Optional[_Union[CredentialMetadata, _Mapping]] = ..., token: _Optional[str] = ...) -> None: ...

class Format(_message.Message):
    __slots__ = ("file_type", "delimited_format", "columns")
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DELIMITED_FORMAT_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    file_type: FileType
    delimited_format: FormatOptions
    columns: _containers.RepeatedCompositeFieldContainer[_schema_pb2.ColumnDetails]
    def __init__(self, file_type: _Optional[_Union[FileType, str]] = ..., delimited_format: _Optional[_Union[FormatOptions, _Mapping]] = ..., columns: _Optional[_Iterable[_Union[_schema_pb2.ColumnDetails, _Mapping]]] = ...) -> None: ...

class DatabaseInfo(_message.Message):
    __slots__ = ("database_name", "table_name", "columns")
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    table_name: str
    columns: _containers.RepeatedCompositeFieldContainer[_schema_pb2.ColumnDetails]
    def __init__(self, database_name: _Optional[str] = ..., table_name: _Optional[str] = ..., columns: _Optional[_Iterable[_Union[_schema_pb2.ColumnDetails, _Mapping]]] = ...) -> None: ...

class FormatOptions(_message.Message):
    __slots__ = ("quote_character", "column_delimiter", "first_row_is_header", "skip_n_rows", "date_format", "date_time_format", "null_value", "empty_value")
    QUOTE_CHARACTER_FIELD_NUMBER: _ClassVar[int]
    COLUMN_DELIMITER_FIELD_NUMBER: _ClassVar[int]
    FIRST_ROW_IS_HEADER_FIELD_NUMBER: _ClassVar[int]
    SKIP_N_ROWS_FIELD_NUMBER: _ClassVar[int]
    DATE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    DATE_TIME_FORMAT_FIELD_NUMBER: _ClassVar[int]
    NULL_VALUE_FIELD_NUMBER: _ClassVar[int]
    EMPTY_VALUE_FIELD_NUMBER: _ClassVar[int]
    quote_character: str
    column_delimiter: str
    first_row_is_header: bool
    skip_n_rows: int
    date_format: str
    date_time_format: str
    null_value: str
    empty_value: str
    def __init__(self, quote_character: _Optional[str] = ..., column_delimiter: _Optional[str] = ..., first_row_is_header: bool = ..., skip_n_rows: _Optional[int] = ..., date_format: _Optional[str] = ..., date_time_format: _Optional[str] = ..., null_value: _Optional[str] = ..., empty_value: _Optional[str] = ...) -> None: ...

class ProjectionColumnCollection(_message.Message):
    __slots__ = ("column_metadata", "colummns_to_skip", "description", "name")
    COLUMN_METADATA_FIELD_NUMBER: _ClassVar[int]
    COLUMMNS_TO_SKIP_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    column_metadata: _containers.RepeatedCompositeFieldContainer[_schema_pb2.ColumnDetails]
    colummns_to_skip: _containers.RepeatedScalarFieldContainer[str]
    description: str
    name: str
    def __init__(self, column_metadata: _Optional[_Iterable[_Union[_schema_pb2.ColumnDetails, _Mapping]]] = ..., colummns_to_skip: _Optional[_Iterable[str]] = ..., description: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class RowsetState(_message.Message):
    __slots__ = ("name", "project_id", "status", "error", "created_at")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    name: str
    project_id: str
    status: RowsetStatus
    error: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., project_id: _Optional[str] = ..., status: _Optional[_Union[RowsetStatus, str]] = ..., error: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MaterializeDataInfo(_message.Message):
    __slots__ = ("project_id", "output_data_collection_id", "create_split_info", "existing_split_id", "cache_info", "projections", "system_columns")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_SPLIT_INFO_FIELD_NUMBER: _ClassVar[int]
    EXISTING_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    CACHE_INFO_FIELD_NUMBER: _ClassVar[int]
    PROJECTIONS_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    output_data_collection_id: str
    create_split_info: CreateSplitInfo
    existing_split_id: str
    cache_info: CreateCacheInfo
    projections: _containers.RepeatedCompositeFieldContainer[MaterializedOutputFile]
    system_columns: SystemColumnDetails
    def __init__(self, project_id: _Optional[str] = ..., output_data_collection_id: _Optional[str] = ..., create_split_info: _Optional[_Union[CreateSplitInfo, _Mapping]] = ..., existing_split_id: _Optional[str] = ..., cache_info: _Optional[_Union[CreateCacheInfo, _Mapping]] = ..., projections: _Optional[_Iterable[_Union[MaterializedOutputFile, _Mapping]]] = ..., system_columns: _Optional[_Union[SystemColumnDetails, _Mapping]] = ...) -> None: ...

class SystemColumnDetails(_message.Message):
    __slots__ = ("id_columns", "ranking_item_id_column", "ranking_group_id_column", "timestamp_column", "tags_column", "tokens_column", "embeddings_column")
    ID_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    RANKING_ITEM_ID_COLUMN_FIELD_NUMBER: _ClassVar[int]
    RANKING_GROUP_ID_COLUMN_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_COLUMN_FIELD_NUMBER: _ClassVar[int]
    TAGS_COLUMN_FIELD_NUMBER: _ClassVar[int]
    TOKENS_COLUMN_FIELD_NUMBER: _ClassVar[int]
    EMBEDDINGS_COLUMN_FIELD_NUMBER: _ClassVar[int]
    id_columns: _containers.RepeatedCompositeFieldContainer[_schema_pb2.ColumnDetails]
    ranking_item_id_column: _schema_pb2.ColumnDetails
    ranking_group_id_column: _schema_pb2.ColumnDetails
    timestamp_column: _schema_pb2.ColumnDetails
    tags_column: _schema_pb2.ColumnDetails
    tokens_column: _schema_pb2.ColumnDetails
    embeddings_column: _schema_pb2.ColumnDetails
    def __init__(self, id_columns: _Optional[_Iterable[_Union[_schema_pb2.ColumnDetails, _Mapping]]] = ..., ranking_item_id_column: _Optional[_Union[_schema_pb2.ColumnDetails, _Mapping]] = ..., ranking_group_id_column: _Optional[_Union[_schema_pb2.ColumnDetails, _Mapping]] = ..., timestamp_column: _Optional[_Union[_schema_pb2.ColumnDetails, _Mapping]] = ..., tags_column: _Optional[_Union[_schema_pb2.ColumnDetails, _Mapping]] = ..., tokens_column: _Optional[_Union[_schema_pb2.ColumnDetails, _Mapping]] = ..., embeddings_column: _Optional[_Union[_schema_pb2.ColumnDetails, _Mapping]] = ...) -> None: ...

class CreateSplitInfo(_message.Message):
    __slots__ = ("output_split_name", "output_split_description", "output_split_type", "output_split_time_range", "output_split_mode", "train_baseline_model")
    OUTPUT_SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SPLIT_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SPLIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SPLIT_TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SPLIT_MODE_FIELD_NUMBER: _ClassVar[int]
    TRAIN_BASELINE_MODEL_FIELD_NUMBER: _ClassVar[int]
    output_split_name: str
    output_split_description: str
    output_split_type: str
    output_split_time_range: _time_range_pb2.TimeRange
    output_split_mode: _split_mode_pb2.SplitMode
    train_baseline_model: bool
    def __init__(self, output_split_name: _Optional[str] = ..., output_split_description: _Optional[str] = ..., output_split_type: _Optional[str] = ..., output_split_time_range: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ..., output_split_mode: _Optional[_Union[_split_mode_pb2.SplitMode, str]] = ..., train_baseline_model: bool = ...) -> None: ...

class CreateCacheInfo(_message.Message):
    __slots__ = ("model_id", "score_type", "background_split_id", "explanation_algorithm_type")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    EXPLANATION_ALGORITHM_TYPE_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    score_type: _qoi_pb2.QuantityOfInterest
    background_split_id: str
    explanation_algorithm_type: _qoi_pb2.ExplanationAlgorithmType
    def __init__(self, model_id: _Optional[str] = ..., score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., background_split_id: _Optional[str] = ..., explanation_algorithm_type: _Optional[_Union[_qoi_pb2.ExplanationAlgorithmType, str]] = ...) -> None: ...

class MaterializedOutputFile(_message.Message):
    __slots__ = ("columns", "schema_id_for_output", "type", "input_rowset_id")
    class MaterializedFileType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MFT_INVALID: _ClassVar[MaterializedOutputFile.MaterializedFileType]
        MFT_PRETRANSFORM: _ClassVar[MaterializedOutputFile.MaterializedFileType]
        MFT_POSTTRANSFORM: _ClassVar[MaterializedOutputFile.MaterializedFileType]
        MFT_LABEL: _ClassVar[MaterializedOutputFile.MaterializedFileType]
        MFT_EXTRA: _ClassVar[MaterializedOutputFile.MaterializedFileType]
        MFT_PREDICTIONCACHE: _ClassVar[MaterializedOutputFile.MaterializedFileType]
        MFT_EXPLANATIONCACHE: _ClassVar[MaterializedOutputFile.MaterializedFileType]
    MFT_INVALID: MaterializedOutputFile.MaterializedFileType
    MFT_PRETRANSFORM: MaterializedOutputFile.MaterializedFileType
    MFT_POSTTRANSFORM: MaterializedOutputFile.MaterializedFileType
    MFT_LABEL: MaterializedOutputFile.MaterializedFileType
    MFT_EXTRA: MaterializedOutputFile.MaterializedFileType
    MFT_PREDICTIONCACHE: MaterializedOutputFile.MaterializedFileType
    MFT_EXPLANATIONCACHE: MaterializedOutputFile.MaterializedFileType
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_ID_FOR_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INPUT_ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    columns: ProjectionColumnCollection
    schema_id_for_output: str
    type: MaterializedOutputFile.MaterializedFileType
    input_rowset_id: str
    def __init__(self, columns: _Optional[_Union[ProjectionColumnCollection, _Mapping]] = ..., schema_id_for_output: _Optional[str] = ..., type: _Optional[_Union[MaterializedOutputFile.MaterializedFileType, str]] = ..., input_rowset_id: _Optional[str] = ...) -> None: ...

class MaterializedIdAndStatus(_message.Message):
    __slots__ = ("id", "status", "error")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: MaterializeStatus
    error: str
    def __init__(self, id: _Optional[str] = ..., status: _Optional[_Union[MaterializeStatus, str]] = ..., error: _Optional[str] = ...) -> None: ...

class RowsetMetadata(_message.Message):
    __slots__ = ("rowset", "status", "error")
    ROWSET_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    rowset: Rowset
    status: RowsetStatus
    error: str
    def __init__(self, rowset: _Optional[_Union[Rowset, _Mapping]] = ..., status: _Optional[_Union[RowsetStatus, str]] = ..., error: _Optional[str] = ...) -> None: ...

class OutputOperationMetadata(_message.Message):
    __slots__ = ("outputs", "schema_mismatch_kafka_output", "schema_mismatch_iceberg_output", "output_file", "unique_columns_expected", "id_column_name", "ranking_item_id_column_name", "ranking_group_id_column_name", "tags_column_name", "timestamp_column_name", "tokens_column_name", "embeddings_column_name", "model_output_type", "score_type", "model_id", "options_hash", "write_time", "split_type")
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_MISMATCH_KAFKA_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_MISMATCH_ICEBERG_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FILE_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_COLUMNS_EXPECTED_FIELD_NUMBER: _ClassVar[int]
    ID_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    RANKING_ITEM_ID_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    RANKING_GROUP_ID_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    TOKENS_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    EMBEDDINGS_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_HASH_FIELD_NUMBER: _ClassVar[int]
    WRITE_TIME_FIELD_NUMBER: _ClassVar[int]
    SPLIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    outputs: _containers.RepeatedCompositeFieldContainer[OutputFileInfo]
    schema_mismatch_kafka_output: OutputFileInfo
    schema_mismatch_iceberg_output: OutputFileInfo
    output_file: MaterializedOutputFile
    unique_columns_expected: bool
    id_column_name: str
    ranking_item_id_column_name: str
    ranking_group_id_column_name: str
    tags_column_name: str
    timestamp_column_name: str
    tokens_column_name: str
    embeddings_column_name: str
    model_output_type: _model_output_type_pb2.ModelOutputType
    score_type: _qoi_pb2.QuantityOfInterest
    model_id: str
    options_hash: str
    write_time: _timestamp_pb2.Timestamp
    split_type: str
    def __init__(self, outputs: _Optional[_Iterable[_Union[OutputFileInfo, _Mapping]]] = ..., schema_mismatch_kafka_output: _Optional[_Union[OutputFileInfo, _Mapping]] = ..., schema_mismatch_iceberg_output: _Optional[_Union[OutputFileInfo, _Mapping]] = ..., output_file: _Optional[_Union[MaterializedOutputFile, _Mapping]] = ..., unique_columns_expected: bool = ..., id_column_name: _Optional[str] = ..., ranking_item_id_column_name: _Optional[str] = ..., ranking_group_id_column_name: _Optional[str] = ..., tags_column_name: _Optional[str] = ..., timestamp_column_name: _Optional[str] = ..., tokens_column_name: _Optional[str] = ..., embeddings_column_name: _Optional[str] = ..., model_output_type: _Optional[_Union[_model_output_type_pb2.ModelOutputType, str]] = ..., score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., model_id: _Optional[str] = ..., options_hash: _Optional[str] = ..., write_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., split_type: _Optional[str] = ...) -> None: ...

class OutputOperationMetadatas(_message.Message):
    __slots__ = ("operations",)
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    operations: _containers.RepeatedCompositeFieldContainer[OutputOperationMetadata]
    def __init__(self, operations: _Optional[_Iterable[_Union[OutputOperationMetadata, _Mapping]]] = ...) -> None: ...

class OutputFileInfo(_message.Message):
    __slots__ = ("output_write_location", "output_details", "id_column_name", "ranking_item_id_column_name", "ranking_group_id_column_name", "unique_columns_expected", "timestamp_column_name", "tags_column_name", "tokens_column_name", "embeddings_column_name", "data_locator", "model_id", "project_id", "data_collection_id")
    OUTPUT_WRITE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_DETAILS_FIELD_NUMBER: _ClassVar[int]
    ID_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    RANKING_ITEM_ID_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    RANKING_GROUP_ID_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_COLUMNS_EXPECTED_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    TOKENS_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    EMBEDDINGS_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    output_write_location: OutputWriteLocation
    output_details: MaterializedOutputFile
    id_column_name: str
    ranking_item_id_column_name: str
    ranking_group_id_column_name: str
    unique_columns_expected: bool
    timestamp_column_name: str
    tags_column_name: str
    tokens_column_name: str
    embeddings_column_name: str
    data_locator: _data_locator_pb2.DataLocator
    model_id: str
    project_id: str
    data_collection_id: str
    def __init__(self, output_write_location: _Optional[_Union[OutputWriteLocation, _Mapping]] = ..., output_details: _Optional[_Union[MaterializedOutputFile, _Mapping]] = ..., id_column_name: _Optional[str] = ..., ranking_item_id_column_name: _Optional[str] = ..., ranking_group_id_column_name: _Optional[str] = ..., unique_columns_expected: bool = ..., timestamp_column_name: _Optional[str] = ..., tags_column_name: _Optional[str] = ..., tokens_column_name: _Optional[str] = ..., embeddings_column_name: _Optional[str] = ..., data_locator: _Optional[_Union[_data_locator_pb2.DataLocator, _Mapping]] = ..., model_id: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ...) -> None: ...

class OutputWriteLocation(_message.Message):
    __slots__ = ("csv_file_path", "kafka_topic_name", "table_info")
    CSV_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    KAFKA_TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_INFO_FIELD_NUMBER: _ClassVar[int]
    csv_file_path: str
    kafka_topic_name: str
    table_info: _common_pb2.TableInfo
    def __init__(self, csv_file_path: _Optional[str] = ..., kafka_topic_name: _Optional[str] = ..., table_info: _Optional[_Union[_common_pb2.TableInfo, _Mapping]] = ...) -> None: ...

class MaterializeOperationMetadata(_message.Message):
    __slots__ = ("rows_written", "bytes_written")
    ROWS_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    BYTES_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    rows_written: int
    bytes_written: int
    def __init__(self, rows_written: _Optional[int] = ..., bytes_written: _Optional[int] = ...) -> None: ...

class MaterializeOutputResult(_message.Message):
    __slots__ = ("bytes_written", "output_schema", "data_kind", "output_write_location", "rows_written")
    BYTES_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    DATA_KIND_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_WRITE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    ROWS_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    bytes_written: int
    output_schema: _containers.RepeatedCompositeFieldContainer[_schema_pb2.ColumnDetails]
    data_kind: _data_kind_pb2.DataKindDescribed
    output_write_location: OutputWriteLocation
    rows_written: int
    def __init__(self, bytes_written: _Optional[int] = ..., output_schema: _Optional[_Iterable[_Union[_schema_pb2.ColumnDetails, _Mapping]]] = ..., data_kind: _Optional[_Union[_data_kind_pb2.DataKindDescribed, str]] = ..., output_write_location: _Optional[_Union[OutputWriteLocation, _Mapping]] = ..., rows_written: _Optional[int] = ...) -> None: ...

class MaterializeResult(_message.Message):
    __slots__ = ("metadata", "output_writes")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_WRITES_FIELD_NUMBER: _ClassVar[int]
    metadata: MaterializeOperationMetadata
    output_writes: _containers.RepeatedCompositeFieldContainer[MaterializeOutputResult]
    def __init__(self, metadata: _Optional[_Union[MaterializeOperationMetadata, _Mapping]] = ..., output_writes: _Optional[_Iterable[_Union[MaterializeOutputResult, _Mapping]]] = ...) -> None: ...

class RowSample(_message.Message):
    __slots__ = ("rows", "schema")
    ROWS_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[_row_pb2.Row]
    schema: _containers.RepeatedCompositeFieldContainer[_schema_pb2.ColumnDetails]
    def __init__(self, rows: _Optional[_Iterable[_Union[_row_pb2.Row, _Mapping]]] = ..., schema: _Optional[_Iterable[_Union[_schema_pb2.ColumnDetails, _Mapping]]] = ...) -> None: ...
