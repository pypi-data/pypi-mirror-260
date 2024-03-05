from truera.protobuf.public.aiq import intelligence_service_pb2 as _intelligence_service_pb2
from truera.protobuf.public.aiq import distance_pb2 as _distance_pb2
from truera.protobuf.public.data import segment_pb2 as _segment_pb2
from truera.protobuf.public.aiq import accuracy_pb2 as _accuracy_pb2
from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModelTestType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODEL_TEST_TYPE_UNDEFINED: _ClassVar[ModelTestType]
    MODEL_TEST_TYPE_PERFORMANCE: _ClassVar[ModelTestType]
    MODEL_TEST_TYPE_FAIRNESS: _ClassVar[ModelTestType]
    MODEL_TEST_TYPE_STABILITY: _ClassVar[ModelTestType]
    MODEL_TEST_TYPE_FEATURE_IMPORTANCE: _ClassVar[ModelTestType]
MODEL_TEST_TYPE_UNDEFINED: ModelTestType
MODEL_TEST_TYPE_PERFORMANCE: ModelTestType
MODEL_TEST_TYPE_FAIRNESS: ModelTestType
MODEL_TEST_TYPE_STABILITY: ModelTestType
MODEL_TEST_TYPE_FEATURE_IMPORTANCE: ModelTestType

class TestThreshold(_message.Message):
    __slots__ = ("threshold_type", "value", "value_range", "reference_split_id", "reference_model_id")
    class ThresholdType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNDEFINED: _ClassVar[TestThreshold.ThresholdType]
        ABSOLUTE_SINGLE_VALUE: _ClassVar[TestThreshold.ThresholdType]
        ABSOLUTE_VALUE_RANGE: _ClassVar[TestThreshold.ThresholdType]
        RELATIVE_SINGLE_VALUE: _ClassVar[TestThreshold.ThresholdType]
        RELATIVE_VALUE_RANGE: _ClassVar[TestThreshold.ThresholdType]
    UNDEFINED: TestThreshold.ThresholdType
    ABSOLUTE_SINGLE_VALUE: TestThreshold.ThresholdType
    ABSOLUTE_VALUE_RANGE: TestThreshold.ThresholdType
    RELATIVE_SINGLE_VALUE: TestThreshold.ThresholdType
    RELATIVE_VALUE_RANGE: TestThreshold.ThresholdType
    class ThresholdValueRange(_message.Message):
        __slots__ = ("lower_bound", "upper_bound", "condition")
        class ThresholdCondition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            UNDEFINED: _ClassVar[TestThreshold.ThresholdValueRange.ThresholdCondition]
            WARN_OR_FAIL_IF_OUTSIDE: _ClassVar[TestThreshold.ThresholdValueRange.ThresholdCondition]
            WARN_OR_FAIL_IF_WITHIN: _ClassVar[TestThreshold.ThresholdValueRange.ThresholdCondition]
        UNDEFINED: TestThreshold.ThresholdValueRange.ThresholdCondition
        WARN_OR_FAIL_IF_OUTSIDE: TestThreshold.ThresholdValueRange.ThresholdCondition
        WARN_OR_FAIL_IF_WITHIN: TestThreshold.ThresholdValueRange.ThresholdCondition
        LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
        UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
        CONDITION_FIELD_NUMBER: _ClassVar[int]
        lower_bound: float
        upper_bound: float
        condition: TestThreshold.ThresholdValueRange.ThresholdCondition
        def __init__(self, lower_bound: _Optional[float] = ..., upper_bound: _Optional[float] = ..., condition: _Optional[_Union[TestThreshold.ThresholdValueRange.ThresholdCondition, str]] = ...) -> None: ...
    class ThresholdValue(_message.Message):
        __slots__ = ("value", "condition")
        class ThresholdCondition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            UNDEFINED: _ClassVar[TestThreshold.ThresholdValue.ThresholdCondition]
            WARN_OR_FAIL_IF_LESS_THAN: _ClassVar[TestThreshold.ThresholdValue.ThresholdCondition]
            WARN_OR_FAIL_IF_GREATER_THAN: _ClassVar[TestThreshold.ThresholdValue.ThresholdCondition]
        UNDEFINED: TestThreshold.ThresholdValue.ThresholdCondition
        WARN_OR_FAIL_IF_LESS_THAN: TestThreshold.ThresholdValue.ThresholdCondition
        WARN_OR_FAIL_IF_GREATER_THAN: TestThreshold.ThresholdValue.ThresholdCondition
        VALUE_FIELD_NUMBER: _ClassVar[int]
        CONDITION_FIELD_NUMBER: _ClassVar[int]
        value: float
        condition: TestThreshold.ThresholdValue.ThresholdCondition
        def __init__(self, value: _Optional[float] = ..., condition: _Optional[_Union[TestThreshold.ThresholdValue.ThresholdCondition, str]] = ...) -> None: ...
    THRESHOLD_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    VALUE_RANGE_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    threshold_type: TestThreshold.ThresholdType
    value: TestThreshold.ThresholdValue
    value_range: TestThreshold.ThresholdValueRange
    reference_split_id: str
    reference_model_id: str
    def __init__(self, threshold_type: _Optional[_Union[TestThreshold.ThresholdType, str]] = ..., value: _Optional[_Union[TestThreshold.ThresholdValue, _Mapping]] = ..., value_range: _Optional[_Union[TestThreshold.ThresholdValueRange, _Mapping]] = ..., reference_split_id: _Optional[str] = ..., reference_model_id: _Optional[str] = ...) -> None: ...

class PerformanceTest(_message.Message):
    __slots__ = ("performance_metric_and_threshold",)
    class PerformanceMetricAndThreshold(_message.Message):
        __slots__ = ("accuracy_type", "threshold_warning", "threshold_fail")
        ACCURACY_TYPE_FIELD_NUMBER: _ClassVar[int]
        THRESHOLD_WARNING_FIELD_NUMBER: _ClassVar[int]
        THRESHOLD_FAIL_FIELD_NUMBER: _ClassVar[int]
        accuracy_type: _accuracy_pb2.AccuracyType.Type
        threshold_warning: TestThreshold
        threshold_fail: TestThreshold
        def __init__(self, accuracy_type: _Optional[_Union[_accuracy_pb2.AccuracyType.Type, str]] = ..., threshold_warning: _Optional[_Union[TestThreshold, _Mapping]] = ..., threshold_fail: _Optional[_Union[TestThreshold, _Mapping]] = ...) -> None: ...
    PERFORMANCE_METRIC_AND_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    performance_metric_and_threshold: PerformanceTest.PerformanceMetricAndThreshold
    def __init__(self, performance_metric_and_threshold: _Optional[_Union[PerformanceTest.PerformanceMetricAndThreshold, _Mapping]] = ...) -> None: ...

class FairnessTest(_message.Message):
    __slots__ = ("fairness_metric_and_threshold", "segment_id_protected", "protected_segment_name_regex", "segment_id_comparison")
    class FairnessMetricAndThreshold(_message.Message):
        __slots__ = ("bias_type", "threshold_warning", "threshold_fail")
        BIAS_TYPE_FIELD_NUMBER: _ClassVar[int]
        THRESHOLD_WARNING_FIELD_NUMBER: _ClassVar[int]
        THRESHOLD_FAIL_FIELD_NUMBER: _ClassVar[int]
        bias_type: _intelligence_service_pb2.BiasType.Type
        threshold_warning: TestThreshold
        threshold_fail: TestThreshold
        def __init__(self, bias_type: _Optional[_Union[_intelligence_service_pb2.BiasType.Type, str]] = ..., threshold_warning: _Optional[_Union[TestThreshold, _Mapping]] = ..., threshold_fail: _Optional[_Union[TestThreshold, _Mapping]] = ...) -> None: ...
    FAIRNESS_METRIC_AND_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_ID_PROTECTED_FIELD_NUMBER: _ClassVar[int]
    PROTECTED_SEGMENT_NAME_REGEX_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_ID_COMPARISON_FIELD_NUMBER: _ClassVar[int]
    fairness_metric_and_threshold: FairnessTest.FairnessMetricAndThreshold
    segment_id_protected: _segment_pb2.SegmentID
    protected_segment_name_regex: str
    segment_id_comparison: _segment_pb2.SegmentID
    def __init__(self, fairness_metric_and_threshold: _Optional[_Union[FairnessTest.FairnessMetricAndThreshold, _Mapping]] = ..., segment_id_protected: _Optional[_Union[_segment_pb2.SegmentID, _Mapping]] = ..., protected_segment_name_regex: _Optional[str] = ..., segment_id_comparison: _Optional[_Union[_segment_pb2.SegmentID, _Mapping]] = ...) -> None: ...

class StabilityTest(_message.Message):
    __slots__ = ("base_split_id", "base_segment_id", "stability_metric_and_threshold")
    class StabilityMetricAndThreshold(_message.Message):
        __slots__ = ("distance_type", "threshold_warning", "threshold_fail")
        DISTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
        THRESHOLD_WARNING_FIELD_NUMBER: _ClassVar[int]
        THRESHOLD_FAIL_FIELD_NUMBER: _ClassVar[int]
        distance_type: _distance_pb2.DistanceType
        threshold_warning: TestThreshold
        threshold_fail: TestThreshold
        def __init__(self, distance_type: _Optional[_Union[_distance_pb2.DistanceType, str]] = ..., threshold_warning: _Optional[_Union[TestThreshold, _Mapping]] = ..., threshold_fail: _Optional[_Union[TestThreshold, _Mapping]] = ...) -> None: ...
    BASE_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    STABILITY_METRIC_AND_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    base_split_id: str
    base_segment_id: _segment_pb2.SegmentID
    stability_metric_and_threshold: StabilityTest.StabilityMetricAndThreshold
    def __init__(self, base_split_id: _Optional[str] = ..., base_segment_id: _Optional[_Union[_segment_pb2.SegmentID, _Mapping]] = ..., stability_metric_and_threshold: _Optional[_Union[StabilityTest.StabilityMetricAndThreshold, _Mapping]] = ...) -> None: ...

class FeatureImportanceTest(_message.Message):
    __slots__ = ("background_split_id", "options_and_threshold")
    class FeatureImportanceOptionsAndThreshold(_message.Message):
        __slots__ = ("qoi", "min_importance_value", "threshold_warning", "threshold_fail")
        QOI_FIELD_NUMBER: _ClassVar[int]
        MIN_IMPORTANCE_VALUE_FIELD_NUMBER: _ClassVar[int]
        THRESHOLD_WARNING_FIELD_NUMBER: _ClassVar[int]
        THRESHOLD_FAIL_FIELD_NUMBER: _ClassVar[int]
        qoi: _qoi_pb2.QuantityOfInterest
        min_importance_value: float
        threshold_warning: TestThreshold
        threshold_fail: TestThreshold
        def __init__(self, qoi: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., min_importance_value: _Optional[float] = ..., threshold_warning: _Optional[_Union[TestThreshold, _Mapping]] = ..., threshold_fail: _Optional[_Union[TestThreshold, _Mapping]] = ...) -> None: ...
    BACKGROUND_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_AND_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    background_split_id: str
    options_and_threshold: FeatureImportanceTest.FeatureImportanceOptionsAndThreshold
    def __init__(self, background_split_id: _Optional[str] = ..., options_and_threshold: _Optional[_Union[FeatureImportanceTest.FeatureImportanceOptionsAndThreshold, _Mapping]] = ...) -> None: ...

class ModelTest(_message.Message):
    __slots__ = ("id", "project_id", "data_collection_id", "data_collection_name_regex", "split_id", "split_name_regex", "segment_id", "test_type", "autorun", "performance_test", "fairness_test", "stability_test", "feature_importance_test", "test_name", "description", "test_group_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_REGEX_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_NAME_REGEX_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_TYPE_FIELD_NUMBER: _ClassVar[int]
    AUTORUN_FIELD_NUMBER: _ClassVar[int]
    PERFORMANCE_TEST_FIELD_NUMBER: _ClassVar[int]
    FAIRNESS_TEST_FIELD_NUMBER: _ClassVar[int]
    STABILITY_TEST_FIELD_NUMBER: _ClassVar[int]
    FEATURE_IMPORTANCE_TEST_FIELD_NUMBER: _ClassVar[int]
    TEST_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TEST_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    data_collection_id: str
    data_collection_name_regex: str
    split_id: str
    split_name_regex: str
    segment_id: _segment_pb2.SegmentID
    test_type: ModelTestType
    autorun: bool
    performance_test: PerformanceTest
    fairness_test: FairnessTest
    stability_test: StabilityTest
    feature_importance_test: FeatureImportanceTest
    test_name: str
    description: str
    test_group_id: str
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., data_collection_name_regex: _Optional[str] = ..., split_id: _Optional[str] = ..., split_name_regex: _Optional[str] = ..., segment_id: _Optional[_Union[_segment_pb2.SegmentID, _Mapping]] = ..., test_type: _Optional[_Union[ModelTestType, str]] = ..., autorun: bool = ..., performance_test: _Optional[_Union[PerformanceTest, _Mapping]] = ..., fairness_test: _Optional[_Union[FairnessTest, _Mapping]] = ..., stability_test: _Optional[_Union[StabilityTest, _Mapping]] = ..., feature_importance_test: _Optional[_Union[FeatureImportanceTest, _Mapping]] = ..., test_name: _Optional[str] = ..., description: _Optional[str] = ..., test_group_id: _Optional[str] = ...) -> None: ...
