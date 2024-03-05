from google.protobuf import timestamp_pb2 as _timestamp_pb2
from truera.protobuf.public import background_data_split_info_pb2 as _background_data_split_info_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TableCatalog(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TABLE_CATALOG_UNSPECIFIED: _ClassVar[TableCatalog]
    TABLE_CATALOG_ICEBERG: _ClassVar[TableCatalog]

class TableFileFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TABLE_FILE_FORMAT_UNSPECIFIED: _ClassVar[TableFileFormat]
    TABLE_FILE_FORMAT_PARQUET: _ClassVar[TableFileFormat]

class TablePartitionTransform(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TABLE_PARTITION_TRANSFORM_UNSPECIFIED: _ClassVar[TablePartitionTransform]
    TABLE_PARTITION_TRANSFORM_IDENTITY: _ClassVar[TablePartitionTransform]
    TABLE_PARTITION_TRANSFORM_HOUR: _ClassVar[TablePartitionTransform]
    TABLE_PARTITION_TRANSFORM_DAY: _ClassVar[TablePartitionTransform]
    TABLE_PARTITION_TRANSFORM_MONTH: _ClassVar[TablePartitionTransform]
    TABLE_PARTITION_TRANSFORM_YEAR: _ClassVar[TablePartitionTransform]

class TablePartitionSystemColumn(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TABLE_PARTITION_SYSTEM_COLUMN_UNSPECIFIED: _ClassVar[TablePartitionSystemColumn]
    TABLE_PARTITION_SYSTEM_COLUMN_TIMESTAMP: _ClassVar[TablePartitionSystemColumn]
    TABLE_PARTITION_SYSTEM_COLUMN_SPLIT_ID: _ClassVar[TablePartitionSystemColumn]
    TABLE_PARTITION_SYSTEM_COLUMN_MODEL_ID: _ClassVar[TablePartitionSystemColumn]
    TABLE_PARTITION_SYSTEM_COLUMN_TENANT_ID: _ClassVar[TablePartitionSystemColumn]

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_ERROR: _ClassVar[ErrorCode]
    UNKNOWN_ERROR: _ClassVar[ErrorCode]

class ServiceNamespace(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_SERVICE: _ClassVar[ServiceNamespace]
TABLE_CATALOG_UNSPECIFIED: TableCatalog
TABLE_CATALOG_ICEBERG: TableCatalog
TABLE_FILE_FORMAT_UNSPECIFIED: TableFileFormat
TABLE_FILE_FORMAT_PARQUET: TableFileFormat
TABLE_PARTITION_TRANSFORM_UNSPECIFIED: TablePartitionTransform
TABLE_PARTITION_TRANSFORM_IDENTITY: TablePartitionTransform
TABLE_PARTITION_TRANSFORM_HOUR: TablePartitionTransform
TABLE_PARTITION_TRANSFORM_DAY: TablePartitionTransform
TABLE_PARTITION_TRANSFORM_MONTH: TablePartitionTransform
TABLE_PARTITION_TRANSFORM_YEAR: TablePartitionTransform
TABLE_PARTITION_SYSTEM_COLUMN_UNSPECIFIED: TablePartitionSystemColumn
TABLE_PARTITION_SYSTEM_COLUMN_TIMESTAMP: TablePartitionSystemColumn
TABLE_PARTITION_SYSTEM_COLUMN_SPLIT_ID: TablePartitionSystemColumn
TABLE_PARTITION_SYSTEM_COLUMN_MODEL_ID: TablePartitionSystemColumn
TABLE_PARTITION_SYSTEM_COLUMN_TENANT_ID: TablePartitionSystemColumn
NO_ERROR: ErrorCode
UNKNOWN_ERROR: ErrorCode
UNKNOWN_SERVICE: ServiceNamespace

class UserContent(_message.Message):
    __slots__ = ("id", "user_id", "created_at", "text", "uri", "uuencoded", "context", "title", "thread_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    UUENCODED_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: UserId
    created_at: _timestamp_pb2.Timestamp
    text: str
    uri: str
    uuencoded: str
    context: str
    title: str
    thread_id: str
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[_Union[UserId, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., text: _Optional[str] = ..., uri: _Optional[str] = ..., uuencoded: _Optional[str] = ..., context: _Optional[str] = ..., title: _Optional[str] = ..., thread_id: _Optional[str] = ...) -> None: ...

class UserId(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class TablePartitionConfig(_message.Message):
    __slots__ = ("transform", "column")
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    transform: TablePartitionTransform
    column: TablePartitionSystemColumn
    def __init__(self, transform: _Optional[_Union[TablePartitionTransform, str]] = ..., column: _Optional[_Union[TablePartitionSystemColumn, str]] = ...) -> None: ...

class TableInfo(_message.Message):
    __slots__ = ("catalog", "schema", "name", "uri", "format", "partition_configs")
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    PARTITION_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    catalog: TableCatalog
    schema: str
    name: str
    uri: str
    format: TableFileFormat
    partition_configs: _containers.RepeatedCompositeFieldContainer[TablePartitionConfig]
    def __init__(self, catalog: _Optional[_Union[TableCatalog, str]] = ..., schema: _Optional[str] = ..., name: _Optional[str] = ..., uri: _Optional[str] = ..., format: _Optional[_Union[TableFileFormat, str]] = ..., partition_configs: _Optional[_Iterable[_Union[TablePartitionConfig, _Mapping]]] = ...) -> None: ...

class TableLocationInfo(_message.Message):
    __slots__ = ("catalog", "schema", "name")
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    catalog: TableCatalog
    schema: str
    name: str
    def __init__(self, catalog: _Optional[_Union[TableCatalog, str]] = ..., schema: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class LocalFile(_message.Message):
    __slots__ = ("file_path",)
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    file_path: str
    def __init__(self, file_path: _Optional[str] = ...) -> None: ...

class KafkaTopic(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DruidTable(_message.Message):
    __slots__ = ("datasource_name", "kafka_topic_name")
    DATASOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    KAFKA_TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    datasource_name: str
    kafka_topic_name: str
    def __init__(self, datasource_name: _Optional[str] = ..., kafka_topic_name: _Optional[str] = ...) -> None: ...

class FeatureInfluenceOptions(_message.Message):
    __slots__ = ("quantity_of_interest", "background_data_split_info", "explanation_algorithm_type")
    QUANTITY_OF_INTEREST_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_DATA_SPLIT_INFO_FIELD_NUMBER: _ClassVar[int]
    EXPLANATION_ALGORITHM_TYPE_FIELD_NUMBER: _ClassVar[int]
    quantity_of_interest: _qoi_pb2.QuantityOfInterest
    background_data_split_info: _background_data_split_info_pb2.BackgroundDataSplitInfo
    explanation_algorithm_type: _qoi_pb2.ExplanationAlgorithmType
    def __init__(self, quantity_of_interest: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., background_data_split_info: _Optional[_Union[_background_data_split_info_pb2.BackgroundDataSplitInfo, _Mapping]] = ..., explanation_algorithm_type: _Optional[_Union[_qoi_pb2.ExplanationAlgorithmType, str]] = ...) -> None: ...

class PredictionOptions(_message.Message):
    __slots__ = ("score_type",)
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    score_type: _qoi_pb2.QuantityOfInterest
    def __init__(self, score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ("error_code", "error_msg")
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    error_code: ErrorCode
    error_msg: str
    def __init__(self, error_code: _Optional[_Union[ErrorCode, str]] = ..., error_msg: _Optional[str] = ...) -> None: ...
