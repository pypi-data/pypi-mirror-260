from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from truera.protobuf.configuration import project_pb2 as _project_pb2
from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from truera.protobuf.public.aiq import intelligence_common_pb2 as _intelligence_common_pb2
from truera.protobuf.public.aiq import rnn_config_pb2 as _rnn_config_pb2
from truera.protobuf.public.common import data_kind_pb2 as _data_kind_pb2
from truera.protobuf.public import background_data_split_info_pb2 as _background_data_split_info_pb2
from truera.protobuf.public.data_service import data_service_messages_pb2 as _data_service_messages_pb2
from truera.protobuf.public.util import split_mode_pb2 as _split_mode_pb2
from truera.protobuf.public.util import time_range_pb2 as _time_range_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from truera.protobuf.public import model_output_type_pb2 as _model_output_type_pb2
from truera.protobuf.public.common import ingestion_schema_pb2 as _ingestion_schema_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InputDataFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_INPUT_FORMAT: _ClassVar[InputDataFormat]
    TABULAR: _ClassVar[InputDataFormat]
    TIME_SERIES_TABULAR: _ClassVar[InputDataFormat]
    IMAGE: _ClassVar[InputDataFormat]
    TEXT: _ClassVar[InputDataFormat]

class ProjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_PROJECT_TYPE: _ClassVar[ProjectType]
    MODEL_PROJECT: _ClassVar[ProjectType]
    APPLICATION_PROJECT: _ClassVar[ProjectType]

class ModelProvenance(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER_GENERATED: _ClassVar[ModelProvenance]
    SYSTEM_GENERATED: _ClassVar[ModelProvenance]

class FeatureTransformationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FEATURE_TRANSFORM_TYPE_UNKNOWN: _ClassVar[FeatureTransformationType]
    FEATURE_TRANSFORM_TYPE_NO_TRANSFORM: _ClassVar[FeatureTransformationType]
    FEATURE_TRANSFORM_TYPE_PRE_POST_DATA: _ClassVar[FeatureTransformationType]
    FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION: _ClassVar[FeatureTransformationType]

class SplitCreationSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CREATED_FROM_UNKNOWN: _ClassVar[SplitCreationSource]
    CREATED_FROM_CLI: _ClassVar[SplitCreationSource]
    CREATED_FROM_DATA_LAYER: _ClassVar[SplitCreationSource]
    CREATED_FROM_RCA: _ClassVar[SplitCreationSource]

class SplitStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPLIT_STATUS_INVALID: _ClassVar[SplitStatus]
    SPLIT_STATUS_ACTIVE: _ClassVar[SplitStatus]
    SPLIT_STATUS_INITIALIZING: _ClassVar[SplitStatus]

class CacheType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID_CACHE_TYPE: _ClassVar[CacheType]
    EXPLANATION_CACHE: _ClassVar[CacheType]
    MODEL_PREDICTION_CACHE: _ClassVar[CacheType]
    PARTIAL_DEPENDENCE_PLOT_CACHE: _ClassVar[CacheType]

class ModelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SKLEARN: _ClassVar[ModelType]
    H2O: _ClassVar[ModelType]
    DATAROBOT_V1: _ClassVar[ModelType]
    DATAROBOT_V2: _ClassVar[ModelType]
    PMML: _ClassVar[ModelType]
    PYFUNC: _ClassVar[ModelType]
    VIRTUAL: _ClassVar[ModelType]
    MLEAP: _ClassVar[ModelType]
UNKNOWN_INPUT_FORMAT: InputDataFormat
TABULAR: InputDataFormat
TIME_SERIES_TABULAR: InputDataFormat
IMAGE: InputDataFormat
TEXT: InputDataFormat
UNKNOWN_PROJECT_TYPE: ProjectType
MODEL_PROJECT: ProjectType
APPLICATION_PROJECT: ProjectType
USER_GENERATED: ModelProvenance
SYSTEM_GENERATED: ModelProvenance
FEATURE_TRANSFORM_TYPE_UNKNOWN: FeatureTransformationType
FEATURE_TRANSFORM_TYPE_NO_TRANSFORM: FeatureTransformationType
FEATURE_TRANSFORM_TYPE_PRE_POST_DATA: FeatureTransformationType
FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION: FeatureTransformationType
CREATED_FROM_UNKNOWN: SplitCreationSource
CREATED_FROM_CLI: SplitCreationSource
CREATED_FROM_DATA_LAYER: SplitCreationSource
CREATED_FROM_RCA: SplitCreationSource
SPLIT_STATUS_INVALID: SplitStatus
SPLIT_STATUS_ACTIVE: SplitStatus
SPLIT_STATUS_INITIALIZING: SplitStatus
INVALID_CACHE_TYPE: CacheType
EXPLANATION_CACHE: CacheType
MODEL_PREDICTION_CACHE: CacheType
PARTIAL_DEPENDENCE_PLOT_CACHE: CacheType
SKLEARN: ModelType
H2O: ModelType
DATAROBOT_V1: ModelType
DATAROBOT_V2: ModelType
PMML: ModelType
PYFUNC: ModelType
VIRTUAL: ModelType
MLEAP: ModelType

class ProjectLevelSettings(_message.Message):
    __slots__ = ("score_type", "input_data_format", "output_type")
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    INPUT_DATA_FORMAT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    score_type: _qoi_pb2.QuantityOfInterest
    input_data_format: InputDataFormat
    output_type: _model_output_type_pb2.ModelOutputType
    def __init__(self, score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., input_data_format: _Optional[_Union[InputDataFormat, str]] = ..., output_type: _Optional[_Union[_model_output_type_pb2.ModelOutputType, str]] = ...) -> None: ...

class ProjectMetadata(_message.Message):
    __slots__ = ("id", "name", "created_at", "documentation", "settings", "project_type")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTATION_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PROJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    created_at: _timestamp_pb2.Timestamp
    documentation: _project_pb2.ProjectDocumentation
    settings: ProjectLevelSettings
    project_type: ProjectType
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., documentation: _Optional[_Union[_project_pb2.ProjectDocumentation, _Mapping]] = ..., settings: _Optional[_Union[ProjectLevelSettings, _Mapping]] = ..., project_type: _Optional[_Union[ProjectType, str]] = ...) -> None: ...

class ApplicationMetadata(_message.Message):
    __slots__ = ("id", "name", "project_id", "description", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    project_id: str
    description: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., project_id: _Optional[str] = ..., description: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DatasetMetadata(_message.Message):
    __slots__ = ("id", "name", "project_id", "type", "created_at", "last_updated")
    class DatasetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[DatasetMetadata.DatasetType]
        EVALUATION: _ClassVar[DatasetMetadata.DatasetType]
        TESTING: _ClassVar[DatasetMetadata.DatasetType]
        PRODUCTION: _ClassVar[DatasetMetadata.DatasetType]
        TIME_RANGE: _ClassVar[DatasetMetadata.DatasetType]
    UNKNOWN: DatasetMetadata.DatasetType
    EVALUATION: DatasetMetadata.DatasetType
    TESTING: DatasetMetadata.DatasetType
    PRODUCTION: DatasetMetadata.DatasetType
    TIME_RANGE: DatasetMetadata.DatasetType
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    project_id: str
    type: DatasetMetadata.DatasetType
    created_at: _timestamp_pb2.Timestamp
    last_updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., project_id: _Optional[str] = ..., type: _Optional[_Union[DatasetMetadata.DatasetType, str]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FeedbackFunctionMetadata(_message.Message):
    __slots__ = ("id", "name", "project_id", "threshold", "config", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    project_id: str
    threshold: float
    config: _struct_pb2.Struct
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., project_id: _Optional[str] = ..., threshold: _Optional[float] = ..., config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ModelMetadata(_message.Message):
    __slots__ = ("id", "name", "description", "project_id", "data_collection_id", "model_type", "model_output_type", "locator", "tags", "created_at", "rnn_attribution_config", "nlp_attribution_config", "rnn_ui_config", "training_metadata", "model_provenance")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOCATOR_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    RNN_ATTRIBUTION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    NLP_ATTRIBUTION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    RNN_UI_CONFIG_FIELD_NUMBER: _ClassVar[int]
    TRAINING_METADATA_FIELD_NUMBER: _ClassVar[int]
    MODEL_PROVENANCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    project_id: str
    data_collection_id: str
    model_type: str
    model_output_type: _model_output_type_pb2.ModelOutputType
    locator: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    created_at: _timestamp_pb2.Timestamp
    rnn_attribution_config: _rnn_config_pb2.RNNAttributionConfig
    nlp_attribution_config: _rnn_config_pb2.NLPAttributionConfig
    rnn_ui_config: _rnn_config_pb2.RNNUIConfig
    training_metadata: ModelTrainingMetadata
    model_provenance: ModelProvenance
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., model_type: _Optional[str] = ..., model_output_type: _Optional[_Union[_model_output_type_pb2.ModelOutputType, str]] = ..., locator: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., rnn_attribution_config: _Optional[_Union[_rnn_config_pb2.RNNAttributionConfig, _Mapping]] = ..., nlp_attribution_config: _Optional[_Union[_rnn_config_pb2.NLPAttributionConfig, _Mapping]] = ..., rnn_ui_config: _Optional[_Union[_rnn_config_pb2.RNNUIConfig, _Mapping]] = ..., training_metadata: _Optional[_Union[ModelTrainingMetadata, _Mapping]] = ..., model_provenance: _Optional[_Union[ModelProvenance, str]] = ...) -> None: ...

class DataCollectionMetadata(_message.Message):
    __slots__ = ("id", "name", "project_id", "base_split_id", "feature_transform_type", "tags", "description", "ground_truth_labels", "schemas", "created_at", "ingestion_schema", "prod_split_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_TRANSFORM_TYPE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    GROUND_TRUTH_LABELS_FIELD_NUMBER: _ClassVar[int]
    SCHEMAS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    INGESTION_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    PROD_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    project_id: str
    base_split_id: str
    feature_transform_type: FeatureTransformationType
    tags: _containers.RepeatedScalarFieldContainer[str]
    description: str
    ground_truth_labels: _containers.RepeatedCompositeFieldContainer[GroundTruthLabel]
    schemas: _containers.RepeatedCompositeFieldContainer[SchemaMetadata]
    created_at: _timestamp_pb2.Timestamp
    ingestion_schema: _ingestion_schema_pb2.Schema
    prod_split_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., project_id: _Optional[str] = ..., base_split_id: _Optional[str] = ..., feature_transform_type: _Optional[_Union[FeatureTransformationType, str]] = ..., tags: _Optional[_Iterable[str]] = ..., description: _Optional[str] = ..., ground_truth_labels: _Optional[_Iterable[_Union[GroundTruthLabel, _Mapping]]] = ..., schemas: _Optional[_Iterable[_Union[SchemaMetadata, _Mapping]]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., ingestion_schema: _Optional[_Union[_ingestion_schema_pb2.Schema, _Mapping]] = ..., prod_split_id: _Optional[str] = ...) -> None: ...

class GroundTruthLabel(_message.Message):
    __slots__ = ("value", "value_name")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    VALUE_NAME_FIELD_NUMBER: _ClassVar[int]
    value: _struct_pb2.Value
    value_name: str
    def __init__(self, value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., value_name: _Optional[str] = ...) -> None: ...

class SchemaMetadata(_message.Message):
    __slots__ = ("schema_id_for_parsing", "schema_id_for_output_data", "describes_file")
    SCHEMA_ID_FOR_PARSING_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_ID_FOR_OUTPUT_DATA_FIELD_NUMBER: _ClassVar[int]
    DESCRIBES_FILE_FIELD_NUMBER: _ClassVar[int]
    schema_id_for_parsing: str
    schema_id_for_output_data: str
    describes_file: _data_kind_pb2.DataKindDescribed
    def __init__(self, schema_id_for_parsing: _Optional[str] = ..., schema_id_for_output_data: _Optional[str] = ..., describes_file: _Optional[_Union[_data_kind_pb2.DataKindDescribed, str]] = ...) -> None: ...

class DataProvenance(_message.Message):
    __slots__ = ("split_creation_source", "root_rowset_id", "schema_info_items", "rowset_id", "materialized_by_operation", "sample_strategy", "seed")
    SPLIT_CREATION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ROOT_ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_INFO_ITEMS_FIELD_NUMBER: _ClassVar[int]
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZED_BY_OPERATION_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    split_creation_source: SplitCreationSource
    root_rowset_id: _containers.RepeatedScalarFieldContainer[str]
    schema_info_items: _containers.RepeatedCompositeFieldContainer[RowsetWithSchema]
    rowset_id: str
    materialized_by_operation: str
    sample_strategy: _data_service_messages_pb2.SampleStrategy
    seed: int
    def __init__(self, split_creation_source: _Optional[_Union[SplitCreationSource, str]] = ..., root_rowset_id: _Optional[_Iterable[str]] = ..., schema_info_items: _Optional[_Iterable[_Union[RowsetWithSchema, _Mapping]]] = ..., rowset_id: _Optional[str] = ..., materialized_by_operation: _Optional[str] = ..., sample_strategy: _Optional[_Union[_data_service_messages_pb2.SampleStrategy, str]] = ..., seed: _Optional[int] = ...) -> None: ...

class RowsetWithSchema(_message.Message):
    __slots__ = ("root_rowset_id", "schemaMetadata")
    ROOT_ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEMAMETADATA_FIELD_NUMBER: _ClassVar[int]
    root_rowset_id: str
    schemaMetadata: SchemaMetadata
    def __init__(self, root_rowset_id: _Optional[str] = ..., schemaMetadata: _Optional[_Union[SchemaMetadata, _Mapping]] = ...) -> None: ...

class DataSplitMetadata(_message.Message):
    __slots__ = ("id", "name", "description", "project_id", "data_collection_id", "split_type", "preprocessed_locator", "processed_locator", "label_locator", "extra_data_locator", "tags", "provenance", "created_at", "time_range", "unique_id_column_name", "timestamp_column_name", "created_on", "updated_on", "split_mode", "status", "train_baseline_model", "time_window_filter", "prediction_score_types", "options_hashes", "rows_written")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PREPROCESSED_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    LABEL_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    EXTRA_DATA_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    PROVENANCE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    UPDATED_ON_FIELD_NUMBER: _ClassVar[int]
    SPLIT_MODE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRAIN_BASELINE_MODEL_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FILTER_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_SCORE_TYPES_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_HASHES_FIELD_NUMBER: _ClassVar[int]
    ROWS_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    project_id: str
    data_collection_id: str
    split_type: str
    preprocessed_locator: str
    processed_locator: str
    label_locator: str
    extra_data_locator: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    provenance: DataProvenance
    created_at: _timestamp_pb2.Timestamp
    time_range: _time_range_pb2.TimeRange
    unique_id_column_name: str
    timestamp_column_name: str
    created_on: str
    updated_on: str
    split_mode: _split_mode_pb2.SplitMode
    status: SplitStatus
    train_baseline_model: bool
    time_window_filter: TimeWindowFilter
    prediction_score_types: _containers.RepeatedScalarFieldContainer[_qoi_pb2.QuantityOfInterest]
    options_hashes: _containers.RepeatedScalarFieldContainer[str]
    rows_written: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., split_type: _Optional[str] = ..., preprocessed_locator: _Optional[str] = ..., processed_locator: _Optional[str] = ..., label_locator: _Optional[str] = ..., extra_data_locator: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., provenance: _Optional[_Union[DataProvenance, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., time_range: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ..., unique_id_column_name: _Optional[str] = ..., timestamp_column_name: _Optional[str] = ..., created_on: _Optional[str] = ..., updated_on: _Optional[str] = ..., split_mode: _Optional[_Union[_split_mode_pb2.SplitMode, str]] = ..., status: _Optional[_Union[SplitStatus, str]] = ..., train_baseline_model: bool = ..., time_window_filter: _Optional[_Union[TimeWindowFilter, _Mapping]] = ..., prediction_score_types: _Optional[_Iterable[_Union[_qoi_pb2.QuantityOfInterest, str]]] = ..., options_hashes: _Optional[_Iterable[str]] = ..., rows_written: _Optional[int] = ...) -> None: ...

class DataSourceWrapper(_message.Message):
    __slots__ = ("data_source", "credentials", "credential_id")
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    data_source: DataSource
    credentials: _data_service_messages_pb2.Credentials
    credential_id: str
    def __init__(self, data_source: _Optional[_Union[DataSource, _Mapping]] = ..., credentials: _Optional[_Union[_data_service_messages_pb2.Credentials, _Mapping]] = ..., credential_id: _Optional[str] = ...) -> None: ...

class DataSource(_message.Message):
    __slots__ = ("id", "name", "project_id", "uri", "format", "db_info", "rowset_id", "type", "creation_reason", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    DB_INFO_FIELD_NUMBER: _ClassVar[int]
    ROWSET_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATION_REASON_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    project_id: str
    uri: str
    format: _data_service_messages_pb2.Format
    db_info: _data_service_messages_pb2.DatabaseInfo
    rowset_id: str
    type: _data_service_messages_pb2.DataSourceType
    creation_reason: _data_service_messages_pb2.CreationReason
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., project_id: _Optional[str] = ..., uri: _Optional[str] = ..., format: _Optional[_Union[_data_service_messages_pb2.Format, _Mapping]] = ..., db_info: _Optional[_Union[_data_service_messages_pb2.DatabaseInfo, _Mapping]] = ..., rowset_id: _Optional[str] = ..., type: _Optional[_Union[_data_service_messages_pb2.DataSourceType, str]] = ..., creation_reason: _Optional[_Union[_data_service_messages_pb2.CreationReason, str]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ModelInputSpecTruncated(_message.Message):
    __slots__ = ("row_count", "split_id")
    ROW_COUNT_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    row_count: int
    split_id: str
    def __init__(self, row_count: _Optional[int] = ..., split_id: _Optional[str] = ...) -> None: ...

class ClientGeneratedByInfo(_message.Message):
    __slots__ = ("client_name", "client_version")
    CLIENT_NAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    client_name: str
    client_version: str
    def __init__(self, client_name: _Optional[str] = ..., client_version: _Optional[str] = ...) -> None: ...

class CacheMetadata(_message.Message):
    __slots__ = ("id", "project_id", "model_id", "model_input_spec_truncated", "background_data_split_info", "score_type", "cache_type", "explanation_algorithm_type", "location", "format", "generated_by", "processing")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_INPUT_SPEC_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_DATA_SPLIT_INFO_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CACHE_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXPLANATION_ALGORITHM_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    GENERATED_BY_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    model_id: str
    model_input_spec_truncated: ModelInputSpecTruncated
    background_data_split_info: _background_data_split_info_pb2.BackgroundDataSplitInfo
    score_type: _qoi_pb2.QuantityOfInterest
    cache_type: CacheType
    explanation_algorithm_type: _qoi_pb2.ExplanationAlgorithmType
    location: str
    format: str
    generated_by: ClientGeneratedByInfo
    processing: _intelligence_common_pb2.ProcessingMetadata
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ..., model_id: _Optional[str] = ..., model_input_spec_truncated: _Optional[_Union[ModelInputSpecTruncated, _Mapping]] = ..., background_data_split_info: _Optional[_Union[_background_data_split_info_pb2.BackgroundDataSplitInfo, _Mapping]] = ..., score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., cache_type: _Optional[_Union[CacheType, str]] = ..., explanation_algorithm_type: _Optional[_Union[_qoi_pb2.ExplanationAlgorithmType, str]] = ..., location: _Optional[str] = ..., format: _Optional[str] = ..., generated_by: _Optional[_Union[ClientGeneratedByInfo, _Mapping]] = ..., processing: _Optional[_Union[_intelligence_common_pb2.ProcessingMetadata, _Mapping]] = ...) -> None: ...

class ModelTrainingMetadata(_message.Message):
    __slots__ = ("train_split_id", "parameters")
    TRAIN_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    train_split_id: str
    parameters: _struct_pb2.Struct
    def __init__(self, train_split_id: _Optional[str] = ..., parameters: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class TimeWindowFilter(_message.Message):
    __slots__ = ("parent_split_id", "split_start_time", "split_end_time")
    PARENT_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_START_TIME_FIELD_NUMBER: _ClassVar[int]
    SPLIT_END_TIME_FIELD_NUMBER: _ClassVar[int]
    parent_split_id: str
    split_start_time: _timestamp_pb2.Timestamp
    split_end_time: _timestamp_pb2.Timestamp
    def __init__(self, parent_split_id: _Optional[str] = ..., split_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., split_end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
