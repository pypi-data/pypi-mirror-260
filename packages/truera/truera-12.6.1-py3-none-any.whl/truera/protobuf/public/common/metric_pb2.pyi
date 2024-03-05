from google.protobuf import timestamp_pb2 as _timestamp_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MetricAggregationLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_AGG_LEVEL_INVALID: _ClassVar[MetricAggregationLevel]
    FIFTEEN_MINUTE: _ClassVar[MetricAggregationLevel]
    THIRTY_MINUTE: _ClassVar[MetricAggregationLevel]
    HOUR: _ClassVar[MetricAggregationLevel]
    DAY: _ClassVar[MetricAggregationLevel]
    WEEK: _ClassVar[MetricAggregationLevel]
    MONTH: _ClassVar[MetricAggregationLevel]

class MetricAggregationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_AGG_TYPE_INVALID: _ClassVar[MetricAggregationType]
    METRIC_COUNT: _ClassVar[MetricAggregationType]
    METRIC_MIN: _ClassVar[MetricAggregationType]
    METRIC_MAX: _ClassVar[MetricAggregationType]
    METRIC_SUM: _ClassVar[MetricAggregationType]
    METRIC_AVG: _ClassVar[MetricAggregationType]

class MetricType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_TYPE_INVALID: _ClassVar[MetricType]
    GENERAL: _ClassVar[MetricType]
    MODEL: _ClassVar[MetricType]
    POINT: _ClassVar[MetricType]
METRIC_AGG_LEVEL_INVALID: MetricAggregationLevel
FIFTEEN_MINUTE: MetricAggregationLevel
THIRTY_MINUTE: MetricAggregationLevel
HOUR: MetricAggregationLevel
DAY: MetricAggregationLevel
WEEK: MetricAggregationLevel
MONTH: MetricAggregationLevel
METRIC_AGG_TYPE_INVALID: MetricAggregationType
METRIC_COUNT: MetricAggregationType
METRIC_MIN: MetricAggregationType
METRIC_MAX: MetricAggregationType
METRIC_SUM: MetricAggregationType
METRIC_AVG: MetricAggregationType
METRIC_TYPE_INVALID: MetricType
GENERAL: MetricType
MODEL: MetricType
POINT: MetricType

class Metric(_message.Message):
    __slots__ = ("project_id", "custom_metric_name", "custom_metric_value", "metric_type", "model_id", "point_id", "timestamp")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_METRIC_VALUE_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    custom_metric_name: str
    custom_metric_value: float
    metric_type: str
    model_id: str
    point_id: str
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, project_id: _Optional[str] = ..., custom_metric_name: _Optional[str] = ..., custom_metric_value: _Optional[float] = ..., metric_type: _Optional[str] = ..., model_id: _Optional[str] = ..., point_id: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MetricDefinition(_message.Message):
    __slots__ = ("id", "name", "project_id", "aggregation_type", "aggregation_level", "metric_type")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_LEVEL_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    project_id: str
    aggregation_type: MetricAggregationType
    aggregation_level: MetricAggregationLevel
    metric_type: MetricType
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., project_id: _Optional[str] = ..., aggregation_type: _Optional[_Union[MetricAggregationType, str]] = ..., aggregation_level: _Optional[_Union[MetricAggregationLevel, str]] = ..., metric_type: _Optional[_Union[MetricType, str]] = ...) -> None: ...
