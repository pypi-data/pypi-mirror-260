from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EstimateType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NONE: _ClassVar[EstimateType]
    ESTIMATE_IF_UNAVAILABLE: _ClassVar[EstimateType]
    FORCE_ESTIMATE: _ClassVar[EstimateType]
NONE: EstimateType
ESTIMATE_IF_UNAVAILABLE: EstimateType
FORCE_ESTIMATE: EstimateType

class AccuracyType(_message.Message):
    __slots__ = ()
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[AccuracyType.Type]
        AUC: _ClassVar[AccuracyType.Type]
        GINI: _ClassVar[AccuracyType.Type]
        LOG_LOSS: _ClassVar[AccuracyType.Type]
        CLASSIFICATION_ACCURACY: _ClassVar[AccuracyType.Type]
        PRECISION: _ClassVar[AccuracyType.Type]
        RECALL: _ClassVar[AccuracyType.Type]
        F1: _ClassVar[AccuracyType.Type]
        TRUE_POSITIVE_RATE: _ClassVar[AccuracyType.Type]
        TRUE_NEGATIVE_RATE: _ClassVar[AccuracyType.Type]
        FALSE_POSITIVE_RATE: _ClassVar[AccuracyType.Type]
        FALSE_NEGATIVE_RATE: _ClassVar[AccuracyType.Type]
        NEGATIVE_PREDICTIVE_VALUE: _ClassVar[AccuracyType.Type]
        JACCARD_INDEX: _ClassVar[AccuracyType.Type]
        MATTHEWS_CORRCOEF: _ClassVar[AccuracyType.Type]
        AVERAGE_PRECISION: _ClassVar[AccuracyType.Type]
        ACCURACY_RATIO: _ClassVar[AccuracyType.Type]
        SEGMENT_GENERALIZED_AUC: _ClassVar[AccuracyType.Type]
        SEGMENT_GENERALIZED_GINI: _ClassVar[AccuracyType.Type]
        SEGMENT_GENERALIZED_ACCURACY_RATIO: _ClassVar[AccuracyType.Type]
        RMSE: _ClassVar[AccuracyType.Type]
        MSE: _ClassVar[AccuracyType.Type]
        MAE: _ClassVar[AccuracyType.Type]
        MSLE: _ClassVar[AccuracyType.Type]
        R_SQUARED: _ClassVar[AccuracyType.Type]
        EXPLAINED_VARIANCE: _ClassVar[AccuracyType.Type]
        MAPE: _ClassVar[AccuracyType.Type]
        WMAPE: _ClassVar[AccuracyType.Type]
        MEAN_PERCENTAGE_ERROR: _ClassVar[AccuracyType.Type]
        NORMALIZED_MEAN_BIAS: _ClassVar[AccuracyType.Type]
        NDCG: _ClassVar[AccuracyType.Type]
    UNKNOWN: AccuracyType.Type
    AUC: AccuracyType.Type
    GINI: AccuracyType.Type
    LOG_LOSS: AccuracyType.Type
    CLASSIFICATION_ACCURACY: AccuracyType.Type
    PRECISION: AccuracyType.Type
    RECALL: AccuracyType.Type
    F1: AccuracyType.Type
    TRUE_POSITIVE_RATE: AccuracyType.Type
    TRUE_NEGATIVE_RATE: AccuracyType.Type
    FALSE_POSITIVE_RATE: AccuracyType.Type
    FALSE_NEGATIVE_RATE: AccuracyType.Type
    NEGATIVE_PREDICTIVE_VALUE: AccuracyType.Type
    JACCARD_INDEX: AccuracyType.Type
    MATTHEWS_CORRCOEF: AccuracyType.Type
    AVERAGE_PRECISION: AccuracyType.Type
    ACCURACY_RATIO: AccuracyType.Type
    SEGMENT_GENERALIZED_AUC: AccuracyType.Type
    SEGMENT_GENERALIZED_GINI: AccuracyType.Type
    SEGMENT_GENERALIZED_ACCURACY_RATIO: AccuracyType.Type
    RMSE: AccuracyType.Type
    MSE: AccuracyType.Type
    MAE: AccuracyType.Type
    MSLE: AccuracyType.Type
    R_SQUARED: AccuracyType.Type
    EXPLAINED_VARIANCE: AccuracyType.Type
    MAPE: AccuracyType.Type
    WMAPE: AccuracyType.Type
    MEAN_PERCENTAGE_ERROR: AccuracyType.Type
    NORMALIZED_MEAN_BIAS: AccuracyType.Type
    NDCG: AccuracyType.Type
    def __init__(self) -> None: ...

class AccuracyEstimateConfidence(_message.Message):
    __slots__ = ()
    class Confidence(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOW: _ClassVar[AccuracyEstimateConfidence.Confidence]
        MEDIUM: _ClassVar[AccuracyEstimateConfidence.Confidence]
        HIGH: _ClassVar[AccuracyEstimateConfidence.Confidence]
    LOW: AccuracyEstimateConfidence.Confidence
    MEDIUM: AccuracyEstimateConfidence.Confidence
    HIGH: AccuracyEstimateConfidence.Confidence
    def __init__(self) -> None: ...

class AccuracyResult(_message.Message):
    __slots__ = ("value", "error_message", "type", "interpretation", "computation_record_count")
    class AccuracyResultType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        VALUE: _ClassVar[AccuracyResult.AccuracyResultType]
        ONLY_ONE_LABEL_CLASS: _ClassVar[AccuracyResult.AccuracyResultType]
        SEGMENT_TOO_RESTRICTIVE: _ClassVar[AccuracyResult.AccuracyResultType]
        MISSING_OR_SMALL_BASELINE: _ClassVar[AccuracyResult.AccuracyResultType]
        UNSUPPORTED_MODEL_TYPE: _ClassVar[AccuracyResult.AccuracyResultType]
        CANNOT_COMPUTE_PREDICTIONS: _ClassVar[AccuracyResult.AccuracyResultType]
        UNKNOWN_EXCEPTION: _ClassVar[AccuracyResult.AccuracyResultType]
        PREDICTION_UNAVAILABLE: _ClassVar[AccuracyResult.AccuracyResultType]
    VALUE: AccuracyResult.AccuracyResultType
    ONLY_ONE_LABEL_CLASS: AccuracyResult.AccuracyResultType
    SEGMENT_TOO_RESTRICTIVE: AccuracyResult.AccuracyResultType
    MISSING_OR_SMALL_BASELINE: AccuracyResult.AccuracyResultType
    UNSUPPORTED_MODEL_TYPE: AccuracyResult.AccuracyResultType
    CANNOT_COMPUTE_PREDICTIONS: AccuracyResult.AccuracyResultType
    UNKNOWN_EXCEPTION: AccuracyResult.AccuracyResultType
    PREDICTION_UNAVAILABLE: AccuracyResult.AccuracyResultType
    class AccuracyInterpretation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[AccuracyResult.AccuracyInterpretation]
        HIGHER_IS_BETTER: _ClassVar[AccuracyResult.AccuracyInterpretation]
        LOWER_IS_BETTER: _ClassVar[AccuracyResult.AccuracyInterpretation]
    UNKNOWN: AccuracyResult.AccuracyInterpretation
    HIGHER_IS_BETTER: AccuracyResult.AccuracyInterpretation
    LOWER_IS_BETTER: AccuracyResult.AccuracyInterpretation
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INTERPRETATION_FIELD_NUMBER: _ClassVar[int]
    COMPUTATION_RECORD_COUNT_FIELD_NUMBER: _ClassVar[int]
    value: float
    error_message: str
    type: AccuracyResult.AccuracyResultType
    interpretation: AccuracyResult.AccuracyInterpretation
    computation_record_count: int
    def __init__(self, value: _Optional[float] = ..., error_message: _Optional[str] = ..., type: _Optional[_Union[AccuracyResult.AccuracyResultType, str]] = ..., interpretation: _Optional[_Union[AccuracyResult.AccuracyInterpretation, str]] = ..., computation_record_count: _Optional[int] = ...) -> None: ...

class PrecisionRecallCurve(_message.Message):
    __slots__ = ("precision", "recall", "thresholds", "computation_record_count")
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    RECALL_FIELD_NUMBER: _ClassVar[int]
    THRESHOLDS_FIELD_NUMBER: _ClassVar[int]
    COMPUTATION_RECORD_COUNT_FIELD_NUMBER: _ClassVar[int]
    precision: _containers.RepeatedScalarFieldContainer[float]
    recall: _containers.RepeatedScalarFieldContainer[float]
    thresholds: _containers.RepeatedScalarFieldContainer[float]
    computation_record_count: int
    def __init__(self, precision: _Optional[_Iterable[float]] = ..., recall: _Optional[_Iterable[float]] = ..., thresholds: _Optional[_Iterable[float]] = ..., computation_record_count: _Optional[int] = ...) -> None: ...

class RocCurve(_message.Message):
    __slots__ = ("fpr", "tpr", "thresholds", "computation_record_count")
    FPR_FIELD_NUMBER: _ClassVar[int]
    TPR_FIELD_NUMBER: _ClassVar[int]
    THRESHOLDS_FIELD_NUMBER: _ClassVar[int]
    COMPUTATION_RECORD_COUNT_FIELD_NUMBER: _ClassVar[int]
    fpr: _containers.RepeatedScalarFieldContainer[float]
    tpr: _containers.RepeatedScalarFieldContainer[float]
    thresholds: _containers.RepeatedScalarFieldContainer[float]
    computation_record_count: int
    def __init__(self, fpr: _Optional[_Iterable[float]] = ..., tpr: _Optional[_Iterable[float]] = ..., thresholds: _Optional[_Iterable[float]] = ..., computation_record_count: _Optional[int] = ...) -> None: ...

class ConfusionMatrix(_message.Message):
    __slots__ = ("true_positive_count", "false_positive_count", "true_negative_count", "false_negative_count", "computation_record_count")
    TRUE_POSITIVE_COUNT_FIELD_NUMBER: _ClassVar[int]
    FALSE_POSITIVE_COUNT_FIELD_NUMBER: _ClassVar[int]
    TRUE_NEGATIVE_COUNT_FIELD_NUMBER: _ClassVar[int]
    FALSE_NEGATIVE_COUNT_FIELD_NUMBER: _ClassVar[int]
    COMPUTATION_RECORD_COUNT_FIELD_NUMBER: _ClassVar[int]
    true_positive_count: int
    false_positive_count: int
    true_negative_count: int
    false_negative_count: int
    computation_record_count: int
    def __init__(self, true_positive_count: _Optional[int] = ..., false_positive_count: _Optional[int] = ..., true_negative_count: _Optional[int] = ..., false_negative_count: _Optional[int] = ..., computation_record_count: _Optional[int] = ...) -> None: ...
