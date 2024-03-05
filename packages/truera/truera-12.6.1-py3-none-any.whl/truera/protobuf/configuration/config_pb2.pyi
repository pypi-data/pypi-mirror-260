from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from truera.protobuf.public.aiq import intelligence_service_pb2 as _intelligence_service_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from truera.protobuf.public.aiq import accuracy_pb2 as _accuracy_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MetricConfiguration(_message.Message):
    __slots__ = ("id", "project_id", "score_type", "accuracy_type", "score_interpretation", "bucketized_stats_type", "bias_configs", "maximum_model_runner_failure_rate")
    class ScoreInterpretation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[MetricConfiguration.ScoreInterpretation]
        HIGHER_IS_WORSE: _ClassVar[MetricConfiguration.ScoreInterpretation]
        LOWER_IS_WORSE: _ClassVar[MetricConfiguration.ScoreInterpretation]
    UNKNOWN: MetricConfiguration.ScoreInterpretation
    HIGHER_IS_WORSE: MetricConfiguration.ScoreInterpretation
    LOWER_IS_WORSE: MetricConfiguration.ScoreInterpretation
    class BiasTypeConfig(_message.Message):
        __slots__ = ("bias_type", "acceptable_min", "acceptable_max")
        BIAS_TYPE_FIELD_NUMBER: _ClassVar[int]
        ACCEPTABLE_MIN_FIELD_NUMBER: _ClassVar[int]
        ACCEPTABLE_MAX_FIELD_NUMBER: _ClassVar[int]
        bias_type: _intelligence_service_pb2.BiasType.Type
        acceptable_min: float
        acceptable_max: float
        def __init__(self, bias_type: _Optional[_Union[_intelligence_service_pb2.BiasType.Type, str]] = ..., acceptable_min: _Optional[float] = ..., acceptable_max: _Optional[float] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCORE_INTERPRETATION_FIELD_NUMBER: _ClassVar[int]
    BUCKETIZED_STATS_TYPE_FIELD_NUMBER: _ClassVar[int]
    BIAS_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_MODEL_RUNNER_FAILURE_RATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    score_type: _qoi_pb2.QuantityOfInterest
    accuracy_type: _containers.RepeatedScalarFieldContainer[_accuracy_pb2.AccuracyType.Type]
    score_interpretation: MetricConfiguration.ScoreInterpretation
    bucketized_stats_type: _intelligence_service_pb2.BucketizedStatsType.Type
    bias_configs: _containers.RepeatedCompositeFieldContainer[MetricConfiguration.BiasTypeConfig]
    maximum_model_runner_failure_rate: float
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ..., score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., accuracy_type: _Optional[_Iterable[_Union[_accuracy_pb2.AccuracyType.Type, str]]] = ..., score_interpretation: _Optional[_Union[MetricConfiguration.ScoreInterpretation, str]] = ..., bucketized_stats_type: _Optional[_Union[_intelligence_service_pb2.BucketizedStatsType.Type, str]] = ..., bias_configs: _Optional[_Iterable[_Union[MetricConfiguration.BiasTypeConfig, _Mapping]]] = ..., maximum_model_runner_failure_rate: _Optional[float] = ...) -> None: ...

class ClassificationThresholdConfiguration(_message.Message):
    __slots__ = ("id", "model_id", "threshold", "score_type")
    ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    model_id: _intelligence_service_pb2.ModelId
    threshold: float
    score_type: _qoi_pb2.QuantityOfInterest
    def __init__(self, id: _Optional[str] = ..., model_id: _Optional[_Union[_intelligence_service_pb2.ModelId, _Mapping]] = ..., threshold: _Optional[float] = ..., score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ...) -> None: ...
