from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from truera.protobuf.public import model_output_type_pb2 as _model_output_type_pb2
from truera.protobuf.public import metadata_message_types_pb2 as _metadata_message_types_pb2
from truera.protobuf.public.aiq import accuracy_pb2 as _accuracy_pb2
from truera.protobuf.public.aiq import distance_pb2 as _distance_pb2
from truera.protobuf.queryservice import query_service_pb2 as _query_service_pb2
from truera.protobuf.public.aiq import intelligence_service_pb2 as _intelligence_service_pb2
from truera.protobuf.public.common import metric_pb2 as _metric_pb2
from truera.protobuf.public import analysis_type_pb2 as _analysis_type_pb2
from truera.protobuf.public.data import data_split_pb2 as _data_split_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PanelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_PANEL_TYPE: _ClassVar[PanelType]
    MODEL_OUTPUT_DISTRIBUTION_PANEL: _ClassVar[PanelType]
    MODEL_OUTPUT_DRIFT_PANEL: _ClassVar[PanelType]
    MODEL_OUTPUT_VOLUME_PANEL: _ClassVar[PanelType]
    MODEL_OUTPUT_MEAN_PANEL: _ClassVar[PanelType]
    LABEL_VOLUME_PANEL: _ClassVar[PanelType]
    LABEL_DISTRIBUTION_PANEL: _ClassVar[PanelType]
    MODEL_PERFORMANCE_PANEL: _ClassVar[PanelType]
    INPUT_VOLUME_PANEL: _ClassVar[PanelType]
    DATA_DRIFT_PANEL: _ClassVar[PanelType]
    DATA_QUALITY_UNRECOGNIZED_CATEGORICAL_PANEL: _ClassVar[PanelType]
    DATA_QUALITY_NUMERICAL_ISSUES_PANEL: _ClassVar[PanelType]
    DATA_QUALITY_SCHEMA_MISMATCH_PANEL: _ClassVar[PanelType]
    DATA_QUALITY_MISSING_VALUES_PANEL: _ClassVar[PanelType]
    DATA_QUALITY_OUT_OF_RANGE_VALUES_PANEL: _ClassVar[PanelType]
    DATA_QUALITY_EXPLORATION_PANEL: _ClassVar[PanelType]
    CLASSIFICATION_LABEL_DISTRIBUTION_PANEL: _ClassVar[PanelType]
    MODEL_OUTPUT_CLASS_DISTRIBUTION_PANEL: _ClassVar[PanelType]
    AVERAGED_SCORE_PANEL: _ClassVar[PanelType]
    MODEL_DECISIONS_AND_LABELS_PANEL: _ClassVar[PanelType]
    LABEL_DRIFT_PANEL: _ClassVar[PanelType]
    CUSTOM_METRIC_PANEL: _ClassVar[PanelType]
    MODEL_SCORE_DISTRIBUTION_PANEL: _ClassVar[PanelType]
    GENERATIVE_METRIC_PANEL: _ClassVar[PanelType]

class MetricType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_METRIC_TYPE: _ClassVar[MetricType]
    MODEL_OUTPUT_STANDARD_DEVIATION_RANGE: _ClassVar[MetricType]
    DATA_QUALITY_UNRECOGNIZED_CATEGORICAL: _ClassVar[MetricType]
    DATA_QUALITY_NUMERICAL_ISSUES: _ClassVar[MetricType]
    DATA_QUALITY_SCHEMA_MISMATCH: _ClassVar[MetricType]
    DATA_QUALITY_MISSING_VALUES: _ClassVar[MetricType]
    DATA_DRIFT: _ClassVar[MetricType]
    MODEL_OUTPUT_DISTRIBUTION: _ClassVar[MetricType]
    MODEL_OUTPUT_DRIFT: _ClassVar[MetricType]
    MODEL_OUTPUT_VOLUME: _ClassVar[MetricType]
    MODEL_PERFORMANCE: _ClassVar[MetricType]
    LABEL_VOLUME: _ClassVar[MetricType]
    LABEL_DISTRIBUTION: _ClassVar[MetricType]
    MODEL_OUTPUT_MEAN: _ClassVar[MetricType]
    DATA_QUALITY_OUT_OF_RANGE: _ClassVar[MetricType]
    FEATURE_INFLUENCE_DRIFT: _ClassVar[MetricType]
    FEATURE_INFLUENCE_MEAN: _ClassVar[MetricType]
    FEATURE_BASED_DATA_QUALITY_NUMERICAL_ISSUES: _ClassVar[MetricType]
    FEATURE_BASED_DATA_QUALITY_OUT_OF_RANGE: _ClassVar[MetricType]
    INPUT_FEATURE_STATISTICS: _ClassVar[MetricType]
    CLASSIFICATION_LABEL_DISTRIBUTION: _ClassVar[MetricType]
    FEATURE_BASED_DATA_QUALITY_CATEGORICAL_MISSING_VALUES: _ClassVar[MetricType]
    FEATURE_BASED_DATA_QUALITY_UNRECOGNIZED_CATEGORICAL: _ClassVar[MetricType]
    MODEL_OUTPUT_CLASS_DISTRIBUTION: _ClassVar[MetricType]
    LABEL_DRIFT: _ClassVar[MetricType]
    LABEL_MEAN: _ClassVar[MetricType]
    MODEL_SCORE_DISTRIBUTION: _ClassVar[MetricType]
    CUSTOM_METRIC: _ClassVar[MetricType]
    GENERATIVE_METRIC: _ClassVar[MetricType]

class CustomMetricType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_CUSTOM_METRIC_TYPE: _ClassVar[CustomMetricType]
    GENERAL_CUSTOM_METRIC: _ClassVar[CustomMetricType]
    MODEL_CUSTOM_METRIC: _ClassVar[CustomMetricType]
    RECORD_CUSTOM_METRIC: _ClassVar[CustomMetricType]

class LLMMetricType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_LLM_METRIC_TYPE: _ClassVar[LLMMetricType]
    FEEDBACK_FUNCTION_METRIC: _ClassVar[LLMMetricType]
    TRACE_METRIC: _ClassVar[LLMMetricType]
UNKNOWN_PANEL_TYPE: PanelType
MODEL_OUTPUT_DISTRIBUTION_PANEL: PanelType
MODEL_OUTPUT_DRIFT_PANEL: PanelType
MODEL_OUTPUT_VOLUME_PANEL: PanelType
MODEL_OUTPUT_MEAN_PANEL: PanelType
LABEL_VOLUME_PANEL: PanelType
LABEL_DISTRIBUTION_PANEL: PanelType
MODEL_PERFORMANCE_PANEL: PanelType
INPUT_VOLUME_PANEL: PanelType
DATA_DRIFT_PANEL: PanelType
DATA_QUALITY_UNRECOGNIZED_CATEGORICAL_PANEL: PanelType
DATA_QUALITY_NUMERICAL_ISSUES_PANEL: PanelType
DATA_QUALITY_SCHEMA_MISMATCH_PANEL: PanelType
DATA_QUALITY_MISSING_VALUES_PANEL: PanelType
DATA_QUALITY_OUT_OF_RANGE_VALUES_PANEL: PanelType
DATA_QUALITY_EXPLORATION_PANEL: PanelType
CLASSIFICATION_LABEL_DISTRIBUTION_PANEL: PanelType
MODEL_OUTPUT_CLASS_DISTRIBUTION_PANEL: PanelType
AVERAGED_SCORE_PANEL: PanelType
MODEL_DECISIONS_AND_LABELS_PANEL: PanelType
LABEL_DRIFT_PANEL: PanelType
CUSTOM_METRIC_PANEL: PanelType
MODEL_SCORE_DISTRIBUTION_PANEL: PanelType
GENERATIVE_METRIC_PANEL: PanelType
UNKNOWN_METRIC_TYPE: MetricType
MODEL_OUTPUT_STANDARD_DEVIATION_RANGE: MetricType
DATA_QUALITY_UNRECOGNIZED_CATEGORICAL: MetricType
DATA_QUALITY_NUMERICAL_ISSUES: MetricType
DATA_QUALITY_SCHEMA_MISMATCH: MetricType
DATA_QUALITY_MISSING_VALUES: MetricType
DATA_DRIFT: MetricType
MODEL_OUTPUT_DISTRIBUTION: MetricType
MODEL_OUTPUT_DRIFT: MetricType
MODEL_OUTPUT_VOLUME: MetricType
MODEL_PERFORMANCE: MetricType
LABEL_VOLUME: MetricType
LABEL_DISTRIBUTION: MetricType
MODEL_OUTPUT_MEAN: MetricType
DATA_QUALITY_OUT_OF_RANGE: MetricType
FEATURE_INFLUENCE_DRIFT: MetricType
FEATURE_INFLUENCE_MEAN: MetricType
FEATURE_BASED_DATA_QUALITY_NUMERICAL_ISSUES: MetricType
FEATURE_BASED_DATA_QUALITY_OUT_OF_RANGE: MetricType
INPUT_FEATURE_STATISTICS: MetricType
CLASSIFICATION_LABEL_DISTRIBUTION: MetricType
FEATURE_BASED_DATA_QUALITY_CATEGORICAL_MISSING_VALUES: MetricType
FEATURE_BASED_DATA_QUALITY_UNRECOGNIZED_CATEGORICAL: MetricType
MODEL_OUTPUT_CLASS_DISTRIBUTION: MetricType
LABEL_DRIFT: MetricType
LABEL_MEAN: MetricType
MODEL_SCORE_DISTRIBUTION: MetricType
CUSTOM_METRIC: MetricType
GENERATIVE_METRIC: MetricType
UNKNOWN_CUSTOM_METRIC_TYPE: CustomMetricType
GENERAL_CUSTOM_METRIC: CustomMetricType
MODEL_CUSTOM_METRIC: CustomMetricType
RECORD_CUSTOM_METRIC: CustomMetricType
UNKNOWN_LLM_METRIC_TYPE: LLMMetricType
FEEDBACK_FUNCTION_METRIC: LLMMetricType
TRACE_METRIC: LLMMetricType

class CreateDashboardRequest(_message.Message):
    __slots__ = ("dashboard_detail", "workspace_id")
    DASHBOARD_DETAIL_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_detail: DashboardDetail
    workspace_id: str
    def __init__(self, dashboard_detail: _Optional[_Union[DashboardDetail, _Mapping]] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class CreateDashboardResponse(_message.Message):
    __slots__ = ("dashboard_id", "last_updated_at")
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    last_updated_at: _timestamp_pb2.Timestamp
    def __init__(self, dashboard_id: _Optional[str] = ..., last_updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UpdateDashboardRequest(_message.Message):
    __slots__ = ("dashboard_detail",)
    DASHBOARD_DETAIL_FIELD_NUMBER: _ClassVar[int]
    dashboard_detail: DashboardDetail
    def __init__(self, dashboard_detail: _Optional[_Union[DashboardDetail, _Mapping]] = ...) -> None: ...

class UpdateDashboardResponse(_message.Message):
    __slots__ = ("dashboard_id", "last_updated_at")
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    last_updated_at: _timestamp_pb2.Timestamp
    def __init__(self, dashboard_id: _Optional[str] = ..., last_updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetDashboardRequest(_message.Message):
    __slots__ = ("dashboard_id",)
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    def __init__(self, dashboard_id: _Optional[str] = ...) -> None: ...

class GetDashboardResponse(_message.Message):
    __slots__ = ("dashboard_detail",)
    DASHBOARD_DETAIL_FIELD_NUMBER: _ClassVar[int]
    dashboard_detail: DashboardDetail
    def __init__(self, dashboard_detail: _Optional[_Union[DashboardDetail, _Mapping]] = ...) -> None: ...

class DeleteDashboardRequest(_message.Message):
    __slots__ = ("dashboard_id",)
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    def __init__(self, dashboard_id: _Optional[str] = ...) -> None: ...

class DeleteDashboardResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListDashboardsRequest(_message.Message):
    __slots__ = ("project_id", "workspace_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    workspace_id: str
    def __init__(self, project_id: _Optional[str] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class ListDashboardsResponse(_message.Message):
    __slots__ = ("dashboard_detail",)
    DASHBOARD_DETAIL_FIELD_NUMBER: _ClassVar[int]
    dashboard_detail: _containers.RepeatedCompositeFieldContainer[DashboardDetail]
    def __init__(self, dashboard_detail: _Optional[_Iterable[_Union[DashboardDetail, _Mapping]]] = ...) -> None: ...

class QueryDataRequest(_message.Message):
    __slots__ = ("query_info", "models_info", "time_window_start", "time_window_end", "time_granularity", "segment_tags")
    QUERY_INFO_FIELD_NUMBER: _ClassVar[int]
    MODELS_INFO_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_START_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_END_FIELD_NUMBER: _ClassVar[int]
    TIME_GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_TAGS_FIELD_NUMBER: _ClassVar[int]
    query_info: QueryInfo
    models_info: _containers.RepeatedCompositeFieldContainer[ModelInfo]
    time_window_start: FlexibleTimestamp
    time_window_end: FlexibleTimestamp
    time_granularity: _duration_pb2.Duration
    segment_tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, query_info: _Optional[_Union[QueryInfo, _Mapping]] = ..., models_info: _Optional[_Iterable[_Union[ModelInfo, _Mapping]]] = ..., time_window_start: _Optional[_Union[FlexibleTimestamp, _Mapping]] = ..., time_window_end: _Optional[_Union[FlexibleTimestamp, _Mapping]] = ..., time_granularity: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., segment_tags: _Optional[_Iterable[str]] = ...) -> None: ...

class QueryDataResponse(_message.Message):
    __slots__ = ("row_major_value_table", "trace_id")
    ROW_MAJOR_VALUE_TABLE_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    row_major_value_table: _query_service_pb2.RowMajorValueTable
    trace_id: str
    def __init__(self, row_major_value_table: _Optional[_Union[_query_service_pb2.RowMajorValueTable, _Mapping]] = ..., trace_id: _Optional[str] = ...) -> None: ...

class ListSegmentTagsRequest(_message.Message):
    __slots__ = ("model_id", "model_output_type")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    model_id: _containers.RepeatedCompositeFieldContainer[_intelligence_service_pb2.ModelId]
    model_output_type: _model_output_type_pb2.ModelOutputType
    def __init__(self, model_id: _Optional[_Iterable[_Union[_intelligence_service_pb2.ModelId, _Mapping]]] = ..., model_output_type: _Optional[_Union[_model_output_type_pb2.ModelOutputType, str]] = ...) -> None: ...

class ListSegmentTagsResponse(_message.Message):
    __slots__ = ("segment_tags", "trace_id")
    SEGMENT_TAGS_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    segment_tags: _containers.RepeatedScalarFieldContainer[str]
    trace_id: str
    def __init__(self, segment_tags: _Optional[_Iterable[str]] = ..., trace_id: _Optional[str] = ...) -> None: ...

class ListCustomMetricsRequest(_message.Message):
    __slots__ = ("model_ids",)
    MODEL_IDS_FIELD_NUMBER: _ClassVar[int]
    model_ids: _containers.RepeatedCompositeFieldContainer[_intelligence_service_pb2.ModelId]
    def __init__(self, model_ids: _Optional[_Iterable[_Union[_intelligence_service_pb2.ModelId, _Mapping]]] = ...) -> None: ...

class ListCustomMetricsResponse(_message.Message):
    __slots__ = ("custom_metric_type_to_metrics_list_map",)
    CUSTOM_METRIC_TYPE_TO_METRICS_LIST_MAP_FIELD_NUMBER: _ClassVar[int]
    custom_metric_type_to_metrics_list_map: _containers.RepeatedCompositeFieldContainer[CustomMetricTypeToMetricsListMapEntry]
    def __init__(self, custom_metric_type_to_metrics_list_map: _Optional[_Iterable[_Union[CustomMetricTypeToMetricsListMapEntry, _Mapping]]] = ...) -> None: ...

class ModelInfo(_message.Message):
    __slots__ = ("model_id", "project_id", "baseline_split_id", "baseline_split_start_date", "baseline_split_end_date", "data_collection_id", "prod_split_id")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    BASELINE_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    BASELINE_SPLIT_START_DATE_FIELD_NUMBER: _ClassVar[int]
    BASELINE_SPLIT_END_DATE_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    PROD_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    project_id: str
    baseline_split_id: str
    baseline_split_start_date: _timestamp_pb2.Timestamp
    baseline_split_end_date: _timestamp_pb2.Timestamp
    data_collection_id: str
    prod_split_id: str
    def __init__(self, model_id: _Optional[str] = ..., project_id: _Optional[str] = ..., baseline_split_id: _Optional[str] = ..., baseline_split_start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., baseline_split_end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., data_collection_id: _Optional[str] = ..., prod_split_id: _Optional[str] = ...) -> None: ...

class PanelInfo(_message.Message):
    __slots__ = ("panel_type", "queries_info", "accuracy_type", "distance_type", "name", "segment_tags")
    PANEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    QUERIES_INFO_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_TAGS_FIELD_NUMBER: _ClassVar[int]
    panel_type: PanelType
    queries_info: _containers.RepeatedCompositeFieldContainer[QueryInfo]
    accuracy_type: _accuracy_pb2.AccuracyType.Type
    distance_type: _distance_pb2.DistanceType
    name: str
    segment_tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, panel_type: _Optional[_Union[PanelType, str]] = ..., queries_info: _Optional[_Iterable[_Union[QueryInfo, _Mapping]]] = ..., accuracy_type: _Optional[_Union[_accuracy_pb2.AccuracyType.Type, str]] = ..., distance_type: _Optional[_Union[_distance_pb2.DistanceType, str]] = ..., name: _Optional[str] = ..., segment_tags: _Optional[_Iterable[str]] = ...) -> None: ...

class QueryInfo(_message.Message):
    __slots__ = ("metric_type", "accuracy_type", "distance_type", "custom_metric")
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_METRIC_FIELD_NUMBER: _ClassVar[int]
    metric_type: MetricType
    accuracy_type: _accuracy_pb2.AccuracyType.Type
    distance_type: _distance_pb2.DistanceType
    custom_metric: CustomMetric
    def __init__(self, metric_type: _Optional[_Union[MetricType, str]] = ..., accuracy_type: _Optional[_Union[_accuracy_pb2.AccuracyType.Type, str]] = ..., distance_type: _Optional[_Union[_distance_pb2.DistanceType, str]] = ..., custom_metric: _Optional[_Union[CustomMetric, _Mapping]] = ...) -> None: ...

class CustomMetric(_message.Message):
    __slots__ = ("metric", "aggregation_type", "metric_type", "llm_metric_type")
    METRIC_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    LLM_METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    metric: str
    aggregation_type: _metric_pb2.MetricAggregationType
    metric_type: CustomMetricType
    llm_metric_type: LLMMetricType
    def __init__(self, metric: _Optional[str] = ..., aggregation_type: _Optional[_Union[_metric_pb2.MetricAggregationType, str]] = ..., metric_type: _Optional[_Union[CustomMetricType, str]] = ..., llm_metric_type: _Optional[_Union[LLMMetricType, str]] = ...) -> None: ...

class CustomMetricTypeToMetricsListMapEntry(_message.Message):
    __slots__ = ("metric_type", "metrics")
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metric_type: CustomMetricType
    metrics: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, metric_type: _Optional[_Union[CustomMetricType, str]] = ..., metrics: _Optional[_Iterable[str]] = ...) -> None: ...

class FlexibleTimestamp(_message.Message):
    __slots__ = ("relative", "absolute")
    RELATIVE_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    relative: str
    absolute: _timestamp_pb2.Timestamp
    def __init__(self, relative: _Optional[str] = ..., absolute: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DashboardMetadata(_message.Message):
    __slots__ = ("label", "description", "refresh_rate_seconds", "created_by_user_id", "dashboard_output_type", "last_updated_at", "time_granularity", "time_window_start", "time_window_end", "created_on", "analysis_type", "input_data_format")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REFRESH_RATE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    TIME_GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_START_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_END_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_TYPE_FIELD_NUMBER: _ClassVar[int]
    INPUT_DATA_FORMAT_FIELD_NUMBER: _ClassVar[int]
    label: str
    description: str
    refresh_rate_seconds: int
    created_by_user_id: str
    dashboard_output_type: _model_output_type_pb2.ModelOutputType
    last_updated_at: _timestamp_pb2.Timestamp
    time_granularity: _duration_pb2.Duration
    time_window_start: FlexibleTimestamp
    time_window_end: FlexibleTimestamp
    created_on: _timestamp_pb2.Timestamp
    analysis_type: _analysis_type_pb2.AnalysisType
    input_data_format: _metadata_message_types_pb2.InputDataFormat
    def __init__(self, label: _Optional[str] = ..., description: _Optional[str] = ..., refresh_rate_seconds: _Optional[int] = ..., created_by_user_id: _Optional[str] = ..., dashboard_output_type: _Optional[_Union[_model_output_type_pb2.ModelOutputType, str]] = ..., last_updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., time_granularity: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., time_window_start: _Optional[_Union[FlexibleTimestamp, _Mapping]] = ..., time_window_end: _Optional[_Union[FlexibleTimestamp, _Mapping]] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., analysis_type: _Optional[_Union[_analysis_type_pb2.AnalysisType, str]] = ..., input_data_format: _Optional[_Union[_metadata_message_types_pb2.InputDataFormat, str]] = ...) -> None: ...

class DashboardDetail(_message.Message):
    __slots__ = ("dashboard_id", "dashboard_metadata", "models_info", "panels_info")
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_METADATA_FIELD_NUMBER: _ClassVar[int]
    MODELS_INFO_FIELD_NUMBER: _ClassVar[int]
    PANELS_INFO_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    dashboard_metadata: DashboardMetadata
    models_info: _containers.RepeatedCompositeFieldContainer[ModelInfo]
    panels_info: _containers.RepeatedCompositeFieldContainer[PanelInfo]
    def __init__(self, dashboard_id: _Optional[str] = ..., dashboard_metadata: _Optional[_Union[DashboardMetadata, _Mapping]] = ..., models_info: _Optional[_Iterable[_Union[ModelInfo, _Mapping]]] = ..., panels_info: _Optional[_Iterable[_Union[PanelInfo, _Mapping]]] = ...) -> None: ...

class DashboardRecord(_message.Message):
    __slots__ = ("id", "dashboard_detail", "created_on")
    ID_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_DETAIL_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    id: str
    dashboard_detail: DashboardDetail
    created_on: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., dashboard_detail: _Optional[_Union[DashboardDetail, _Mapping]] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ValidateTimeRangeSplitBoundsRequest(_message.Message):
    __slots__ = ("project_id", "model_id", "split_id", "start_at", "end_at")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    START_AT_FIELD_NUMBER: _ClassVar[int]
    END_AT_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_id: str
    split_id: str
    start_at: _timestamp_pb2.Timestamp
    end_at: _timestamp_pb2.Timestamp
    def __init__(self, project_id: _Optional[str] = ..., model_id: _Optional[str] = ..., split_id: _Optional[str] = ..., start_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ValidateTimeRangeSplitBoundsResponse(_message.Message):
    __slots__ = ("data_point_count", "data_kind_label_percentage", "data_kind_fii_percentage", "allow_split_creation", "approximate_feature_count")
    DATA_POINT_COUNT_FIELD_NUMBER: _ClassVar[int]
    DATA_KIND_LABEL_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    DATA_KIND_FII_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    ALLOW_SPLIT_CREATION_FIELD_NUMBER: _ClassVar[int]
    APPROXIMATE_FEATURE_COUNT_FIELD_NUMBER: _ClassVar[int]
    data_point_count: float
    data_kind_label_percentage: float
    data_kind_fii_percentage: float
    allow_split_creation: bool
    approximate_feature_count: float
    def __init__(self, data_point_count: _Optional[float] = ..., data_kind_label_percentage: _Optional[float] = ..., data_kind_fii_percentage: _Optional[float] = ..., allow_split_creation: bool = ..., approximate_feature_count: _Optional[float] = ...) -> None: ...

class ApplicationFeedbackFunctionAggregate(_message.Message):
    __slots__ = ("function_id", "average_score")
    FUNCTION_ID_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_SCORE_FIELD_NUMBER: _ClassVar[int]
    function_id: str
    average_score: float
    def __init__(self, function_id: _Optional[str] = ..., average_score: _Optional[float] = ...) -> None: ...

class DataSplitMetadata(_message.Message):
    __slots__ = ("data_collection_id", "data_split_id", "data_split_type")
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    data_collection_id: str
    data_split_id: str
    data_split_type: _data_split_pb2.DataSplitType
    def __init__(self, data_collection_id: _Optional[str] = ..., data_split_id: _Optional[str] = ..., data_split_type: _Optional[_Union[_data_split_pb2.DataSplitType, str]] = ...) -> None: ...

class ApplicationAggregate(_message.Message):
    __slots__ = ("model_id", "average_latency", "total_cost", "total_tokens", "num_traces", "feedback_function_aggregates", "dataset_id")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_LATENCY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COST_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
    NUM_TRACES_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FUNCTION_AGGREGATES_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    average_latency: float
    total_cost: float
    total_tokens: int
    num_traces: int
    feedback_function_aggregates: _containers.RepeatedCompositeFieldContainer[ApplicationFeedbackFunctionAggregate]
    dataset_id: DataSplitMetadata
    def __init__(self, model_id: _Optional[str] = ..., average_latency: _Optional[float] = ..., total_cost: _Optional[float] = ..., total_tokens: _Optional[int] = ..., num_traces: _Optional[int] = ..., feedback_function_aggregates: _Optional[_Iterable[_Union[ApplicationFeedbackFunctionAggregate, _Mapping]]] = ..., dataset_id: _Optional[_Union[DataSplitMetadata, _Mapping]] = ...) -> None: ...

class ApplicationAggregatesRequest(_message.Message):
    __slots__ = ("project_id", "dataset_type")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_TYPE_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    dataset_type: _data_split_pb2.DataSplitType
    def __init__(self, project_id: _Optional[str] = ..., dataset_type: _Optional[_Union[_data_split_pb2.DataSplitType, str]] = ...) -> None: ...

class ApplicationAggregatesResponse(_message.Message):
    __slots__ = ("application_aggregate",)
    APPLICATION_AGGREGATE_FIELD_NUMBER: _ClassVar[int]
    application_aggregate: _containers.RepeatedCompositeFieldContainer[ApplicationAggregate]
    def __init__(self, application_aggregate: _Optional[_Iterable[_Union[ApplicationAggregate, _Mapping]]] = ...) -> None: ...

class ApplicationAggregateRequest(_message.Message):
    __slots__ = ("project_id", "dataset_type", "model_id", "data_split_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    dataset_type: _data_split_pb2.DataSplitType
    model_id: str
    data_split_id: str
    def __init__(self, project_id: _Optional[str] = ..., dataset_type: _Optional[_Union[_data_split_pb2.DataSplitType, str]] = ..., model_id: _Optional[str] = ..., data_split_id: _Optional[str] = ...) -> None: ...

class ApplicationAggregateResponse(_message.Message):
    __slots__ = ("application_aggregate",)
    APPLICATION_AGGREGATE_FIELD_NUMBER: _ClassVar[int]
    application_aggregate: ApplicationAggregate
    def __init__(self, application_aggregate: _Optional[_Union[ApplicationAggregate, _Mapping]] = ...) -> None: ...
