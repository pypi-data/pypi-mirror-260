from google.api import visibility_pb2 as _visibility_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnalyticsConfig(_message.Message):
    __slots__ = ("id", "project_id", "algorithm_type", "num_bulk_instances", "num_samples", "num_estimate_metrics_baseline_samples", "num_estimate_metrics_estimate_samples", "ranking_k", "num_data_samples", "num_set_samples")
    class AlgorithmType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TRUERA_QII: _ClassVar[AnalyticsConfig.AlgorithmType]
        SHAP: _ClassVar[AnalyticsConfig.AlgorithmType]
        INTEGRATED_GRADIENTS: _ClassVar[AnalyticsConfig.AlgorithmType]
        NLP_SHAP: _ClassVar[AnalyticsConfig.AlgorithmType]
    TRUERA_QII: AnalyticsConfig.AlgorithmType
    SHAP: AnalyticsConfig.AlgorithmType
    INTEGRATED_GRADIENTS: AnalyticsConfig.AlgorithmType
    NLP_SHAP: AnalyticsConfig.AlgorithmType
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUM_BULK_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    NUM_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    NUM_ESTIMATE_METRICS_BASELINE_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    NUM_ESTIMATE_METRICS_ESTIMATE_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    RANKING_K_FIELD_NUMBER: _ClassVar[int]
    NUM_DATA_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    NUM_SET_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    algorithm_type: AnalyticsConfig.AlgorithmType
    num_bulk_instances: int
    num_samples: int
    num_estimate_metrics_baseline_samples: int
    num_estimate_metrics_estimate_samples: int
    ranking_k: int
    num_data_samples: int
    num_set_samples: int
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ..., algorithm_type: _Optional[_Union[AnalyticsConfig.AlgorithmType, str]] = ..., num_bulk_instances: _Optional[int] = ..., num_samples: _Optional[int] = ..., num_estimate_metrics_baseline_samples: _Optional[int] = ..., num_estimate_metrics_estimate_samples: _Optional[int] = ..., ranking_k: _Optional[int] = ..., num_data_samples: _Optional[int] = ..., num_set_samples: _Optional[int] = ...) -> None: ...
