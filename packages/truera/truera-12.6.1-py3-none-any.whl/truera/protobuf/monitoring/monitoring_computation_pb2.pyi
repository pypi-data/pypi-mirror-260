from google.protobuf import timestamp_pb2 as _timestamp_pb2
from truera.protobuf.public.data import filter_pb2 as _filter_pb2
from truera.protobuf.monitoring import monitoring_enums_pb2 as _monitoring_enums_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from truera.protobuf.public.util import split_mode_pb2 as _split_mode_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ComputationScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNDEFINED_COMPUTATION_SCOPE: _ClassVar[ComputationScope]
    MODEL: _ClassVar[ComputationScope]
    DATA_COLLECTION: _ClassVar[ComputationScope]
UNDEFINED_COMPUTATION_SCOPE: ComputationScope
MODEL: ComputationScope
DATA_COLLECTION: ComputationScope

class MonitoringComputationTask(_message.Message):
    __slots__ = ("id", "monitoring_task_id", "monitoring_task_collection_id", "task_type", "created_on", "updated_on", "status_history")
    class MonitoringComputationLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNDEFINED: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        MODEL_STABILITY_SCORE: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        FEATURE_INFLUENCE_SCORE: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        PREDICTION_SCORE_SUMMARY: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        FEATURE_VALUES_SUMMARY: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        MODEL_SCORE_DISPARITY: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        FEATURE_CONTRIBUTION_SCORE_DISPARITY: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        ACCURACY: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        ESTIMATED_ACCURACY: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        CLASSIFICATION_SUMMARY: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        DATA_QUALITY: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        FEATURE_DRIFT: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        GROUND_TRUTH_LABELS: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        MODEL_BIAS: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
        SCHEMA_MISMATCH: _ClassVar[MonitoringComputationTask.MonitoringComputationLevel]
    UNDEFINED: MonitoringComputationTask.MonitoringComputationLevel
    MODEL_STABILITY_SCORE: MonitoringComputationTask.MonitoringComputationLevel
    FEATURE_INFLUENCE_SCORE: MonitoringComputationTask.MonitoringComputationLevel
    PREDICTION_SCORE_SUMMARY: MonitoringComputationTask.MonitoringComputationLevel
    FEATURE_VALUES_SUMMARY: MonitoringComputationTask.MonitoringComputationLevel
    MODEL_SCORE_DISPARITY: MonitoringComputationTask.MonitoringComputationLevel
    FEATURE_CONTRIBUTION_SCORE_DISPARITY: MonitoringComputationTask.MonitoringComputationLevel
    ACCURACY: MonitoringComputationTask.MonitoringComputationLevel
    ESTIMATED_ACCURACY: MonitoringComputationTask.MonitoringComputationLevel
    CLASSIFICATION_SUMMARY: MonitoringComputationTask.MonitoringComputationLevel
    DATA_QUALITY: MonitoringComputationTask.MonitoringComputationLevel
    FEATURE_DRIFT: MonitoringComputationTask.MonitoringComputationLevel
    GROUND_TRUTH_LABELS: MonitoringComputationTask.MonitoringComputationLevel
    MODEL_BIAS: MonitoringComputationTask.MonitoringComputationLevel
    SCHEMA_MISMATCH: MonitoringComputationTask.MonitoringComputationLevel
    class TaskStatus(_message.Message):
        __slots__ = ("status_code", "error_message", "attempt", "updated_on")
        STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
        ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
        ATTEMPT_FIELD_NUMBER: _ClassVar[int]
        UPDATED_ON_FIELD_NUMBER: _ClassVar[int]
        status_code: _monitoring_enums_pb2.MonitoringTaskStatus
        error_message: str
        attempt: int
        updated_on: _timestamp_pb2.Timestamp
        def __init__(self, status_code: _Optional[_Union[_monitoring_enums_pb2.MonitoringTaskStatus, str]] = ..., error_message: _Optional[str] = ..., attempt: _Optional[int] = ..., updated_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    MONITORING_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    MONITORING_TASK_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    UPDATED_ON_FIELD_NUMBER: _ClassVar[int]
    STATUS_HISTORY_FIELD_NUMBER: _ClassVar[int]
    id: str
    monitoring_task_id: MonitoringTaskId
    monitoring_task_collection_id: str
    task_type: MonitoringComputationTask.MonitoringComputationLevel
    created_on: _timestamp_pb2.Timestamp
    updated_on: _timestamp_pb2.Timestamp
    status_history: _containers.RepeatedCompositeFieldContainer[MonitoringComputationTask.TaskStatus]
    def __init__(self, id: _Optional[str] = ..., monitoring_task_id: _Optional[_Union[MonitoringTaskId, _Mapping]] = ..., monitoring_task_collection_id: _Optional[str] = ..., task_type: _Optional[_Union[MonitoringComputationTask.MonitoringComputationLevel, str]] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status_history: _Optional[_Iterable[_Union[MonitoringComputationTask.TaskStatus, _Mapping]]] = ...) -> None: ...

class MonitoringTaskId(_message.Message):
    __slots__ = ("project_id", "model_id", "data_collection_id", "split_id", "computation_scope", "task_type", "base_split_id", "use_segment_filter", "segmentation_id", "segment_filter_expression", "pretty_segment_name")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    COMPUTATION_SCOPE_FIELD_NUMBER: _ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: _ClassVar[int]
    BASE_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    USE_SEGMENT_FILTER_FIELD_NUMBER: _ClassVar[int]
    SEGMENTATION_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_FILTER_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    PRETTY_SEGMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_id: str
    data_collection_id: str
    split_id: str
    computation_scope: ComputationScope
    task_type: MonitoringComputationTask.MonitoringComputationLevel
    base_split_id: str
    use_segment_filter: bool
    segmentation_id: str
    segment_filter_expression: _filter_pb2.FilterExpression
    pretty_segment_name: str
    def __init__(self, project_id: _Optional[str] = ..., model_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., split_id: _Optional[str] = ..., computation_scope: _Optional[_Union[ComputationScope, str]] = ..., task_type: _Optional[_Union[MonitoringComputationTask.MonitoringComputationLevel, str]] = ..., base_split_id: _Optional[str] = ..., use_segment_filter: bool = ..., segmentation_id: _Optional[str] = ..., segment_filter_expression: _Optional[_Union[_filter_pb2.FilterExpression, _Mapping]] = ..., pretty_segment_name: _Optional[str] = ...) -> None: ...

class MonitoringTaskCollection(_message.Message):
    __slots__ = ("id", "monitoring_task_collection_id", "task_status_details", "created_on", "generated_from")
    class MonitoringTaskCollectionId(_message.Message):
        __slots__ = ("project_id", "model_id", "data_collection_id", "split_id", "computation_scope")
        PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
        MODEL_ID_FIELD_NUMBER: _ClassVar[int]
        DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
        SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
        COMPUTATION_SCOPE_FIELD_NUMBER: _ClassVar[int]
        project_id: str
        model_id: str
        data_collection_id: str
        split_id: str
        computation_scope: ComputationScope
        def __init__(self, project_id: _Optional[str] = ..., model_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., split_id: _Optional[str] = ..., computation_scope: _Optional[_Union[ComputationScope, str]] = ...) -> None: ...
    class TaskStatusDetailsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: MonitoringComputationTask
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[MonitoringComputationTask, _Mapping]] = ...) -> None: ...
    class GeneratedFrom(_message.Message):
        __slots__ = ("label_locator", "split_mode")
        LABEL_LOCATOR_FIELD_NUMBER: _ClassVar[int]
        SPLIT_MODE_FIELD_NUMBER: _ClassVar[int]
        label_locator: str
        split_mode: _split_mode_pb2.SplitMode
        def __init__(self, label_locator: _Optional[str] = ..., split_mode: _Optional[_Union[_split_mode_pb2.SplitMode, str]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    MONITORING_TASK_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_STATUS_DETAILS_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    GENERATED_FROM_FIELD_NUMBER: _ClassVar[int]
    id: str
    monitoring_task_collection_id: MonitoringTaskCollection.MonitoringTaskCollectionId
    task_status_details: _containers.MessageMap[str, MonitoringComputationTask]
    created_on: _timestamp_pb2.Timestamp
    generated_from: MonitoringTaskCollection.GeneratedFrom
    def __init__(self, id: _Optional[str] = ..., monitoring_task_collection_id: _Optional[_Union[MonitoringTaskCollection.MonitoringTaskCollectionId, _Mapping]] = ..., task_status_details: _Optional[_Mapping[str, MonitoringComputationTask]] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., generated_from: _Optional[_Union[MonitoringTaskCollection.GeneratedFrom, _Mapping]] = ...) -> None: ...
