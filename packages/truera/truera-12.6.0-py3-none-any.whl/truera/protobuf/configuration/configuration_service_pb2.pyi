from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from truera.protobuf.aiq import config_pb2 as _config_pb2
from truera.protobuf.configuration import config_pb2 as _config_pb2_1
from truera.protobuf.configuration import monitoring_pb2 as _monitoring_pb2
from truera.protobuf.configuration import project_pb2 as _project_pb2
from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from truera.protobuf.public.aiq import intelligence_service_pb2 as _intelligence_service_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateMetricConfigurationRequest(_message.Message):
    __slots__ = ("metric_configuration",)
    METRIC_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    metric_configuration: _config_pb2_1.MetricConfiguration
    def __init__(self, metric_configuration: _Optional[_Union[_config_pb2_1.MetricConfiguration, _Mapping]] = ...) -> None: ...

class UpdateMetricConfigurationResponse(_message.Message):
    __slots__ = ("metric_configuration",)
    METRIC_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    metric_configuration: _config_pb2_1.MetricConfiguration
    def __init__(self, metric_configuration: _Optional[_Union[_config_pb2_1.MetricConfiguration, _Mapping]] = ...) -> None: ...

class GetMetricConfigurationRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class GetMetricConfigurationResponse(_message.Message):
    __slots__ = ("metric_configuration",)
    METRIC_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    metric_configuration: _config_pb2_1.MetricConfiguration
    def __init__(self, metric_configuration: _Optional[_Union[_config_pb2_1.MetricConfiguration, _Mapping]] = ...) -> None: ...

class GetProjectDocumentationRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class GetProjectDocumentationResponse(_message.Message):
    __slots__ = ("documentation",)
    DOCUMENTATION_FIELD_NUMBER: _ClassVar[int]
    documentation: _project_pb2.ProjectDocumentation
    def __init__(self, documentation: _Optional[_Union[_project_pb2.ProjectDocumentation, _Mapping]] = ...) -> None: ...

class UpdateProjectDocumentationRequest(_message.Message):
    __slots__ = ("project_id", "mode", "documentation")
    class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[UpdateProjectDocumentationRequest.Mode]
        UPDATE: _ClassVar[UpdateProjectDocumentationRequest.Mode]
        DELETE: _ClassVar[UpdateProjectDocumentationRequest.Mode]
    UNKNOWN: UpdateProjectDocumentationRequest.Mode
    UPDATE: UpdateProjectDocumentationRequest.Mode
    DELETE: UpdateProjectDocumentationRequest.Mode
    class DocumentationEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTATION_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    mode: UpdateProjectDocumentationRequest.Mode
    documentation: _containers.ScalarMap[str, str]
    def __init__(self, project_id: _Optional[str] = ..., mode: _Optional[_Union[UpdateProjectDocumentationRequest.Mode, str]] = ..., documentation: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UpdateProjectDocumentationResponse(_message.Message):
    __slots__ = ("documentation",)
    DOCUMENTATION_FIELD_NUMBER: _ClassVar[int]
    documentation: _project_pb2.ProjectDocumentation
    def __init__(self, documentation: _Optional[_Union[_project_pb2.ProjectDocumentation, _Mapping]] = ...) -> None: ...

class GetAnalyticsConfigurationRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class GetAnalyticsConfigurationResponse(_message.Message):
    __slots__ = ("analytics_config",)
    ANALYTICS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    analytics_config: _config_pb2.AnalyticsConfig
    def __init__(self, analytics_config: _Optional[_Union[_config_pb2.AnalyticsConfig, _Mapping]] = ...) -> None: ...

class UpdateAnalyticsConfigurationRequest(_message.Message):
    __slots__ = ("analytics_config",)
    ANALYTICS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    analytics_config: _config_pb2.AnalyticsConfig
    def __init__(self, analytics_config: _Optional[_Union[_config_pb2.AnalyticsConfig, _Mapping]] = ...) -> None: ...

class UpdateAnalyticsConfigurationResponse(_message.Message):
    __slots__ = ("analytics_config",)
    ANALYTICS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    analytics_config: _config_pb2.AnalyticsConfig
    def __init__(self, analytics_config: _Optional[_Union[_config_pb2.AnalyticsConfig, _Mapping]] = ...) -> None: ...

class GetClassificationThresholdConfigurationRequest(_message.Message):
    __slots__ = ("model_id", "score_type", "infer_threshold_if_not_set")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    INFER_THRESHOLD_IF_NOT_SET_FIELD_NUMBER: _ClassVar[int]
    model_id: _intelligence_service_pb2.ModelId
    score_type: _qoi_pb2.QuantityOfInterest
    infer_threshold_if_not_set: bool
    def __init__(self, model_id: _Optional[_Union[_intelligence_service_pb2.ModelId, _Mapping]] = ..., score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., infer_threshold_if_not_set: bool = ...) -> None: ...

class GetClassificationThresholdConfigurationResponse(_message.Message):
    __slots__ = ("threshold_config", "inferred_threshold")
    THRESHOLD_CONFIG_FIELD_NUMBER: _ClassVar[int]
    INFERRED_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    threshold_config: _config_pb2_1.ClassificationThresholdConfiguration
    inferred_threshold: bool
    def __init__(self, threshold_config: _Optional[_Union[_config_pb2_1.ClassificationThresholdConfiguration, _Mapping]] = ..., inferred_threshold: bool = ...) -> None: ...

class UpdateClassificationThresholdConfigurationRequest(_message.Message):
    __slots__ = ("threshold_config",)
    THRESHOLD_CONFIG_FIELD_NUMBER: _ClassVar[int]
    threshold_config: _config_pb2_1.ClassificationThresholdConfiguration
    def __init__(self, threshold_config: _Optional[_Union[_config_pb2_1.ClassificationThresholdConfiguration, _Mapping]] = ...) -> None: ...

class UpdateClassificationThresholdConfigurationResponse(_message.Message):
    __slots__ = ("threshold_config",)
    THRESHOLD_CONFIG_FIELD_NUMBER: _ClassVar[int]
    threshold_config: _config_pb2_1.ClassificationThresholdConfiguration
    def __init__(self, threshold_config: _Optional[_Union[_config_pb2_1.ClassificationThresholdConfiguration, _Mapping]] = ...) -> None: ...

class GetBaseSplitRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "infer_base_split_if_not_set")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    INFER_BASE_SPLIT_IF_NOT_SET_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    infer_base_split_if_not_set: bool
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., infer_base_split_if_not_set: bool = ...) -> None: ...

class GetBaseSplitRequestResponse(_message.Message):
    __slots__ = ("split_id",)
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    split_id: str
    def __init__(self, split_id: _Optional[str] = ...) -> None: ...

class SetBaseSplitRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "split_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    split_id: str
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., split_id: _Optional[str] = ...) -> None: ...

class SetBaseSplitRequestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAllBaseSplitsRequest(_message.Message):
    __slots__ = ("project_id", "infer_base_split_if_not_set")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    INFER_BASE_SPLIT_IF_NOT_SET_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    infer_base_split_if_not_set: bool
    def __init__(self, project_id: _Optional[str] = ..., infer_base_split_if_not_set: bool = ...) -> None: ...

class GetAllBaseSplitsResponse(_message.Message):
    __slots__ = ("base_split_map",)
    class BaseSplitMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BASE_SPLIT_MAP_FIELD_NUMBER: _ClassVar[int]
    base_split_map: _containers.ScalarMap[str, str]
    def __init__(self, base_split_map: _Optional[_Mapping[str, str]] = ...) -> None: ...

class GetMonitoringConfigurationRequest(_message.Message):
    __slots__ = ("project_id", "model_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_id: str
    def __init__(self, project_id: _Optional[str] = ..., model_id: _Optional[str] = ...) -> None: ...

class GetMonitoringConfigurationResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: _monitoring_pb2.MonitoringConfig
    def __init__(self, config: _Optional[_Union[_monitoring_pb2.MonitoringConfig, _Mapping]] = ...) -> None: ...

class ListMonitoringConfigurationRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class ListMonitoringConfigurationResponse(_message.Message):
    __slots__ = ("configs",)
    CONFIGS_FIELD_NUMBER: _ClassVar[int]
    configs: _containers.RepeatedCompositeFieldContainer[_monitoring_pb2.MonitoringConfig]
    def __init__(self, configs: _Optional[_Iterable[_Union[_monitoring_pb2.MonitoringConfig, _Mapping]]] = ...) -> None: ...

class UpdateMonitoringConfigurationRequest(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: _monitoring_pb2.MonitoringConfig
    def __init__(self, config: _Optional[_Union[_monitoring_pb2.MonitoringConfig, _Mapping]] = ...) -> None: ...

class UpdateMonitoringConfigurationResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: _monitoring_pb2.MonitoringConfig
    def __init__(self, config: _Optional[_Union[_monitoring_pb2.MonitoringConfig, _Mapping]] = ...) -> None: ...
