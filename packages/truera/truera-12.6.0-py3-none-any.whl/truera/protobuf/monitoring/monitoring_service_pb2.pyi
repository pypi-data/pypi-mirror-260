from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from truera.protobuf.monitoring import grafana_record_pb2 as _grafana_record_pb2
from truera.protobuf.monitoring import monitoring_computation_pb2 as _monitoring_computation_pb2
from truera.protobuf.public.aiq import intelligence_service_pb2 as _intelligence_service_pb2
from truera.protobuf.public.common import metric_pb2 as _metric_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MonitoringRpcStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[MonitoringRpcStatus]
    SUCCESS: _ClassVar[MonitoringRpcStatus]
    PENDING: _ClassVar[MonitoringRpcStatus]
UNKNOWN: MonitoringRpcStatus
SUCCESS: MonitoringRpcStatus
PENDING: MonitoringRpcStatus

class GetEnabledModelsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetEnabledModelsResponse(_message.Message):
    __slots__ = ("enabled_models",)
    class MonitoringModelStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_MONITORING_MODEL_STATUS: _ClassVar[GetEnabledModelsResponse.MonitoringModelStatus]
        MISSING_VALID_SPLIT: _ClassVar[GetEnabledModelsResponse.MonitoringModelStatus]
        MONITORING: _ClassVar[GetEnabledModelsResponse.MonitoringModelStatus]
    UNKNOWN_MONITORING_MODEL_STATUS: GetEnabledModelsResponse.MonitoringModelStatus
    MISSING_VALID_SPLIT: GetEnabledModelsResponse.MonitoringModelStatus
    MONITORING: GetEnabledModelsResponse.MonitoringModelStatus
    class EnabledModel(_message.Message):
        __slots__ = ("model_id", "monitoring_model_status")
        MODEL_ID_FIELD_NUMBER: _ClassVar[int]
        MONITORING_MODEL_STATUS_FIELD_NUMBER: _ClassVar[int]
        model_id: _intelligence_service_pb2.ModelId
        monitoring_model_status: GetEnabledModelsResponse.MonitoringModelStatus
        def __init__(self, model_id: _Optional[_Union[_intelligence_service_pb2.ModelId, _Mapping]] = ..., monitoring_model_status: _Optional[_Union[GetEnabledModelsResponse.MonitoringModelStatus, str]] = ...) -> None: ...
    ENABLED_MODELS_FIELD_NUMBER: _ClassVar[int]
    enabled_models: _containers.RepeatedCompositeFieldContainer[GetEnabledModelsResponse.EnabledModel]
    def __init__(self, enabled_models: _Optional[_Iterable[_Union[GetEnabledModelsResponse.EnabledModel, _Mapping]]] = ...) -> None: ...

class RefreshGrafanaDashboardRequest(_message.Message):
    __slots__ = ("model_id",)
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    model_id: _intelligence_service_pb2.ModelId
    def __init__(self, model_id: _Optional[_Union[_intelligence_service_pb2.ModelId, _Mapping]] = ...) -> None: ...

class RefreshGrafanaDashboardResponse(_message.Message):
    __slots__ = ("model_record",)
    MODEL_RECORD_FIELD_NUMBER: _ClassVar[int]
    model_record: _grafana_record_pb2.GrafanaModelRecord
    def __init__(self, model_record: _Optional[_Union[_grafana_record_pb2.GrafanaModelRecord, _Mapping]] = ...) -> None: ...

class GetGrafanaRecordRequest(_message.Message):
    __slots__ = ("model_id",)
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    model_id: _containers.RepeatedCompositeFieldContainer[_intelligence_service_pb2.ModelId]
    def __init__(self, model_id: _Optional[_Iterable[_Union[_intelligence_service_pb2.ModelId, _Mapping]]] = ...) -> None: ...

class GetGrafanaRecordResponse(_message.Message):
    __slots__ = ("grafana_record_summaries",)
    class GrafanaRecordSummary(_message.Message):
        __slots__ = ("status", "model_record")
        STATUS_FIELD_NUMBER: _ClassVar[int]
        MODEL_RECORD_FIELD_NUMBER: _ClassVar[int]
        status: MonitoringRpcStatus
        model_record: _grafana_record_pb2.GrafanaModelRecord
        def __init__(self, status: _Optional[_Union[MonitoringRpcStatus, str]] = ..., model_record: _Optional[_Union[_grafana_record_pb2.GrafanaModelRecord, _Mapping]] = ...) -> None: ...
    GRAFANA_RECORD_SUMMARIES_FIELD_NUMBER: _ClassVar[int]
    grafana_record_summaries: _containers.RepeatedCompositeFieldContainer[GetGrafanaRecordResponse.GrafanaRecordSummary]
    def __init__(self, grafana_record_summaries: _Optional[_Iterable[_Union[GetGrafanaRecordResponse.GrafanaRecordSummary, _Mapping]]] = ...) -> None: ...

class GetDataQualitySummaryRequest(_message.Message):
    __slots__ = ("project_id", "split_id", "data_collection_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    split_id: str
    data_collection_id: str
    def __init__(self, project_id: _Optional[str] = ..., split_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ...) -> None: ...

class GetDataQualitySummaryResponse(_message.Message):
    __slots__ = ("data_quality_status", "total_violations", "total_rules")
    DATA_QUALITY_STATUS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_VIOLATIONS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_RULES_FIELD_NUMBER: _ClassVar[int]
    data_quality_status: MonitoringRpcStatus
    total_violations: float
    total_rules: float
    def __init__(self, data_quality_status: _Optional[_Union[MonitoringRpcStatus, str]] = ..., total_violations: _Optional[float] = ..., total_rules: _Optional[float] = ...) -> None: ...

class GetTaskCollectionStatusSummaryRequest(_message.Message):
    __slots__ = ("project_id", "filter")
    class TaskCollectionFilter(_message.Message):
        __slots__ = ("model_id", "data_collection_id", "split_id")
        MODEL_ID_FIELD_NUMBER: _ClassVar[int]
        DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
        SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
        model_id: str
        data_collection_id: str
        split_id: str
        def __init__(self, model_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., split_id: _Optional[str] = ...) -> None: ...
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    filter: _containers.RepeatedCompositeFieldContainer[GetTaskCollectionStatusSummaryRequest.TaskCollectionFilter]
    def __init__(self, project_id: _Optional[str] = ..., filter: _Optional[_Iterable[_Union[GetTaskCollectionStatusSummaryRequest.TaskCollectionFilter, _Mapping]]] = ...) -> None: ...

class GetTaskCollectionStatusSummaryResponse(_message.Message):
    __slots__ = ("status_summary",)
    class TaskCollectionStatusSummary(_message.Message):
        __slots__ = ("id", "task_collection_id", "started_at", "updated_at", "failed_tasks", "successful_tasks", "total_tasks", "generated_split_tags")
        class GeneratedSplitTags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            UNDEFINED: _ClassVar[GetTaskCollectionStatusSummaryResponse.TaskCollectionStatusSummary.GeneratedSplitTags]
            NO_LABELS: _ClassVar[GetTaskCollectionStatusSummaryResponse.TaskCollectionStatusSummary.GeneratedSplitTags]
        UNDEFINED: GetTaskCollectionStatusSummaryResponse.TaskCollectionStatusSummary.GeneratedSplitTags
        NO_LABELS: GetTaskCollectionStatusSummaryResponse.TaskCollectionStatusSummary.GeneratedSplitTags
        ID_FIELD_NUMBER: _ClassVar[int]
        TASK_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
        STARTED_AT_FIELD_NUMBER: _ClassVar[int]
        UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
        FAILED_TASKS_FIELD_NUMBER: _ClassVar[int]
        SUCCESSFUL_TASKS_FIELD_NUMBER: _ClassVar[int]
        TOTAL_TASKS_FIELD_NUMBER: _ClassVar[int]
        GENERATED_SPLIT_TAGS_FIELD_NUMBER: _ClassVar[int]
        id: str
        task_collection_id: _monitoring_computation_pb2.MonitoringTaskCollection.MonitoringTaskCollectionId
        started_at: _timestamp_pb2.Timestamp
        updated_at: _timestamp_pb2.Timestamp
        failed_tasks: int
        successful_tasks: int
        total_tasks: int
        generated_split_tags: _containers.RepeatedScalarFieldContainer[GetTaskCollectionStatusSummaryResponse.TaskCollectionStatusSummary.GeneratedSplitTags]
        def __init__(self, id: _Optional[str] = ..., task_collection_id: _Optional[_Union[_monitoring_computation_pb2.MonitoringTaskCollection.MonitoringTaskCollectionId, _Mapping]] = ..., started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., failed_tasks: _Optional[int] = ..., successful_tasks: _Optional[int] = ..., total_tasks: _Optional[int] = ..., generated_split_tags: _Optional[_Iterable[_Union[GetTaskCollectionStatusSummaryResponse.TaskCollectionStatusSummary.GeneratedSplitTags, str]]] = ...) -> None: ...
    STATUS_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    status_summary: _containers.RepeatedCompositeFieldContainer[GetTaskCollectionStatusSummaryResponse.TaskCollectionStatusSummary]
    def __init__(self, status_summary: _Optional[_Iterable[_Union[GetTaskCollectionStatusSummaryResponse.TaskCollectionStatusSummary, _Mapping]]] = ...) -> None: ...

class TaskStatusDetails(_message.Message):
    __slots__ = ("id", "task_name", "segment_name", "started_at", "updated_at", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    TASK_NAME_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    task_name: str
    segment_name: str
    started_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    status: _monitoring_computation_pb2.MonitoringComputationTask.TaskStatus
    def __init__(self, id: _Optional[str] = ..., task_name: _Optional[str] = ..., segment_name: _Optional[str] = ..., started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[_monitoring_computation_pb2.MonitoringComputationTask.TaskStatus, _Mapping]] = ...) -> None: ...

class GetTaskCollectionStatusDetailsRequest(_message.Message):
    __slots__ = ("task_collection_id",)
    TASK_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    task_collection_id: str
    def __init__(self, task_collection_id: _Optional[str] = ...) -> None: ...

class GetTaskCollectionStatusDetailsResponse(_message.Message):
    __slots__ = ("task_collection_id", "task_details")
    TASK_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_DETAILS_FIELD_NUMBER: _ClassVar[int]
    task_collection_id: str
    task_details: _containers.RepeatedCompositeFieldContainer[TaskStatusDetails]
    def __init__(self, task_collection_id: _Optional[str] = ..., task_details: _Optional[_Iterable[_Union[TaskStatusDetails, _Mapping]]] = ...) -> None: ...

class RetryTaskRequest(_message.Message):
    __slots__ = ("task_id", "task_collection_id")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    task_collection_id: str
    def __init__(self, task_id: _Optional[str] = ..., task_collection_id: _Optional[str] = ...) -> None: ...

class RetryTaskResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: TaskStatusDetails
    def __init__(self, status: _Optional[_Union[TaskStatusDetails, _Mapping]] = ...) -> None: ...

class PutMetricDefinitionRequest(_message.Message):
    __slots__ = ("metric",)
    METRIC_FIELD_NUMBER: _ClassVar[int]
    metric: _metric_pb2.MetricDefinition
    def __init__(self, metric: _Optional[_Union[_metric_pb2.MetricDefinition, _Mapping]] = ...) -> None: ...

class PutMetricDefinitionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetMetricDefinitionRequest(_message.Message):
    __slots__ = ("project_id", "metric_name")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    metric_name: str
    def __init__(self, project_id: _Optional[str] = ..., metric_name: _Optional[str] = ...) -> None: ...

class GetMetricDefinitionResponse(_message.Message):
    __slots__ = ("metric",)
    METRIC_FIELD_NUMBER: _ClassVar[int]
    metric: _metric_pb2.MetricDefinition
    def __init__(self, metric: _Optional[_Union[_metric_pb2.MetricDefinition, _Mapping]] = ...) -> None: ...

class DeleteMetricDefinitionRequest(_message.Message):
    __slots__ = ("project_id", "metric_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    METRIC_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    metric_id: str
    def __init__(self, project_id: _Optional[str] = ..., metric_id: _Optional[str] = ...) -> None: ...

class DeleteMetricDefinitionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
