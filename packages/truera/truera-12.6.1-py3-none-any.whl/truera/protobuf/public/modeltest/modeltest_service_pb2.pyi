from google.api import annotations_pb2 as _annotations_pb2
from truera.protobuf.public.aiq import intelligence_service_pb2 as _intelligence_service_pb2
from truera.protobuf.public.data import segment_pb2 as _segment_pb2
from truera.protobuf.public import metadata_message_types_pb2 as _metadata_message_types_pb2
from truera.protobuf.public.modeltest import modeltest_pb2 as _modeltest_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestResultType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNDEFINED: _ClassVar[TestResultType]
    VALUE: _ClassVar[TestResultType]
    PREDICTION_UNAVAILABLE: _ClassVar[TestResultType]
    INFLUENCE_UNAVAILABLE: _ClassVar[TestResultType]
    OTHER_EXCEPTION: _ClassVar[TestResultType]

class ThresholdResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THRESHOLD_RESULT_UNDEFINED: _ClassVar[ThresholdResult]
    THRESHOLD_RESULT_PASS: _ClassVar[ThresholdResult]
    THRESHOLD_RESULT_FAIL: _ClassVar[ThresholdResult]
UNDEFINED: TestResultType
VALUE: TestResultType
PREDICTION_UNAVAILABLE: TestResultType
INFLUENCE_UNAVAILABLE: TestResultType
OTHER_EXCEPTION: TestResultType
THRESHOLD_RESULT_UNDEFINED: ThresholdResult
THRESHOLD_RESULT_PASS: ThresholdResult
THRESHOLD_RESULT_FAIL: ThresholdResult

class CreateTestsFromSplitRequest(_message.Message):
    __slots__ = ("project_id", "split_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    split_id: str
    def __init__(self, project_id: _Optional[str] = ..., split_id: _Optional[str] = ...) -> None: ...

class CreateTestsFromSplitResponse(_message.Message):
    __slots__ = ("model_tests",)
    MODEL_TESTS_FIELD_NUMBER: _ClassVar[int]
    model_tests: _containers.RepeatedCompositeFieldContainer[_modeltest_pb2.ModelTest]
    def __init__(self, model_tests: _Optional[_Iterable[_Union[_modeltest_pb2.ModelTest, _Mapping]]] = ...) -> None: ...

class StartBaselineModelWorkflowRequest(_message.Message):
    __slots__ = ("project_id", "project_name", "data_collection_id", "data_collection_name", "split_id", "split_name", "output_type")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    project_name: str
    data_collection_id: str
    data_collection_name: str
    split_id: str
    split_name: str
    output_type: str
    def __init__(self, project_id: _Optional[str] = ..., project_name: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., split_id: _Optional[str] = ..., split_name: _Optional[str] = ..., output_type: _Optional[str] = ...) -> None: ...

class StartBaselineModelWorkflowResponse(_message.Message):
    __slots__ = ("workflow_id",)
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    workflow_id: str
    def __init__(self, workflow_id: _Optional[str] = ...) -> None: ...

class CreatePerformanceTestRequest(_message.Message):
    __slots__ = ("project_id", "split_id", "segment_id", "test_definition", "autorun", "overwrite", "test_name", "description")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    AUTORUN_FIELD_NUMBER: _ClassVar[int]
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    TEST_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    split_id: str
    segment_id: _segment_pb2.SegmentID
    test_definition: _modeltest_pb2.PerformanceTest
    autorun: bool
    overwrite: bool
    test_name: str
    description: str
    def __init__(self, project_id: _Optional[str] = ..., split_id: _Optional[str] = ..., segment_id: _Optional[_Union[_segment_pb2.SegmentID, _Mapping]] = ..., test_definition: _Optional[_Union[_modeltest_pb2.PerformanceTest, _Mapping]] = ..., autorun: bool = ..., overwrite: bool = ..., test_name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreatePerformanceTestResponse(_message.Message):
    __slots__ = ("test_id", "test_group_id")
    TEST_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    test_id: str
    test_group_id: str
    def __init__(self, test_id: _Optional[str] = ..., test_group_id: _Optional[str] = ...) -> None: ...

class CreateFairnessTestRequest(_message.Message):
    __slots__ = ("project_id", "split_id", "segment_id", "test_definition", "autorun", "overwrite", "test_name", "description")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    AUTORUN_FIELD_NUMBER: _ClassVar[int]
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    TEST_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    split_id: str
    segment_id: _segment_pb2.SegmentID
    test_definition: _modeltest_pb2.FairnessTest
    autorun: bool
    overwrite: bool
    test_name: str
    description: str
    def __init__(self, project_id: _Optional[str] = ..., split_id: _Optional[str] = ..., segment_id: _Optional[_Union[_segment_pb2.SegmentID, _Mapping]] = ..., test_definition: _Optional[_Union[_modeltest_pb2.FairnessTest, _Mapping]] = ..., autorun: bool = ..., overwrite: bool = ..., test_name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateFairnessTestResponse(_message.Message):
    __slots__ = ("test_id", "test_group_id")
    TEST_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    test_id: str
    test_group_id: str
    def __init__(self, test_id: _Optional[str] = ..., test_group_id: _Optional[str] = ...) -> None: ...

class CreateStabilityTestRequest(_message.Message):
    __slots__ = ("project_id", "split_id", "segment_id", "test_definition", "autorun", "overwrite", "test_name", "description")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    AUTORUN_FIELD_NUMBER: _ClassVar[int]
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    TEST_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    split_id: str
    segment_id: _segment_pb2.SegmentID
    test_definition: _modeltest_pb2.StabilityTest
    autorun: bool
    overwrite: bool
    test_name: str
    description: str
    def __init__(self, project_id: _Optional[str] = ..., split_id: _Optional[str] = ..., segment_id: _Optional[_Union[_segment_pb2.SegmentID, _Mapping]] = ..., test_definition: _Optional[_Union[_modeltest_pb2.StabilityTest, _Mapping]] = ..., autorun: bool = ..., overwrite: bool = ..., test_name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateStabilityTestResponse(_message.Message):
    __slots__ = ("test_id", "test_group_id")
    TEST_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    test_id: str
    test_group_id: str
    def __init__(self, test_id: _Optional[str] = ..., test_group_id: _Optional[str] = ...) -> None: ...

class CreateFeatureImportanceTestRequest(_message.Message):
    __slots__ = ("project_id", "split_id", "segment_id", "test_definition", "autorun", "overwrite", "test_name", "description")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    AUTORUN_FIELD_NUMBER: _ClassVar[int]
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    TEST_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    split_id: str
    segment_id: _segment_pb2.SegmentID
    test_definition: _modeltest_pb2.FeatureImportanceTest
    autorun: bool
    overwrite: bool
    test_name: str
    description: str
    def __init__(self, project_id: _Optional[str] = ..., split_id: _Optional[str] = ..., segment_id: _Optional[_Union[_segment_pb2.SegmentID, _Mapping]] = ..., test_definition: _Optional[_Union[_modeltest_pb2.FeatureImportanceTest, _Mapping]] = ..., autorun: bool = ..., overwrite: bool = ..., test_name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateFeatureImportanceTestResponse(_message.Message):
    __slots__ = ("test_id", "test_group_id")
    TEST_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    test_id: str
    test_group_id: str
    def __init__(self, test_id: _Optional[str] = ..., test_group_id: _Optional[str] = ...) -> None: ...

class DeleteModelTestRequest(_message.Message):
    __slots__ = ("project_id", "test_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    test_id: str
    def __init__(self, project_id: _Optional[str] = ..., test_id: _Optional[str] = ...) -> None: ...

class DeleteModelTestResponse(_message.Message):
    __slots__ = ("deleted_test",)
    DELETED_TEST_FIELD_NUMBER: _ClassVar[int]
    deleted_test: _modeltest_pb2.ModelTest
    def __init__(self, deleted_test: _Optional[_Union[_modeltest_pb2.ModelTest, _Mapping]] = ...) -> None: ...

class DeleteModelTestGroupRequest(_message.Message):
    __slots__ = ("project_id", "test_group_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    test_group_id: str
    def __init__(self, project_id: _Optional[str] = ..., test_group_id: _Optional[str] = ...) -> None: ...

class DeleteModelTestGroupResponse(_message.Message):
    __slots__ = ("deleted_test_ids",)
    DELETED_TEST_IDS_FIELD_NUMBER: _ClassVar[int]
    deleted_test_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, deleted_test_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteModelTestsForSplitRequest(_message.Message):
    __slots__ = ("project_id", "split_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    split_id: str
    def __init__(self, project_id: _Optional[str] = ..., split_id: _Optional[str] = ...) -> None: ...

class DeleteModelTestsForSplitResponse(_message.Message):
    __slots__ = ("deleted_tests",)
    DELETED_TESTS_FIELD_NUMBER: _ClassVar[int]
    deleted_tests: _containers.RepeatedCompositeFieldContainer[_modeltest_pb2.ModelTest]
    def __init__(self, deleted_tests: _Optional[_Iterable[_Union[_modeltest_pb2.ModelTest, _Mapping]]] = ...) -> None: ...

class GetModelTestsRequest(_message.Message):
    __slots__ = ("project_id", "test_type", "data_collection_id", "split_id", "test_id", "test_name")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_NAME_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    test_type: _modeltest_pb2.ModelTestType
    data_collection_id: str
    split_id: str
    test_id: str
    test_name: str
    def __init__(self, project_id: _Optional[str] = ..., test_type: _Optional[_Union[_modeltest_pb2.ModelTestType, str]] = ..., data_collection_id: _Optional[str] = ..., split_id: _Optional[str] = ..., test_id: _Optional[str] = ..., test_name: _Optional[str] = ...) -> None: ...

class GetModelTestsResponse(_message.Message):
    __slots__ = ("model_tests",)
    MODEL_TESTS_FIELD_NUMBER: _ClassVar[int]
    model_tests: _containers.RepeatedCompositeFieldContainer[_modeltest_pb2.ModelTest]
    def __init__(self, model_tests: _Optional[_Iterable[_Union[_modeltest_pb2.ModelTest, _Mapping]]] = ...) -> None: ...

class GetModelTestGroupsRequest(_message.Message):
    __slots__ = ("project_id", "test_type", "data_collection_id", "split_id", "test_group_id", "test_name")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_NAME_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    test_type: _modeltest_pb2.ModelTestType
    data_collection_id: str
    split_id: str
    test_group_id: str
    test_name: str
    def __init__(self, project_id: _Optional[str] = ..., test_type: _Optional[_Union[_modeltest_pb2.ModelTestType, str]] = ..., data_collection_id: _Optional[str] = ..., split_id: _Optional[str] = ..., test_group_id: _Optional[str] = ..., test_name: _Optional[str] = ...) -> None: ...

class GetModelTestGroupsResponse(_message.Message):
    __slots__ = ("model_test_groups",)
    MODEL_TEST_GROUPS_FIELD_NUMBER: _ClassVar[int]
    model_test_groups: _containers.RepeatedCompositeFieldContainer[ModelTestGroup]
    def __init__(self, model_test_groups: _Optional[_Iterable[_Union[ModelTestGroup, _Mapping]]] = ...) -> None: ...

class GetTestResultsForModelRequest(_message.Message):
    __slots__ = ("project_id", "model_id", "test_type", "split_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_TYPE_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_id: str
    test_type: _modeltest_pb2.ModelTestType
    split_id: str
    def __init__(self, project_id: _Optional[str] = ..., model_id: _Optional[str] = ..., test_type: _Optional[_Union[_modeltest_pb2.ModelTestType, str]] = ..., split_id: _Optional[str] = ...) -> None: ...

class GetTestResultsForModelResponse(_message.Message):
    __slots__ = ("performance_test_results", "fairness_test_results", "stability_test_results", "pending_operations", "pending_test_results", "feature_importance_test_results")
    PERFORMANCE_TEST_RESULTS_FIELD_NUMBER: _ClassVar[int]
    FAIRNESS_TEST_RESULTS_FIELD_NUMBER: _ClassVar[int]
    STABILITY_TEST_RESULTS_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    PENDING_TEST_RESULTS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_IMPORTANCE_TEST_RESULTS_FIELD_NUMBER: _ClassVar[int]
    performance_test_results: _containers.RepeatedCompositeFieldContainer[PerformanceTestResult]
    fairness_test_results: _containers.RepeatedCompositeFieldContainer[FairnessTestResult]
    stability_test_results: _containers.RepeatedCompositeFieldContainer[StabilityTestResult]
    pending_operations: _intelligence_service_pb2.PendingOperations
    pending_test_results: PendingModelTestResults
    feature_importance_test_results: _containers.RepeatedCompositeFieldContainer[FeatureImportanceTestResult]
    def __init__(self, performance_test_results: _Optional[_Iterable[_Union[PerformanceTestResult, _Mapping]]] = ..., fairness_test_results: _Optional[_Iterable[_Union[FairnessTestResult, _Mapping]]] = ..., stability_test_results: _Optional[_Iterable[_Union[StabilityTestResult, _Mapping]]] = ..., pending_operations: _Optional[_Union[_intelligence_service_pb2.PendingOperations, _Mapping]] = ..., pending_test_results: _Optional[_Union[PendingModelTestResults, _Mapping]] = ..., feature_importance_test_results: _Optional[_Iterable[_Union[FeatureImportanceTestResult, _Mapping]]] = ...) -> None: ...

class PendingModelTestResults(_message.Message):
    __slots__ = ("pending_test_ids",)
    PENDING_TEST_IDS_FIELD_NUMBER: _ClassVar[int]
    pending_test_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, pending_test_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class PerformanceTestResult(_message.Message):
    __slots__ = ("test_details", "metric_result", "warning_result", "pass_fail_result", "result_type", "error_message")
    TEST_DETAILS_FIELD_NUMBER: _ClassVar[int]
    METRIC_RESULT_FIELD_NUMBER: _ClassVar[int]
    WARNING_RESULT_FIELD_NUMBER: _ClassVar[int]
    PASS_FAIL_RESULT_FIELD_NUMBER: _ClassVar[int]
    RESULT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    test_details: _modeltest_pb2.ModelTest
    metric_result: float
    warning_result: ThresholdResult
    pass_fail_result: ThresholdResult
    result_type: TestResultType
    error_message: str
    def __init__(self, test_details: _Optional[_Union[_modeltest_pb2.ModelTest, _Mapping]] = ..., metric_result: _Optional[float] = ..., warning_result: _Optional[_Union[ThresholdResult, str]] = ..., pass_fail_result: _Optional[_Union[ThresholdResult, str]] = ..., result_type: _Optional[_Union[TestResultType, str]] = ..., error_message: _Optional[str] = ...) -> None: ...

class FairnessTestResult(_message.Message):
    __slots__ = ("test_details", "metric_result", "warning_result", "pass_fail_result", "result_type", "error_message")
    TEST_DETAILS_FIELD_NUMBER: _ClassVar[int]
    METRIC_RESULT_FIELD_NUMBER: _ClassVar[int]
    WARNING_RESULT_FIELD_NUMBER: _ClassVar[int]
    PASS_FAIL_RESULT_FIELD_NUMBER: _ClassVar[int]
    RESULT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    test_details: _modeltest_pb2.ModelTest
    metric_result: float
    warning_result: ThresholdResult
    pass_fail_result: ThresholdResult
    result_type: TestResultType
    error_message: str
    def __init__(self, test_details: _Optional[_Union[_modeltest_pb2.ModelTest, _Mapping]] = ..., metric_result: _Optional[float] = ..., warning_result: _Optional[_Union[ThresholdResult, str]] = ..., pass_fail_result: _Optional[_Union[ThresholdResult, str]] = ..., result_type: _Optional[_Union[TestResultType, str]] = ..., error_message: _Optional[str] = ...) -> None: ...

class StabilityTestResult(_message.Message):
    __slots__ = ("test_details", "metric_result", "warning_result", "pass_fail_result", "result_type", "error_message")
    TEST_DETAILS_FIELD_NUMBER: _ClassVar[int]
    METRIC_RESULT_FIELD_NUMBER: _ClassVar[int]
    WARNING_RESULT_FIELD_NUMBER: _ClassVar[int]
    PASS_FAIL_RESULT_FIELD_NUMBER: _ClassVar[int]
    RESULT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    test_details: _modeltest_pb2.ModelTest
    metric_result: float
    warning_result: ThresholdResult
    pass_fail_result: ThresholdResult
    result_type: TestResultType
    error_message: str
    def __init__(self, test_details: _Optional[_Union[_modeltest_pb2.ModelTest, _Mapping]] = ..., metric_result: _Optional[float] = ..., warning_result: _Optional[_Union[ThresholdResult, str]] = ..., pass_fail_result: _Optional[_Union[ThresholdResult, str]] = ..., result_type: _Optional[_Union[TestResultType, str]] = ..., error_message: _Optional[str] = ...) -> None: ...

class FeatureImportanceTestResult(_message.Message):
    __slots__ = ("test_details", "num_features_below_importance_threshold", "warning_result", "pass_fail_result", "result_type", "error_message")
    TEST_DETAILS_FIELD_NUMBER: _ClassVar[int]
    NUM_FEATURES_BELOW_IMPORTANCE_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    WARNING_RESULT_FIELD_NUMBER: _ClassVar[int]
    PASS_FAIL_RESULT_FIELD_NUMBER: _ClassVar[int]
    RESULT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    test_details: _modeltest_pb2.ModelTest
    num_features_below_importance_threshold: int
    warning_result: ThresholdResult
    pass_fail_result: ThresholdResult
    result_type: TestResultType
    error_message: str
    def __init__(self, test_details: _Optional[_Union[_modeltest_pb2.ModelTest, _Mapping]] = ..., num_features_below_importance_threshold: _Optional[int] = ..., warning_result: _Optional[_Union[ThresholdResult, str]] = ..., pass_fail_result: _Optional[_Union[ThresholdResult, str]] = ..., result_type: _Optional[_Union[TestResultType, str]] = ..., error_message: _Optional[str] = ...) -> None: ...

class CreatePerformanceTestGroupRequest(_message.Message):
    __slots__ = ("model_test_group",)
    MODEL_TEST_GROUP_FIELD_NUMBER: _ClassVar[int]
    model_test_group: ModelTestGroup
    def __init__(self, model_test_group: _Optional[_Union[ModelTestGroup, _Mapping]] = ...) -> None: ...

class CreatePerformanceTestGroupResponse(_message.Message):
    __slots__ = ("test_group_id", "test_ids")
    TEST_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_IDS_FIELD_NUMBER: _ClassVar[int]
    test_group_id: str
    test_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, test_group_id: _Optional[str] = ..., test_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateFairnessTestGroupRequest(_message.Message):
    __slots__ = ("model_test_group",)
    MODEL_TEST_GROUP_FIELD_NUMBER: _ClassVar[int]
    model_test_group: ModelTestGroup
    def __init__(self, model_test_group: _Optional[_Union[ModelTestGroup, _Mapping]] = ...) -> None: ...

class CreateFairnessTestGroupResponse(_message.Message):
    __slots__ = ("test_group_id", "test_ids")
    TEST_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_IDS_FIELD_NUMBER: _ClassVar[int]
    test_group_id: str
    test_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, test_group_id: _Optional[str] = ..., test_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateStabilityTestGroupRequest(_message.Message):
    __slots__ = ("model_test_group",)
    MODEL_TEST_GROUP_FIELD_NUMBER: _ClassVar[int]
    model_test_group: ModelTestGroup
    def __init__(self, model_test_group: _Optional[_Union[ModelTestGroup, _Mapping]] = ...) -> None: ...

class CreateStabilityTestGroupResponse(_message.Message):
    __slots__ = ("test_group_id", "test_ids")
    TEST_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_IDS_FIELD_NUMBER: _ClassVar[int]
    test_group_id: str
    test_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, test_group_id: _Optional[str] = ..., test_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateFeatureImportanceTestGroupRequest(_message.Message):
    __slots__ = ("model_test_group",)
    MODEL_TEST_GROUP_FIELD_NUMBER: _ClassVar[int]
    model_test_group: ModelTestGroup
    def __init__(self, model_test_group: _Optional[_Union[ModelTestGroup, _Mapping]] = ...) -> None: ...

class CreateFeatureImportanceTestGroupResponse(_message.Message):
    __slots__ = ("test_group_id", "test_ids")
    TEST_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_IDS_FIELD_NUMBER: _ClassVar[int]
    test_group_id: str
    test_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, test_group_id: _Optional[str] = ..., test_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ModelTestGroup(_message.Message):
    __slots__ = ("project_id", "split_ids", "test_group_id", "test_name", "description", "segment_ids", "protected_segment_ids", "comparison_segment_ids", "performance_test", "fairness_test", "stability_test", "feature_importance_test", "data_collection_name_regex", "data_collection_ids", "split_name_regex", "data_collection_id_to_base_split_id")
    class DataCollectionIdToBaseSplitIdEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_IDS_FIELD_NUMBER: _ClassVar[int]
    TEST_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    PROTECTED_SEGMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    COMPARISON_SEGMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    PERFORMANCE_TEST_FIELD_NUMBER: _ClassVar[int]
    FAIRNESS_TEST_FIELD_NUMBER: _ClassVar[int]
    STABILITY_TEST_FIELD_NUMBER: _ClassVar[int]
    FEATURE_IMPORTANCE_TEST_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_REGEX_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_IDS_FIELD_NUMBER: _ClassVar[int]
    SPLIT_NAME_REGEX_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_TO_BASE_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    split_ids: _containers.RepeatedScalarFieldContainer[str]
    test_group_id: str
    test_name: str
    description: str
    segment_ids: _containers.RepeatedCompositeFieldContainer[_segment_pb2.SegmentID]
    protected_segment_ids: _containers.RepeatedCompositeFieldContainer[_segment_pb2.SegmentID]
    comparison_segment_ids: _containers.RepeatedCompositeFieldContainer[_segment_pb2.SegmentID]
    performance_test: _modeltest_pb2.PerformanceTest
    fairness_test: _modeltest_pb2.FairnessTest
    stability_test: _modeltest_pb2.StabilityTest
    feature_importance_test: _modeltest_pb2.FeatureImportanceTest
    data_collection_name_regex: str
    data_collection_ids: _containers.RepeatedScalarFieldContainer[str]
    split_name_regex: str
    data_collection_id_to_base_split_id: _containers.ScalarMap[str, str]
    def __init__(self, project_id: _Optional[str] = ..., split_ids: _Optional[_Iterable[str]] = ..., test_group_id: _Optional[str] = ..., test_name: _Optional[str] = ..., description: _Optional[str] = ..., segment_ids: _Optional[_Iterable[_Union[_segment_pb2.SegmentID, _Mapping]]] = ..., protected_segment_ids: _Optional[_Iterable[_Union[_segment_pb2.SegmentID, _Mapping]]] = ..., comparison_segment_ids: _Optional[_Iterable[_Union[_segment_pb2.SegmentID, _Mapping]]] = ..., performance_test: _Optional[_Union[_modeltest_pb2.PerformanceTest, _Mapping]] = ..., fairness_test: _Optional[_Union[_modeltest_pb2.FairnessTest, _Mapping]] = ..., stability_test: _Optional[_Union[_modeltest_pb2.StabilityTest, _Mapping]] = ..., feature_importance_test: _Optional[_Union[_modeltest_pb2.FeatureImportanceTest, _Mapping]] = ..., data_collection_name_regex: _Optional[str] = ..., data_collection_ids: _Optional[_Iterable[str]] = ..., split_name_regex: _Optional[str] = ..., data_collection_id_to_base_split_id: _Optional[_Mapping[str, str]] = ...) -> None: ...

class GetDataSplitsFromRegexRequest(_message.Message):
    __slots__ = ("project_id", "split_name_regex", "data_collection_ids", "data_collection_name_regex")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_NAME_REGEX_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_IDS_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_REGEX_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    split_name_regex: str
    data_collection_ids: _containers.RepeatedScalarFieldContainer[str]
    data_collection_name_regex: str
    def __init__(self, project_id: _Optional[str] = ..., split_name_regex: _Optional[str] = ..., data_collection_ids: _Optional[_Iterable[str]] = ..., data_collection_name_regex: _Optional[str] = ...) -> None: ...

class GetDataSplitsFromRegexResponse(_message.Message):
    __slots__ = ("splits_metadata",)
    SPLITS_METADATA_FIELD_NUMBER: _ClassVar[int]
    splits_metadata: _containers.RepeatedCompositeFieldContainer[_metadata_message_types_pb2.DataSplitMetadata]
    def __init__(self, splits_metadata: _Optional[_Iterable[_Union[_metadata_message_types_pb2.DataSplitMetadata, _Mapping]]] = ...) -> None: ...
