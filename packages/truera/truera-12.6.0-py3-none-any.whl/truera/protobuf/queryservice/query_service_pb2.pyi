from google.api import annotations_pb2 as _annotations_pb2
from truera.protobuf.public import common_pb2 as _common_pb2
from truera.protobuf.public.common import data_kind_pb2 as _data_kind_pb2
from truera.protobuf.public.common import row_pb2 as _row_pb2
from truera.protobuf.public.data import filter_pb2 as _filter_pb2
from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from truera.protobuf.public.aiq import accuracy_pb2 as _accuracy_pb2
from truera.protobuf.public.aiq import distance_pb2 as _distance_pb2
from truera.protobuf.public.aiq import intelligence_service_pb2 as _intelligence_service_pb2
from truera.protobuf.public.read_optimized_table_service import read_optimized_table_messages_pb2 as _read_optimized_table_messages_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNDEFINED: _ClassVar[ValueType]
    BYTE: _ClassVar[ValueType]
    INT16: _ClassVar[ValueType]
    INT32: _ClassVar[ValueType]
    INT64: _ClassVar[ValueType]
    FLOAT: _ClassVar[ValueType]
    DOUBLE: _ClassVar[ValueType]
    STRING: _ClassVar[ValueType]
    BOOLEAN: _ClassVar[ValueType]
    TIMESTAMP: _ClassVar[ValueType]
    NULL: _ClassVar[ValueType]

class AccuracyErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NONE: _ClassVar[AccuracyErrorCode]
    PREDICTIONS_UNAVAILABLE: _ClassVar[AccuracyErrorCode]
    GROUND_TRUTH_UNAVAILABLE: _ClassVar[AccuracyErrorCode]
UNDEFINED: ValueType
BYTE: ValueType
INT16: ValueType
INT32: ValueType
INT64: ValueType
FLOAT: ValueType
DOUBLE: ValueType
STRING: ValueType
BOOLEAN: ValueType
TIMESTAMP: ValueType
NULL: ValueType
NONE: AccuracyErrorCode
PREDICTIONS_UNAVAILABLE: AccuracyErrorCode
GROUND_TRUTH_UNAVAILABLE: AccuracyErrorCode

class QueryRequest(_message.Message):
    __slots__ = ("id", "project_id", "sql_query", "raw_data_request", "prediction_request", "feature_influence_request", "filter_data_request", "model_comparison_request", "model_bias_request", "bucketized_stats_request", "drift_request", "isp_request", "feedback_threshold_request", "return_rot_metadata_only")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SQL_QUERY_FIELD_NUMBER: _ClassVar[int]
    RAW_DATA_REQUEST_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_REQUEST_FIELD_NUMBER: _ClassVar[int]
    FEATURE_INFLUENCE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    FILTER_DATA_REQUEST_FIELD_NUMBER: _ClassVar[int]
    MODEL_COMPARISON_REQUEST_FIELD_NUMBER: _ClassVar[int]
    MODEL_BIAS_REQUEST_FIELD_NUMBER: _ClassVar[int]
    BUCKETIZED_STATS_REQUEST_FIELD_NUMBER: _ClassVar[int]
    DRIFT_REQUEST_FIELD_NUMBER: _ClassVar[int]
    ISP_REQUEST_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_THRESHOLD_REQUEST_FIELD_NUMBER: _ClassVar[int]
    RETURN_ROT_METADATA_ONLY_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    sql_query: SQLQueryRequest
    raw_data_request: RawDataRequest
    prediction_request: PredictionRequest
    feature_influence_request: FeatureInfluenceRequest
    filter_data_request: FilterDataRequest
    model_comparison_request: ModelComparisonRequest
    model_bias_request: ModelBiasRequest
    bucketized_stats_request: BucketizedStatsRequest
    drift_request: DriftRequest
    isp_request: ISPRequest
    feedback_threshold_request: FeedbackThresholdsRequest
    return_rot_metadata_only: bool
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ..., sql_query: _Optional[_Union[SQLQueryRequest, _Mapping]] = ..., raw_data_request: _Optional[_Union[RawDataRequest, _Mapping]] = ..., prediction_request: _Optional[_Union[PredictionRequest, _Mapping]] = ..., feature_influence_request: _Optional[_Union[FeatureInfluenceRequest, _Mapping]] = ..., filter_data_request: _Optional[_Union[FilterDataRequest, _Mapping]] = ..., model_comparison_request: _Optional[_Union[ModelComparisonRequest, _Mapping]] = ..., model_bias_request: _Optional[_Union[ModelBiasRequest, _Mapping]] = ..., bucketized_stats_request: _Optional[_Union[BucketizedStatsRequest, _Mapping]] = ..., drift_request: _Optional[_Union[DriftRequest, _Mapping]] = ..., isp_request: _Optional[_Union[ISPRequest, _Mapping]] = ..., feedback_threshold_request: _Optional[_Union[FeedbackThresholdsRequest, _Mapping]] = ..., return_rot_metadata_only: bool = ...) -> None: ...

class SQLQueryRequest(_message.Message):
    __slots__ = ("sql", "should_parse")
    SQL_FIELD_NUMBER: _ClassVar[int]
    SHOULD_PARSE_FIELD_NUMBER: _ClassVar[int]
    sql: str
    should_parse: bool
    def __init__(self, sql: _Optional[str] = ..., should_parse: bool = ...) -> None: ...

class RawDataRequest(_message.Message):
    __slots__ = ("data_kind", "data_collection_id", "query_spec")
    DATA_KIND_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_SPEC_FIELD_NUMBER: _ClassVar[int]
    data_kind: _data_kind_pb2.DataKindDescribed
    data_collection_id: str
    query_spec: QuerySpec
    def __init__(self, data_kind: _Optional[_Union[_data_kind_pb2.DataKindDescribed, str]] = ..., data_collection_id: _Optional[str] = ..., query_spec: _Optional[_Union[QuerySpec, _Mapping]] = ...) -> None: ...

class PredictionRequest(_message.Message):
    __slots__ = ("model_id", "qoi", "query_spec", "classification_threshold", "threshold_context")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    QOI_FIELD_NUMBER: _ClassVar[int]
    QUERY_SPEC_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    qoi: _qoi_pb2.QuantityOfInterest
    query_spec: QuerySpec
    classification_threshold: float
    threshold_context: ClassificationThresholdContext
    def __init__(self, model_id: _Optional[str] = ..., qoi: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., query_spec: _Optional[_Union[QuerySpec, _Mapping]] = ..., classification_threshold: _Optional[float] = ..., threshold_context: _Optional[_Union[ClassificationThresholdContext, _Mapping]] = ...) -> None: ...

class FeatureInfluenceRequest(_message.Message):
    __slots__ = ("model_id", "query_spec", "options")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_SPEC_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    query_spec: QuerySpec
    options: _common_pb2.FeatureInfluenceOptions
    def __init__(self, model_id: _Optional[str] = ..., query_spec: _Optional[_Union[QuerySpec, _Mapping]] = ..., options: _Optional[_Union[_common_pb2.FeatureInfluenceOptions, _Mapping]] = ...) -> None: ...

class FilterDataRequest(_message.Message):
    __slots__ = ("data_collection_id", "query_spec")
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_SPEC_FIELD_NUMBER: _ClassVar[int]
    data_collection_id: str
    query_spec: QuerySpec
    def __init__(self, data_collection_id: _Optional[str] = ..., query_spec: _Optional[_Union[QuerySpec, _Mapping]] = ...) -> None: ...

class ModelComparisonRequest(_message.Message):
    __slots__ = ("comparison_specs",)
    class PredictionSpec(_message.Message):
        __slots__ = ("model_id", "quantity_of_interest", "query_spec", "fi_options")
        MODEL_ID_FIELD_NUMBER: _ClassVar[int]
        QUANTITY_OF_INTEREST_FIELD_NUMBER: _ClassVar[int]
        QUERY_SPEC_FIELD_NUMBER: _ClassVar[int]
        FI_OPTIONS_FIELD_NUMBER: _ClassVar[int]
        model_id: str
        quantity_of_interest: _qoi_pb2.QuantityOfInterest
        query_spec: QuerySpec
        fi_options: _common_pb2.FeatureInfluenceOptions
        def __init__(self, model_id: _Optional[str] = ..., quantity_of_interest: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., query_spec: _Optional[_Union[QuerySpec, _Mapping]] = ..., fi_options: _Optional[_Union[_common_pb2.FeatureInfluenceOptions, _Mapping]] = ...) -> None: ...
    class ModelComparisonSpec(_message.Message):
        __slots__ = ("distance_type", "prediction_spec_1", "prediction_spec_2", "include_prediction_distance", "include_breakdown_by_feature")
        DISTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
        PREDICTION_SPEC_1_FIELD_NUMBER: _ClassVar[int]
        PREDICTION_SPEC_2_FIELD_NUMBER: _ClassVar[int]
        INCLUDE_PREDICTION_DISTANCE_FIELD_NUMBER: _ClassVar[int]
        INCLUDE_BREAKDOWN_BY_FEATURE_FIELD_NUMBER: _ClassVar[int]
        distance_type: _distance_pb2.DistanceType
        prediction_spec_1: ModelComparisonRequest.PredictionSpec
        prediction_spec_2: ModelComparisonRequest.PredictionSpec
        include_prediction_distance: bool
        include_breakdown_by_feature: bool
        def __init__(self, distance_type: _Optional[_Union[_distance_pb2.DistanceType, str]] = ..., prediction_spec_1: _Optional[_Union[ModelComparisonRequest.PredictionSpec, _Mapping]] = ..., prediction_spec_2: _Optional[_Union[ModelComparisonRequest.PredictionSpec, _Mapping]] = ..., include_prediction_distance: bool = ..., include_breakdown_by_feature: bool = ...) -> None: ...
    COMPARISON_SPECS_FIELD_NUMBER: _ClassVar[int]
    comparison_specs: _containers.RepeatedCompositeFieldContainer[ModelComparisonRequest.ModelComparisonSpec]
    def __init__(self, comparison_specs: _Optional[_Iterable[_Union[ModelComparisonRequest.ModelComparisonSpec, _Mapping]]] = ...) -> None: ...

class ModelBiasRequest(_message.Message):
    __slots__ = ("bias_type", "model_id", "query_spec_1", "query_spec_2", "qoi", "classification_threshold", "positive_class_favored", "threshold_context")
    BIAS_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_SPEC_1_FIELD_NUMBER: _ClassVar[int]
    QUERY_SPEC_2_FIELD_NUMBER: _ClassVar[int]
    QOI_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    POSITIVE_CLASS_FAVORED_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    bias_type: _intelligence_service_pb2.BiasType.Type
    model_id: str
    query_spec_1: QuerySpec
    query_spec_2: QuerySpec
    qoi: _qoi_pb2.QuantityOfInterest
    classification_threshold: float
    positive_class_favored: bool
    threshold_context: ClassificationThresholdContext
    def __init__(self, bias_type: _Optional[_Union[_intelligence_service_pb2.BiasType.Type, str]] = ..., model_id: _Optional[str] = ..., query_spec_1: _Optional[_Union[QuerySpec, _Mapping]] = ..., query_spec_2: _Optional[_Union[QuerySpec, _Mapping]] = ..., qoi: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., classification_threshold: _Optional[float] = ..., positive_class_favored: bool = ..., threshold_context: _Optional[_Union[ClassificationThresholdContext, _Mapping]] = ...) -> None: ...

class BucketizedStatsRequest(_message.Message):
    __slots__ = ("model_id", "qoi", "query_spec", "classification_threshold", "stats_type", "threshold_context")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    QOI_FIELD_NUMBER: _ClassVar[int]
    QUERY_SPEC_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    STATS_TYPE_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    qoi: _qoi_pb2.QuantityOfInterest
    query_spec: QuerySpec
    classification_threshold: float
    stats_type: _intelligence_service_pb2.BucketizedStatsType.Type
    threshold_context: ClassificationThresholdContext
    def __init__(self, model_id: _Optional[str] = ..., qoi: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., query_spec: _Optional[_Union[QuerySpec, _Mapping]] = ..., classification_threshold: _Optional[float] = ..., stats_type: _Optional[_Union[_intelligence_service_pb2.BucketizedStatsType.Type, str]] = ..., threshold_context: _Optional[_Union[ClassificationThresholdContext, _Mapping]] = ...) -> None: ...

class DriftInputSpec(_message.Message):
    __slots__ = ("raw_data_request",)
    RAW_DATA_REQUEST_FIELD_NUMBER: _ClassVar[int]
    raw_data_request: RawDataRequest
    def __init__(self, raw_data_request: _Optional[_Union[RawDataRequest, _Mapping]] = ...) -> None: ...

class DriftRequest(_message.Message):
    __slots__ = ("comparison_spec",)
    class DriftComparisonSpec(_message.Message):
        __slots__ = ("distance_types", "drift_input_spec_1", "drift_input_spec_2")
        DISTANCE_TYPES_FIELD_NUMBER: _ClassVar[int]
        DRIFT_INPUT_SPEC_1_FIELD_NUMBER: _ClassVar[int]
        DRIFT_INPUT_SPEC_2_FIELD_NUMBER: _ClassVar[int]
        distance_types: _containers.RepeatedScalarFieldContainer[_distance_pb2.DistanceType]
        drift_input_spec_1: DriftInputSpec
        drift_input_spec_2: DriftInputSpec
        def __init__(self, distance_types: _Optional[_Iterable[_Union[_distance_pb2.DistanceType, str]]] = ..., drift_input_spec_1: _Optional[_Union[DriftInputSpec, _Mapping]] = ..., drift_input_spec_2: _Optional[_Union[DriftInputSpec, _Mapping]] = ...) -> None: ...
    COMPARISON_SPEC_FIELD_NUMBER: _ClassVar[int]
    comparison_spec: DriftRequest.DriftComparisonSpec
    def __init__(self, comparison_spec: _Optional[_Union[DriftRequest.DriftComparisonSpec, _Mapping]] = ...) -> None: ...

class ISPRequest(_message.Message):
    __slots__ = ("model_id", "query_spec", "fv_grid_size", "fi_grid_size", "options")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_SPEC_FIELD_NUMBER: _ClassVar[int]
    FV_GRID_SIZE_FIELD_NUMBER: _ClassVar[int]
    FI_GRID_SIZE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    query_spec: QuerySpec
    fv_grid_size: int
    fi_grid_size: int
    options: _common_pb2.FeatureInfluenceOptions
    def __init__(self, model_id: _Optional[str] = ..., query_spec: _Optional[_Union[QuerySpec, _Mapping]] = ..., fv_grid_size: _Optional[int] = ..., fi_grid_size: _Optional[int] = ..., options: _Optional[_Union[_common_pb2.FeatureInfluenceOptions, _Mapping]] = ...) -> None: ...

class FeedbackThresholdsRequest(_message.Message):
    __slots__ = ("model_id", "query_spec", "thresholds")
    class FeedbackThresholds(_message.Message):
        __slots__ = ("feedback_function_id", "threshold")
        FEEDBACK_FUNCTION_ID_FIELD_NUMBER: _ClassVar[int]
        THRESHOLD_FIELD_NUMBER: _ClassVar[int]
        feedback_function_id: str
        threshold: float
        def __init__(self, feedback_function_id: _Optional[str] = ..., threshold: _Optional[float] = ...) -> None: ...
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_SPEC_FIELD_NUMBER: _ClassVar[int]
    THRESHOLDS_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    query_spec: QuerySpec
    thresholds: _containers.RepeatedCompositeFieldContainer[FeedbackThresholdsRequest.FeedbackThresholds]
    def __init__(self, model_id: _Optional[str] = ..., query_spec: _Optional[_Union[QuerySpec, _Mapping]] = ..., thresholds: _Optional[_Iterable[_Union[FeedbackThresholdsRequest.FeedbackThresholds, _Mapping]]] = ...) -> None: ...

class RotUsed(_message.Message):
    __slots__ = ("rot_metadata", "latest_rot_status")
    ROT_METADATA_FIELD_NUMBER: _ClassVar[int]
    LATEST_ROT_STATUS_FIELD_NUMBER: _ClassVar[int]
    rot_metadata: _read_optimized_table_messages_pb2.RotMetadata
    latest_rot_status: _read_optimized_table_messages_pb2.RotStatus
    def __init__(self, rot_metadata: _Optional[_Union[_read_optimized_table_messages_pb2.RotMetadata, _Mapping]] = ..., latest_rot_status: _Optional[_Union[_read_optimized_table_messages_pb2.RotStatus, str]] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("request_id", "row_major_value_table", "page_number", "rots_used")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ROW_MAJOR_VALUE_TABLE_FIELD_NUMBER: _ClassVar[int]
    PAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ROTS_USED_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    row_major_value_table: RowMajorValueTable
    page_number: int
    rots_used: _containers.RepeatedCompositeFieldContainer[RotUsed]
    def __init__(self, request_id: _Optional[str] = ..., row_major_value_table: _Optional[_Union[RowMajorValueTable, _Mapping]] = ..., page_number: _Optional[int] = ..., rots_used: _Optional[_Iterable[_Union[RotUsed, _Mapping]]] = ...) -> None: ...

class QuerySpec(_message.Message):
    __slots__ = ("split_id", "selection_options", "filter", "operation_types", "aggregation_types", "select_columns", "skip_initial_rows", "ranking_options", "group_by_columns")
    class RankingOptions(_message.Message):
        __slots__ = ("project_ranking_K", "ranking_qoi", "ranking_model_id")
        PROJECT_RANKING_K_FIELD_NUMBER: _ClassVar[int]
        RANKING_QOI_FIELD_NUMBER: _ClassVar[int]
        RANKING_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
        project_ranking_K: int
        ranking_qoi: _qoi_pb2.QuantityOfInterest
        ranking_model_id: str
        def __init__(self, project_ranking_K: _Optional[int] = ..., ranking_qoi: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., ranking_model_id: _Optional[str] = ...) -> None: ...
    class SelectionOptions(_message.Message):
        __slots__ = ("all_align_to_pre", "all_available_data", "uniform_random_n")
        class AllAlignToPre(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        class AllAvailableData(_message.Message):
            __slots__ = ("sample_size",)
            SAMPLE_SIZE_FIELD_NUMBER: _ClassVar[int]
            sample_size: int
            def __init__(self, sample_size: _Optional[int] = ...) -> None: ...
        class UniformRandomN(_message.Message):
            __slots__ = ("sample_size",)
            SAMPLE_SIZE_FIELD_NUMBER: _ClassVar[int]
            sample_size: int
            def __init__(self, sample_size: _Optional[int] = ...) -> None: ...
        ALL_ALIGN_TO_PRE_FIELD_NUMBER: _ClassVar[int]
        ALL_AVAILABLE_DATA_FIELD_NUMBER: _ClassVar[int]
        UNIFORM_RANDOM_N_FIELD_NUMBER: _ClassVar[int]
        all_align_to_pre: QuerySpec.SelectionOptions.AllAlignToPre
        all_available_data: QuerySpec.SelectionOptions.AllAvailableData
        uniform_random_n: QuerySpec.SelectionOptions.UniformRandomN
        def __init__(self, all_align_to_pre: _Optional[_Union[QuerySpec.SelectionOptions.AllAlignToPre, _Mapping]] = ..., all_available_data: _Optional[_Union[QuerySpec.SelectionOptions.AllAvailableData, _Mapping]] = ..., uniform_random_n: _Optional[_Union[QuerySpec.SelectionOptions.UniformRandomN, _Mapping]] = ...) -> None: ...
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    SELECTION_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    OPERATION_TYPES_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_TYPES_FIELD_NUMBER: _ClassVar[int]
    SELECT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    SKIP_INITIAL_ROWS_FIELD_NUMBER: _ClassVar[int]
    RANKING_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    split_id: str
    selection_options: QuerySpec.SelectionOptions
    filter: _filter_pb2.FilterExpression
    operation_types: _containers.RepeatedScalarFieldContainer[_intelligence_service_pb2.DataSummaryRequest.OperationType]
    aggregation_types: _containers.RepeatedScalarFieldContainer[_intelligence_service_pb2.DataSummaryRequest.AggregationType]
    select_columns: _containers.RepeatedScalarFieldContainer[str]
    skip_initial_rows: int
    ranking_options: QuerySpec.RankingOptions
    group_by_columns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, split_id: _Optional[str] = ..., selection_options: _Optional[_Union[QuerySpec.SelectionOptions, _Mapping]] = ..., filter: _Optional[_Union[_filter_pb2.FilterExpression, _Mapping]] = ..., operation_types: _Optional[_Iterable[_Union[_intelligence_service_pb2.DataSummaryRequest.OperationType, str]]] = ..., aggregation_types: _Optional[_Iterable[_Union[_intelligence_service_pb2.DataSummaryRequest.AggregationType, str]]] = ..., select_columns: _Optional[_Iterable[str]] = ..., skip_initial_rows: _Optional[int] = ..., ranking_options: _Optional[_Union[QuerySpec.RankingOptions, _Mapping]] = ..., group_by_columns: _Optional[_Iterable[str]] = ...) -> None: ...

class QueryItem(_message.Message):
    __slots__ = ("data_kind", "prediction_options", "feature_influence_options", "classification_threshold", "model_id", "query_spec", "threshold_context")
    DATA_KIND_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_INFLUENCE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_SPEC_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    data_kind: _data_kind_pb2.DataKindDescribed
    prediction_options: _common_pb2.PredictionOptions
    feature_influence_options: _common_pb2.FeatureInfluenceOptions
    classification_threshold: float
    model_id: str
    query_spec: QuerySpec
    threshold_context: ClassificationThresholdContext
    def __init__(self, data_kind: _Optional[_Union[_data_kind_pb2.DataKindDescribed, str]] = ..., prediction_options: _Optional[_Union[_common_pb2.PredictionOptions, _Mapping]] = ..., feature_influence_options: _Optional[_Union[_common_pb2.FeatureInfluenceOptions, _Mapping]] = ..., classification_threshold: _Optional[float] = ..., model_id: _Optional[str] = ..., query_spec: _Optional[_Union[QuerySpec, _Mapping]] = ..., threshold_context: _Optional[_Union[ClassificationThresholdContext, _Mapping]] = ...) -> None: ...

class RowMajorValueTable(_message.Message):
    __slots__ = ("row_count", "metadata", "rows")
    ROW_COUNT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    row_count: int
    metadata: _containers.RepeatedCompositeFieldContainer[ColumnMetadata]
    rows: _containers.RepeatedCompositeFieldContainer[_row_pb2.Row]
    def __init__(self, row_count: _Optional[int] = ..., metadata: _Optional[_Iterable[_Union[ColumnMetadata, _Mapping]]] = ..., rows: _Optional[_Iterable[_Union[_row_pb2.Row, _Mapping]]] = ...) -> None: ...

class ArrayType(_message.Message):
    __slots__ = ("inner_type",)
    INNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    inner_type: MergedType
    def __init__(self, inner_type: _Optional[_Union[MergedType, _Mapping]] = ...) -> None: ...

class MergedType(_message.Message):
    __slots__ = ("value_type", "array_type")
    VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARRAY_TYPE_FIELD_NUMBER: _ClassVar[int]
    value_type: ValueType
    array_type: ArrayType
    def __init__(self, value_type: _Optional[_Union[ValueType, str]] = ..., array_type: _Optional[_Union[ArrayType, _Mapping]] = ...) -> None: ...

class ColumnMetadata(_message.Message):
    __slots__ = ("index", "name", "type", "array_type")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ARRAY_TYPE_FIELD_NUMBER: _ClassVar[int]
    index: int
    name: str
    type: ValueType
    array_type: ArrayType
    def __init__(self, index: _Optional[int] = ..., name: _Optional[str] = ..., type: _Optional[_Union[ValueType, str]] = ..., array_type: _Optional[_Union[ArrayType, _Mapping]] = ...) -> None: ...

class AccuracyRequest(_message.Message):
    __slots__ = ("project_id", "model_id", "accuracy_type", "query_spec", "qoi", "classification_threshold", "include_confusion_matrix", "request_id", "include_compute_record_count", "threshold_context", "return_rot_metadata_only", "include_precision_recall_curve", "include_roc_curve")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_TYPE_FIELD_NUMBER: _ClassVar[int]
    QUERY_SPEC_FIELD_NUMBER: _ClassVar[int]
    QOI_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CONFUSION_MATRIX_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_COMPUTE_RECORD_COUNT_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    RETURN_ROT_METADATA_ONLY_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PRECISION_RECALL_CURVE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ROC_CURVE_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_id: str
    accuracy_type: _containers.RepeatedScalarFieldContainer[_accuracy_pb2.AccuracyType.Type]
    query_spec: QuerySpec
    qoi: _qoi_pb2.QuantityOfInterest
    classification_threshold: float
    include_confusion_matrix: bool
    request_id: str
    include_compute_record_count: bool
    threshold_context: ClassificationThresholdContext
    return_rot_metadata_only: bool
    include_precision_recall_curve: bool
    include_roc_curve: bool
    def __init__(self, project_id: _Optional[str] = ..., model_id: _Optional[str] = ..., accuracy_type: _Optional[_Iterable[_Union[_accuracy_pb2.AccuracyType.Type, str]]] = ..., query_spec: _Optional[_Union[QuerySpec, _Mapping]] = ..., qoi: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., classification_threshold: _Optional[float] = ..., include_confusion_matrix: bool = ..., request_id: _Optional[str] = ..., include_compute_record_count: bool = ..., threshold_context: _Optional[_Union[ClassificationThresholdContext, _Mapping]] = ..., return_rot_metadata_only: bool = ..., include_precision_recall_curve: bool = ..., include_roc_curve: bool = ...) -> None: ...

class AccuracyResponse(_message.Message):
    __slots__ = ("accuracy_results", "confusion_matrix", "request_id", "computation_record_count", "rots_used", "precision_recall_curve", "roc_curve")
    ACCURACY_RESULTS_FIELD_NUMBER: _ClassVar[int]
    CONFUSION_MATRIX_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    COMPUTATION_RECORD_COUNT_FIELD_NUMBER: _ClassVar[int]
    ROTS_USED_FIELD_NUMBER: _ClassVar[int]
    PRECISION_RECALL_CURVE_FIELD_NUMBER: _ClassVar[int]
    ROC_CURVE_FIELD_NUMBER: _ClassVar[int]
    accuracy_results: _containers.RepeatedCompositeFieldContainer[AccuracyResult]
    confusion_matrix: _accuracy_pb2.ConfusionMatrix
    request_id: str
    computation_record_count: int
    rots_used: _containers.RepeatedCompositeFieldContainer[RotUsed]
    precision_recall_curve: _accuracy_pb2.PrecisionRecallCurve
    roc_curve: _accuracy_pb2.RocCurve
    def __init__(self, accuracy_results: _Optional[_Iterable[_Union[AccuracyResult, _Mapping]]] = ..., confusion_matrix: _Optional[_Union[_accuracy_pb2.ConfusionMatrix, _Mapping]] = ..., request_id: _Optional[str] = ..., computation_record_count: _Optional[int] = ..., rots_used: _Optional[_Iterable[_Union[RotUsed, _Mapping]]] = ..., precision_recall_curve: _Optional[_Union[_accuracy_pb2.PrecisionRecallCurve, _Mapping]] = ..., roc_curve: _Optional[_Union[_accuracy_pb2.RocCurve, _Mapping]] = ...) -> None: ...

class AccuracyResult(_message.Message):
    __slots__ = ("accuracy_type", "value", "error_code", "interpretation")
    ACCURACY_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    INTERPRETATION_FIELD_NUMBER: _ClassVar[int]
    accuracy_type: _accuracy_pb2.AccuracyType.Type
    value: float
    error_code: AccuracyErrorCode
    interpretation: _accuracy_pb2.AccuracyResult.AccuracyInterpretation
    def __init__(self, accuracy_type: _Optional[_Union[_accuracy_pb2.AccuracyType.Type, str]] = ..., value: _Optional[float] = ..., error_code: _Optional[_Union[AccuracyErrorCode, str]] = ..., interpretation: _Optional[_Union[_accuracy_pb2.AccuracyResult.AccuracyInterpretation, str]] = ...) -> None: ...

class EchoRequest(_message.Message):
    __slots__ = ("request_id", "message")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    message: str
    def __init__(self, request_id: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class EchoResponse(_message.Message):
    __slots__ = ("request_id", "response")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    response: str
    def __init__(self, request_id: _Optional[str] = ..., response: _Optional[str] = ...) -> None: ...

class QueryItemResult(_message.Message):
    __slots__ = ("row_major_value_table", "error_code", "rots_used")
    class QueryError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NO_ERROR: _ClassVar[QueryItemResult.QueryError]
        DATA_LOCATOR_NOT_FOUND: _ClassVar[QueryItemResult.QueryError]
        MISSING_REQUIRED_DETAILS: _ClassVar[QueryItemResult.QueryError]
        INVALID_OPERATION: _ClassVar[QueryItemResult.QueryError]
        INVALID_AGGREGATION: _ClassVar[QueryItemResult.QueryError]
        COLUMN_NOT_FOUND: _ClassVar[QueryItemResult.QueryError]
        DATA_COLLECTION_NOT_FOUND: _ClassVar[QueryItemResult.QueryError]
        INVALID_FILTER_EXPRESSION: _ClassVar[QueryItemResult.QueryError]
        MULTIPLE_DATA_LOCATORS_FOUND: _ClassVar[QueryItemResult.QueryError]
        MULTIPLE_OPTION_HASH_FOUND: _ClassVar[QueryItemResult.QueryError]
        OPTION_HASH_NOT_FOUND: _ClassVar[QueryItemResult.QueryError]
        PREDICTION_SCORE_NOT_FOUND: _ClassVar[QueryItemResult.QueryError]
        SCHEMA_NOT_FOUND: _ClassVar[QueryItemResult.QueryError]
        UNKNOWN_ERROR: _ClassVar[QueryItemResult.QueryError]
        INVALID_PROJECT_RANKING_K: _ClassVar[QueryItemResult.QueryError]
        MATERIALIZE_METADATA_NOT_FOUND: _ClassVar[QueryItemResult.QueryError]
        NOT_SUPPORTED: _ClassVar[QueryItemResult.QueryError]
    NO_ERROR: QueryItemResult.QueryError
    DATA_LOCATOR_NOT_FOUND: QueryItemResult.QueryError
    MISSING_REQUIRED_DETAILS: QueryItemResult.QueryError
    INVALID_OPERATION: QueryItemResult.QueryError
    INVALID_AGGREGATION: QueryItemResult.QueryError
    COLUMN_NOT_FOUND: QueryItemResult.QueryError
    DATA_COLLECTION_NOT_FOUND: QueryItemResult.QueryError
    INVALID_FILTER_EXPRESSION: QueryItemResult.QueryError
    MULTIPLE_DATA_LOCATORS_FOUND: QueryItemResult.QueryError
    MULTIPLE_OPTION_HASH_FOUND: QueryItemResult.QueryError
    OPTION_HASH_NOT_FOUND: QueryItemResult.QueryError
    PREDICTION_SCORE_NOT_FOUND: QueryItemResult.QueryError
    SCHEMA_NOT_FOUND: QueryItemResult.QueryError
    UNKNOWN_ERROR: QueryItemResult.QueryError
    INVALID_PROJECT_RANKING_K: QueryItemResult.QueryError
    MATERIALIZE_METADATA_NOT_FOUND: QueryItemResult.QueryError
    NOT_SUPPORTED: QueryItemResult.QueryError
    ROW_MAJOR_VALUE_TABLE_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ROTS_USED_FIELD_NUMBER: _ClassVar[int]
    row_major_value_table: RowMajorValueTable
    error_code: QueryItemResult.QueryError
    rots_used: _containers.RepeatedCompositeFieldContainer[RotUsed]
    def __init__(self, row_major_value_table: _Optional[_Union[RowMajorValueTable, _Mapping]] = ..., error_code: _Optional[_Union[QueryItemResult.QueryError, str]] = ..., rots_used: _Optional[_Iterable[_Union[RotUsed, _Mapping]]] = ...) -> None: ...

class BatchQueryRequest(_message.Message):
    __slots__ = ("request_id", "project_id", "data_collection_id", "query_items", "return_rot_metadata_only")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_ITEMS_FIELD_NUMBER: _ClassVar[int]
    RETURN_ROT_METADATA_ONLY_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    project_id: str
    data_collection_id: str
    query_items: _containers.RepeatedCompositeFieldContainer[QueryItem]
    return_rot_metadata_only: bool
    def __init__(self, request_id: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., query_items: _Optional[_Iterable[_Union[QueryItem, _Mapping]]] = ..., return_rot_metadata_only: bool = ...) -> None: ...

class BatchQueryResponse(_message.Message):
    __slots__ = ("request_id", "results")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    results: _containers.RepeatedCompositeFieldContainer[QueryItemResult]
    def __init__(self, request_id: _Optional[str] = ..., results: _Optional[_Iterable[_Union[QueryItemResult, _Mapping]]] = ...) -> None: ...

class ClassificationThresholdContext(_message.Message):
    __slots__ = ("qoi", "threshold")
    QOI_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    qoi: _qoi_pb2.QuantityOfInterest
    threshold: float
    def __init__(self, qoi: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., threshold: _Optional[float] = ...) -> None: ...
