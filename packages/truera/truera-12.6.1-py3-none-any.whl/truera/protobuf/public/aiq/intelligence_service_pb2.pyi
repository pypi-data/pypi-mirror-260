from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import any_pb2 as _any_pb2
from truera.protobuf.public import artifactrepo_pb2 as _artifactrepo_pb2
from truera.protobuf.public import common_pb2 as _common_pb2
from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from truera.protobuf.public.aiq import distance_pb2 as _distance_pb2
from truera.protobuf.public import background_data_split_info_pb2 as _background_data_split_info_pb2
from truera.protobuf.public.data import data_split_pb2 as _data_split_pb2
from truera.protobuf.public.data import filter_pb2 as _filter_pb2
from truera.protobuf.public.data import segment_pb2 as _segment_pb2
from truera.protobuf.public.util import elementary_types_pb2 as _elementary_types_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from truera.protobuf.public.aiq import accuracy_pb2 as _accuracy_pb2
from truera.protobuf.public import metadata_message_types_pb2 as _metadata_message_types_pb2
from truera.protobuf.public.read_optimized_table_service import read_optimized_table_messages_pb2 as _read_optimized_table_messages_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModelDataRequestType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[ModelDataRequestType]
    FILTER: _ClassVar[ModelDataRequestType]
    CALIBRATION: _ClassVar[ModelDataRequestType]
    FEATURE_SORT: _ClassVar[ModelDataRequestType]
    FEATURE_SPLINE: _ClassVar[ModelDataRequestType]

class FeatureSortMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ABSOLUTE_VALUE_SUM: _ClassVar[FeatureSortMethod]
    ABSOLUTE_VALUE_SUM_MEAN_CORRECTED: _ClassVar[FeatureSortMethod]
    VARIANCE: _ClassVar[FeatureSortMethod]
    LINEAR_TREND: _ClassVar[FeatureSortMethod]
    CUBIC_TREND: _ClassVar[FeatureSortMethod]
    TREND_LOW_RESIDUAL: _ClassVar[FeatureSortMethod]
    TREND_OUTLIERS: _ClassVar[FeatureSortMethod]
    MAX_INFLUENCE: _ClassVar[FeatureSortMethod]
    MULTI_MODAL: _ClassVar[FeatureSortMethod]
    CATEGORICAL_OUTLIERS: _ClassVar[FeatureSortMethod]
    TREND_R_SQUARED: _ClassVar[FeatureSortMethod]

class FeatureSplineType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LINEAR: _ClassVar[FeatureSplineType]
    CUBIC: _ClassVar[FeatureSplineType]

class PredicateType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PT_UNKNOWN: _ClassVar[PredicateType]
    PT_LOWER_BOUND: _ClassVar[PredicateType]
    PT_UPPER_BOUND: _ClassVar[PredicateType]
    PT_IN: _ClassVar[PredicateType]
    PT_IS_NOT_CATEGORY: _ClassVar[PredicateType]
    PT_IS_CATEGORY: _ClassVar[PredicateType]
UNKNOWN: ModelDataRequestType
FILTER: ModelDataRequestType
CALIBRATION: ModelDataRequestType
FEATURE_SORT: ModelDataRequestType
FEATURE_SPLINE: ModelDataRequestType
ABSOLUTE_VALUE_SUM: FeatureSortMethod
ABSOLUTE_VALUE_SUM_MEAN_CORRECTED: FeatureSortMethod
VARIANCE: FeatureSortMethod
LINEAR_TREND: FeatureSortMethod
CUBIC_TREND: FeatureSortMethod
TREND_LOW_RESIDUAL: FeatureSortMethod
TREND_OUTLIERS: FeatureSortMethod
MAX_INFLUENCE: FeatureSortMethod
MULTI_MODAL: FeatureSortMethod
CATEGORICAL_OUTLIERS: FeatureSortMethod
TREND_R_SQUARED: FeatureSortMethod
LINEAR: FeatureSplineType
CUBIC: FeatureSplineType
PT_UNKNOWN: PredicateType
PT_LOWER_BOUND: PredicateType
PT_UPPER_BOUND: PredicateType
PT_IN: PredicateType
PT_IS_NOT_CATEGORY: PredicateType
PT_IS_CATEGORY: PredicateType

class PendingOperations(_message.Message):
    __slots__ = ("waiting_on_operation_ids",)
    WAITING_ON_OPERATION_IDS_FIELD_NUMBER: _ClassVar[int]
    waiting_on_operation_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, waiting_on_operation_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ModelId(_message.Message):
    __slots__ = ("project_id", "model_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_id: str
    def __init__(self, project_id: _Optional[str] = ..., model_id: _Optional[str] = ...) -> None: ...

class ModelInputSpec(_message.Message):
    __slots__ = ("dataset_index", "dataset_index_range", "standard_bulk_inputs", "all_available_inputs", "split_id", "filter_expression", "ranking_spec")
    DATASET_INDEX_FIELD_NUMBER: _ClassVar[int]
    DATASET_INDEX_RANGE_FIELD_NUMBER: _ClassVar[int]
    STANDARD_BULK_INPUTS_FIELD_NUMBER: _ClassVar[int]
    ALL_AVAILABLE_INPUTS_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    FILTER_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    RANKING_SPEC_FIELD_NUMBER: _ClassVar[int]
    dataset_index: int
    dataset_index_range: IndexRange
    standard_bulk_inputs: bool
    all_available_inputs: bool
    split_id: str
    filter_expression: _filter_pb2.FilterExpression
    ranking_spec: RankingSpec
    def __init__(self, dataset_index: _Optional[int] = ..., dataset_index_range: _Optional[_Union[IndexRange, _Mapping]] = ..., standard_bulk_inputs: bool = ..., all_available_inputs: bool = ..., split_id: _Optional[str] = ..., filter_expression: _Optional[_Union[_filter_pb2.FilterExpression, _Mapping]] = ..., ranking_spec: _Optional[_Union[RankingSpec, _Mapping]] = ...) -> None: ...

class RankingSpec(_message.Message):
    __slots__ = ("num_per_group", "model_id", "quantity_of_interest")
    NUM_PER_GROUP_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_OF_INTEREST_FIELD_NUMBER: _ClassVar[int]
    num_per_group: int
    model_id: str
    quantity_of_interest: _qoi_pb2.QuantityOfInterest
    def __init__(self, num_per_group: _Optional[int] = ..., model_id: _Optional[str] = ..., quantity_of_interest: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ...) -> None: ...

class RotInfo(_message.Message):
    __slots__ = ("id", "query_metadata", "last_updated_timestamp", "rot_status")
    ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_METADATA_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ROT_STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    query_metadata: _read_optimized_table_messages_pb2.RotQueryMetadata
    last_updated_timestamp: _timestamp_pb2.Timestamp
    rot_status: _read_optimized_table_messages_pb2.RotStatus
    def __init__(self, id: _Optional[str] = ..., query_metadata: _Optional[_Union[_read_optimized_table_messages_pb2.RotQueryMetadata, _Mapping]] = ..., last_updated_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., rot_status: _Optional[_Union[_read_optimized_table_messages_pb2.RotStatus, str]] = ...) -> None: ...

class SplitMetaData(_message.Message):
    __slots__ = ("split_id", "split_name", "split_type", "ordered_column_names", "system_columns", "label_column_name", "time_window_filter")
    class SystemColumns(_message.Message):
        __slots__ = ("unique_id_column_name", "timestamp_column_name")
        UNIQUE_ID_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
        unique_id_column_name: str
        timestamp_column_name: str
        def __init__(self, unique_id_column_name: _Optional[str] = ..., timestamp_column_name: _Optional[str] = ...) -> None: ...
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_NAME_FIELD_NUMBER: _ClassVar[int]
    SPLIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDERED_COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    LABEL_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FILTER_FIELD_NUMBER: _ClassVar[int]
    split_id: str
    split_name: str
    split_type: _data_split_pb2.DataSplitType
    ordered_column_names: _elementary_types_pb2.StringList
    system_columns: SplitMetaData.SystemColumns
    label_column_name: str
    time_window_filter: _metadata_message_types_pb2.TimeWindowFilter
    def __init__(self, split_id: _Optional[str] = ..., split_name: _Optional[str] = ..., split_type: _Optional[_Union[_data_split_pb2.DataSplitType, str]] = ..., ordered_column_names: _Optional[_Union[_elementary_types_pb2.StringList, _Mapping]] = ..., system_columns: _Optional[_Union[SplitMetaData.SystemColumns, _Mapping]] = ..., label_column_name: _Optional[str] = ..., time_window_filter: _Optional[_Union[_metadata_message_types_pb2.TimeWindowFilter, _Mapping]] = ...) -> None: ...

class ModelDataRequest(_message.Message):
    __slots__ = ("model_id", "input_spec", "request_entry")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ENTRY_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    input_spec: ModelInputSpec
    request_entry: _containers.RepeatedCompositeFieldContainer[ModelDataRequestEntry]
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., request_entry: _Optional[_Iterable[_Union[ModelDataRequestEntry, _Mapping]]] = ...) -> None: ...

class ModelDataRequestEntry(_message.Message):
    __slots__ = ("type", "options")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    type: ModelDataRequestType
    options: ModelDataRequestEntryOptions
    def __init__(self, type: _Optional[_Union[ModelDataRequestType, str]] = ..., options: _Optional[_Union[ModelDataRequestEntryOptions, _Mapping]] = ...) -> None: ...

class ModelDataRequestEntryOptions(_message.Message):
    __slots__ = ("filter_options", "feature_sort_options", "feature_spline_options")
    FILTER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SORT_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SPLINE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    filter_options: FilterOptions
    feature_sort_options: FeatureSortOptions
    feature_spline_options: FeatureSplineOptions
    def __init__(self, filter_options: _Optional[_Union[FilterOptions, _Mapping]] = ..., feature_sort_options: _Optional[_Union[FeatureSortOptions, _Mapping]] = ..., feature_spline_options: _Optional[_Union[FeatureSplineOptions, _Mapping]] = ...) -> None: ...

class ReduceDimensionOptions(_message.Message):
    __slots__ = ("method",)
    class ReduceDimensionMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        REDUCE_DIM_NONE: _ClassVar[ReduceDimensionOptions.ReduceDimensionMethod]
        REDUCE_DIM_TSNE: _ClassVar[ReduceDimensionOptions.ReduceDimensionMethod]
        REDUCE_DIM_PCA: _ClassVar[ReduceDimensionOptions.ReduceDimensionMethod]
    REDUCE_DIM_NONE: ReduceDimensionOptions.ReduceDimensionMethod
    REDUCE_DIM_TSNE: ReduceDimensionOptions.ReduceDimensionMethod
    REDUCE_DIM_PCA: ReduceDimensionOptions.ReduceDimensionMethod
    METHOD_FIELD_NUMBER: _ClassVar[int]
    method: ReduceDimensionOptions.ReduceDimensionMethod
    def __init__(self, method: _Optional[_Union[ReduceDimensionOptions.ReduceDimensionMethod, str]] = ...) -> None: ...

class FilterOptions(_message.Message):
    __slots__ = ("filter_expression",)
    FILTER_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    filter_expression: _filter_pb2.FilterExpression
    def __init__(self, filter_expression: _Optional[_Union[_filter_pb2.FilterExpression, _Mapping]] = ...) -> None: ...

class FeatureSortOptions(_message.Message):
    __slots__ = ("sort_methods", "spline_exclude_vals")
    SORT_METHODS_FIELD_NUMBER: _ClassVar[int]
    SPLINE_EXCLUDE_VALS_FIELD_NUMBER: _ClassVar[int]
    sort_methods: _containers.RepeatedScalarFieldContainer[FeatureSortMethod]
    spline_exclude_vals: FloatTable
    def __init__(self, sort_methods: _Optional[_Iterable[_Union[FeatureSortMethod, str]]] = ..., spline_exclude_vals: _Optional[_Union[FloatTable, _Mapping]] = ...) -> None: ...

class FeatureSplineOptions(_message.Message):
    __slots__ = ("spline_type", "spline_resolution", "spline_exclude_vals")
    SPLINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SPLINE_RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    SPLINE_EXCLUDE_VALS_FIELD_NUMBER: _ClassVar[int]
    spline_type: FeatureSplineType
    spline_resolution: int
    spline_exclude_vals: FloatTable
    def __init__(self, spline_type: _Optional[_Union[FeatureSplineType, str]] = ..., spline_resolution: _Optional[int] = ..., spline_exclude_vals: _Optional[_Union[FloatTable, _Mapping]] = ...) -> None: ...

class CoordinateResponseEntry(_message.Message):
    __slots__ = ("x_float_table", "y_float_table")
    X_FLOAT_TABLE_FIELD_NUMBER: _ClassVar[int]
    Y_FLOAT_TABLE_FIELD_NUMBER: _ClassVar[int]
    x_float_table: FloatTable
    y_float_table: FloatTable
    def __init__(self, x_float_table: _Optional[_Union[FloatTable, _Mapping]] = ..., y_float_table: _Optional[_Union[FloatTable, _Mapping]] = ...) -> None: ...

class ModelDataResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: _containers.RepeatedCompositeFieldContainer[ModelDataResponseEntry]
    def __init__(self, entry: _Optional[_Iterable[_Union[ModelDataResponseEntry, _Mapping]]] = ...) -> None: ...

class ModelDataResponseEntry(_message.Message):
    __slots__ = ("float_table", "value_table", "bool_table", "coordinates", "type", "pending_operations")
    FLOAT_TABLE_FIELD_NUMBER: _ClassVar[int]
    VALUE_TABLE_FIELD_NUMBER: _ClassVar[int]
    BOOL_TABLE_FIELD_NUMBER: _ClassVar[int]
    COORDINATES_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    float_table: FloatTable
    value_table: ValueTable
    bool_table: BoolTable
    coordinates: CoordinateResponseEntry
    type: ModelDataRequestType
    pending_operations: PendingOperations
    def __init__(self, float_table: _Optional[_Union[FloatTable, _Mapping]] = ..., value_table: _Optional[_Union[ValueTable, _Mapping]] = ..., bool_table: _Optional[_Union[BoolTable, _Mapping]] = ..., coordinates: _Optional[_Union[CoordinateResponseEntry, _Mapping]] = ..., type: _Optional[_Union[ModelDataRequestType, str]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ...) -> None: ...

class FloatTable(_message.Message):
    __slots__ = ("column_value_map", "row_labels")
    class ColumnValueMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _elementary_types_pb2.FloatList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_elementary_types_pb2.FloatList, _Mapping]] = ...) -> None: ...
    COLUMN_VALUE_MAP_FIELD_NUMBER: _ClassVar[int]
    ROW_LABELS_FIELD_NUMBER: _ClassVar[int]
    column_value_map: _containers.MessageMap[str, _elementary_types_pb2.FloatList]
    row_labels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, column_value_map: _Optional[_Mapping[str, _elementary_types_pb2.FloatList]] = ..., row_labels: _Optional[_Iterable[str]] = ...) -> None: ...

class BoolTable(_message.Message):
    __slots__ = ("column_value_map", "row_labels")
    class ColumnValueMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: BoolList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[BoolList, _Mapping]] = ...) -> None: ...
    COLUMN_VALUE_MAP_FIELD_NUMBER: _ClassVar[int]
    ROW_LABELS_FIELD_NUMBER: _ClassVar[int]
    column_value_map: _containers.MessageMap[str, BoolList]
    row_labels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, column_value_map: _Optional[_Mapping[str, BoolList]] = ..., row_labels: _Optional[_Iterable[str]] = ...) -> None: ...

class ValueTable(_message.Message):
    __slots__ = ("column_value_map", "row_labels")
    class ColumnValueMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _elementary_types_pb2.ValueList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_elementary_types_pb2.ValueList, _Mapping]] = ...) -> None: ...
    COLUMN_VALUE_MAP_FIELD_NUMBER: _ClassVar[int]
    ROW_LABELS_FIELD_NUMBER: _ClassVar[int]
    column_value_map: _containers.MessageMap[str, _elementary_types_pb2.ValueList]
    row_labels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, column_value_map: _Optional[_Mapping[str, _elementary_types_pb2.ValueList]] = ..., row_labels: _Optional[_Iterable[str]] = ...) -> None: ...

class StringTable(_message.Message):
    __slots__ = ("column_value_map", "row_labels")
    class ColumnValueMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _elementary_types_pb2.StringList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_elementary_types_pb2.StringList, _Mapping]] = ...) -> None: ...
    COLUMN_VALUE_MAP_FIELD_NUMBER: _ClassVar[int]
    ROW_LABELS_FIELD_NUMBER: _ClassVar[int]
    column_value_map: _containers.MessageMap[str, _elementary_types_pb2.StringList]
    row_labels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, column_value_map: _Optional[_Mapping[str, _elementary_types_pb2.StringList]] = ..., row_labels: _Optional[_Iterable[str]] = ...) -> None: ...

class BoolList(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, values: _Optional[_Iterable[bool]] = ...) -> None: ...

class SplitDataRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "model_id", "input_spec", "include_labels", "include_extra_data", "exclude_feature_values", "pre_processed_data_required", "get_post_processed_data", "include_system_data")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_LABELS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_EXTRA_DATA_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FEATURE_VALUES_FIELD_NUMBER: _ClassVar[int]
    PRE_PROCESSED_DATA_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    GET_POST_PROCESSED_DATA_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SYSTEM_DATA_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    model_id: str
    input_spec: ModelInputSpec
    include_labels: bool
    include_extra_data: bool
    exclude_feature_values: bool
    pre_processed_data_required: bool
    get_post_processed_data: bool
    include_system_data: bool
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., model_id: _Optional[str] = ..., input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., include_labels: bool = ..., include_extra_data: bool = ..., exclude_feature_values: bool = ..., pre_processed_data_required: bool = ..., get_post_processed_data: bool = ..., include_system_data: bool = ...) -> None: ...

class SplitDataResponse(_message.Message):
    __slots__ = ("split_metadata", "split_data", "split_extra_data", "split_labels", "pending_operations")
    SPLIT_METADATA_FIELD_NUMBER: _ClassVar[int]
    SPLIT_DATA_FIELD_NUMBER: _ClassVar[int]
    SPLIT_EXTRA_DATA_FIELD_NUMBER: _ClassVar[int]
    SPLIT_LABELS_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    split_metadata: SplitMetaData
    split_data: ValueTable
    split_extra_data: ValueTable
    split_labels: ValueTable
    pending_operations: PendingOperations
    def __init__(self, split_metadata: _Optional[_Union[SplitMetaData, _Mapping]] = ..., split_data: _Optional[_Union[ValueTable, _Mapping]] = ..., split_extra_data: _Optional[_Union[ValueTable, _Mapping]] = ..., split_labels: _Optional[_Union[ValueTable, _Mapping]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ...) -> None: ...

class SplitMetadataRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "split_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    split_id: str
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., split_id: _Optional[str] = ...) -> None: ...

class SplitMetadataResponse(_message.Message):
    __slots__ = ("split_metadata",)
    SPLIT_METADATA_FIELD_NUMBER: _ClassVar[int]
    split_metadata: SplitMetaData
    def __init__(self, split_metadata: _Optional[_Union[SplitMetaData, _Mapping]] = ...) -> None: ...

class ModelPredictionsRequest(_message.Message):
    __slots__ = ("model_id", "input_spec", "prediction_options", "include_system_data")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SYSTEM_DATA_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    input_spec: ModelInputSpec
    prediction_options: _common_pb2.PredictionOptions
    include_system_data: bool
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., prediction_options: _Optional[_Union[_common_pb2.PredictionOptions, _Mapping]] = ..., include_system_data: bool = ...) -> None: ...

class ModelPredictionsResponse(_message.Message):
    __slots__ = ("predictions", "system_data", "quantity_of_interest", "pending_operations")
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_DATA_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_OF_INTEREST_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    predictions: ValueTable
    system_data: StringTable
    quantity_of_interest: _qoi_pb2.QuantityOfInterest
    pending_operations: PendingOperations
    def __init__(self, predictions: _Optional[_Union[ValueTable, _Mapping]] = ..., system_data: _Optional[_Union[StringTable, _Mapping]] = ..., quantity_of_interest: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ...) -> None: ...

class ModelTokensRequest(_message.Message):
    __slots__ = ("model_id", "input_spec", "include_system_data")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SYSTEM_DATA_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    input_spec: ModelInputSpec
    include_system_data: bool
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., include_system_data: bool = ...) -> None: ...

class ModelTokensResponse(_message.Message):
    __slots__ = ("tokens", "system_data")
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_DATA_FIELD_NUMBER: _ClassVar[int]
    tokens: ValueTable
    system_data: StringTable
    def __init__(self, tokens: _Optional[_Union[ValueTable, _Mapping]] = ..., system_data: _Optional[_Union[StringTable, _Mapping]] = ...) -> None: ...

class ModelEmbeddingsRequest(_message.Message):
    __slots__ = ("model_id", "input_spec", "include_system_data")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SYSTEM_DATA_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    input_spec: ModelInputSpec
    include_system_data: bool
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., include_system_data: bool = ...) -> None: ...

class ModelEmbeddingsResponse(_message.Message):
    __slots__ = ("embeddings", "system_data")
    EMBEDDINGS_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_DATA_FIELD_NUMBER: _ClassVar[int]
    embeddings: ValueTable
    system_data: StringTable
    def __init__(self, embeddings: _Optional[_Union[ValueTable, _Mapping]] = ..., system_data: _Optional[_Union[StringTable, _Mapping]] = ...) -> None: ...

class ModelInfluencesRequest(_message.Message):
    __slots__ = ("model_id", "input_spec", "feature_influence_options", "include_system_data", "include_global_aggregation", "exclude_pointwise_influences", "dont_compute")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    FEATURE_INFLUENCE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SYSTEM_DATA_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_GLOBAL_AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_POINTWISE_INFLUENCES_FIELD_NUMBER: _ClassVar[int]
    DONT_COMPUTE_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    input_spec: ModelInputSpec
    feature_influence_options: _common_pb2.FeatureInfluenceOptions
    include_system_data: bool
    include_global_aggregation: bool
    exclude_pointwise_influences: bool
    dont_compute: bool
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., feature_influence_options: _Optional[_Union[_common_pb2.FeatureInfluenceOptions, _Mapping]] = ..., include_system_data: bool = ..., include_global_aggregation: bool = ..., exclude_pointwise_influences: bool = ..., dont_compute: bool = ...) -> None: ...

class ModelInfluencesResponse(_message.Message):
    __slots__ = ("influences", "global_influences", "system_data", "quantity_of_interest", "ordered_column_names", "pending_operations", "explanation_algorithm_type")
    INFLUENCES_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_INFLUENCES_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_DATA_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_OF_INTEREST_FIELD_NUMBER: _ClassVar[int]
    ORDERED_COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    EXPLANATION_ALGORITHM_TYPE_FIELD_NUMBER: _ClassVar[int]
    influences: FloatTable
    global_influences: FloatTable
    system_data: StringTable
    quantity_of_interest: _qoi_pb2.QuantityOfInterest
    ordered_column_names: _elementary_types_pb2.StringList
    pending_operations: PendingOperations
    explanation_algorithm_type: _qoi_pb2.ExplanationAlgorithmType
    def __init__(self, influences: _Optional[_Union[FloatTable, _Mapping]] = ..., global_influences: _Optional[_Union[FloatTable, _Mapping]] = ..., system_data: _Optional[_Union[StringTable, _Mapping]] = ..., quantity_of_interest: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., ordered_column_names: _Optional[_Union[_elementary_types_pb2.StringList, _Mapping]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ..., explanation_algorithm_type: _Optional[_Union[_qoi_pb2.ExplanationAlgorithmType, str]] = ...) -> None: ...

class ModelNLPInfluencesRequest(_message.Message):
    __slots__ = ("model_id", "input_spec", "feature_influence_options", "include_system_data")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    FEATURE_INFLUENCE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SYSTEM_DATA_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    input_spec: ModelInputSpec
    feature_influence_options: _common_pb2.FeatureInfluenceOptions
    include_system_data: bool
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., feature_influence_options: _Optional[_Union[_common_pb2.FeatureInfluenceOptions, _Mapping]] = ..., include_system_data: bool = ...) -> None: ...

class ModelNLPInfluencesResponse(_message.Message):
    __slots__ = ("influences", "system_data", "quantity_of_interest", "pending_operations", "explanation_algorithm_type")
    INFLUENCES_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_DATA_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_OF_INTEREST_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    EXPLANATION_ALGORITHM_TYPE_FIELD_NUMBER: _ClassVar[int]
    influences: ValueTable
    system_data: StringTable
    quantity_of_interest: _qoi_pb2.QuantityOfInterest
    pending_operations: PendingOperations
    explanation_algorithm_type: _qoi_pb2.ExplanationAlgorithmType
    def __init__(self, influences: _Optional[_Union[ValueTable, _Mapping]] = ..., system_data: _Optional[_Union[StringTable, _Mapping]] = ..., quantity_of_interest: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ..., explanation_algorithm_type: _Optional[_Union[_qoi_pb2.ExplanationAlgorithmType, str]] = ...) -> None: ...

class TokensOccurrencesRequest(_message.Message):
    __slots__ = ("model_id", "input_spec", "search_tokens", "compute_record_metrics", "get_predictions_labels")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_RECORD_METRICS_FIELD_NUMBER: _ClassVar[int]
    GET_PREDICTIONS_LABELS_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    input_spec: ModelInputSpec
    search_tokens: _containers.RepeatedScalarFieldContainer[str]
    compute_record_metrics: bool
    get_predictions_labels: bool
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., search_tokens: _Optional[_Iterable[str]] = ..., compute_record_metrics: bool = ..., get_predictions_labels: bool = ...) -> None: ...

class TokensOccurrencesResponse(_message.Message):
    __slots__ = ("token_occurrences",)
    TOKEN_OCCURRENCES_FIELD_NUMBER: _ClassVar[int]
    token_occurrences: ValueTable
    def __init__(self, token_occurrences: _Optional[_Union[ValueTable, _Mapping]] = ...) -> None: ...

class GlobalTokensDataSummaryRequest(_message.Message):
    __slots__ = ("model_id", "input_spec", "search_tokens", "compute_metrics")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_METRICS_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    input_spec: ModelInputSpec
    search_tokens: _containers.RepeatedScalarFieldContainer[str]
    compute_metrics: bool
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., search_tokens: _Optional[_Iterable[str]] = ..., compute_metrics: bool = ...) -> None: ...

class GlobalTokensDataSummaryResponse(_message.Message):
    __slots__ = ("tokens_data_summary",)
    TOKENS_DATA_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    tokens_data_summary: ValueTable
    def __init__(self, tokens_data_summary: _Optional[_Union[ValueTable, _Mapping]] = ...) -> None: ...

class NLPRecordDataSummaryRequest(_message.Message):
    __slots__ = ("model_id", "input_spec", "record_id")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    RECORD_ID_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    input_spec: ModelInputSpec
    record_id: str
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., record_id: _Optional[str] = ...) -> None: ...

class NLPRecordDataSummaryResponse(_message.Message):
    __slots__ = ("min_influence", "max_influence", "q1_influence", "q3_influence", "median_influence", "n_tokens")
    MIN_INFLUENCE_FIELD_NUMBER: _ClassVar[int]
    MAX_INFLUENCE_FIELD_NUMBER: _ClassVar[int]
    Q1_INFLUENCE_FIELD_NUMBER: _ClassVar[int]
    Q3_INFLUENCE_FIELD_NUMBER: _ClassVar[int]
    MEDIAN_INFLUENCE_FIELD_NUMBER: _ClassVar[int]
    N_TOKENS_FIELD_NUMBER: _ClassVar[int]
    min_influence: float
    max_influence: float
    q1_influence: float
    q3_influence: float
    median_influence: float
    n_tokens: int
    def __init__(self, min_influence: _Optional[float] = ..., max_influence: _Optional[float] = ..., q1_influence: _Optional[float] = ..., q3_influence: _Optional[float] = ..., median_influence: _Optional[float] = ..., n_tokens: _Optional[int] = ...) -> None: ...

class EmbeddingDrift(_message.Message):
    __slots__ = ("distance_type", "distance_value")
    DISTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_VALUE_FIELD_NUMBER: _ClassVar[int]
    distance_type: _distance_pb2.DistanceType
    distance_value: float
    def __init__(self, distance_type: _Optional[_Union[_distance_pb2.DistanceType, str]] = ..., distance_value: _Optional[float] = ...) -> None: ...

class EmbeddingDriftRequest(_message.Message):
    __slots__ = ("model_id", "input_spec1", "input_spec2", "distances")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC1_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC2_FIELD_NUMBER: _ClassVar[int]
    DISTANCES_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    input_spec1: ModelInputSpec
    input_spec2: ModelInputSpec
    distances: _containers.RepeatedScalarFieldContainer[_distance_pb2.DistanceType]
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., input_spec1: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., input_spec2: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., distances: _Optional[_Iterable[_Union[_distance_pb2.DistanceType, str]]] = ...) -> None: ...

class EmbeddingDriftResponse(_message.Message):
    __slots__ = ("drifts",)
    DRIFTS_FIELD_NUMBER: _ClassVar[int]
    drifts: _containers.RepeatedCompositeFieldContainer[EmbeddingDrift]
    def __init__(self, drifts: _Optional[_Iterable[_Union[EmbeddingDrift, _Mapping]]] = ...) -> None: ...

class TraceFeedbackFunctionAggregate(_message.Message):
    __slots__ = ("function_id", "average_score", "num_passed", "num_failed", "num_total")
    FUNCTION_ID_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_SCORE_FIELD_NUMBER: _ClassVar[int]
    NUM_PASSED_FIELD_NUMBER: _ClassVar[int]
    NUM_FAILED_FIELD_NUMBER: _ClassVar[int]
    NUM_TOTAL_FIELD_NUMBER: _ClassVar[int]
    function_id: str
    average_score: float
    num_passed: int
    num_failed: int
    num_total: int
    def __init__(self, function_id: _Optional[str] = ..., average_score: _Optional[float] = ..., num_passed: _Optional[int] = ..., num_failed: _Optional[int] = ..., num_total: _Optional[int] = ...) -> None: ...

class FeedbackFunctionEval(_message.Message):
    __slots__ = ("function_id", "score", "passed", "args", "metadata")
    class ArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _any_pb2.Any
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _any_pb2.Any
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
    FUNCTION_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    PASSED_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    function_id: str
    score: float
    passed: bool
    args: _containers.MessageMap[str, _any_pb2.Any]
    metadata: _containers.MessageMap[str, _any_pb2.Any]
    def __init__(self, function_id: _Optional[str] = ..., score: _Optional[float] = ..., passed: bool = ..., args: _Optional[_Mapping[str, _any_pb2.Any]] = ..., metadata: _Optional[_Mapping[str, _any_pb2.Any]] = ...) -> None: ...

class TraceData(_message.Message):
    __slots__ = ("id", "created_on", "feedback_function_aggregates", "application_input", "application_output", "prompt", "latency", "cost", "num_tokens", "span_data", "start_time", "end_time")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FUNCTION_AGGREGATES_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_INPUT_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    COST_FIELD_NUMBER: _ClassVar[int]
    NUM_TOKENS_FIELD_NUMBER: _ClassVar[int]
    SPAN_DATA_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    id: str
    created_on: _timestamp_pb2.Timestamp
    feedback_function_aggregates: _containers.RepeatedCompositeFieldContainer[TraceFeedbackFunctionAggregate]
    application_input: str
    application_output: str
    prompt: str
    latency: float
    cost: float
    num_tokens: int
    span_data: _struct_pb2.Value
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., created_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., feedback_function_aggregates: _Optional[_Iterable[_Union[TraceFeedbackFunctionAggregate, _Mapping]]] = ..., application_input: _Optional[str] = ..., application_output: _Optional[str] = ..., prompt: _Optional[str] = ..., latency: _Optional[float] = ..., cost: _Optional[float] = ..., num_tokens: _Optional[int] = ..., span_data: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TraceDataRequest(_message.Message):
    __slots__ = ("project_id", "model_id", "data_split_id", "include_feedback_aggregations", "trace_id", "include_spans")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_FEEDBACK_AGGREGATIONS_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SPANS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_id: str
    data_split_id: str
    include_feedback_aggregations: bool
    trace_id: str
    include_spans: bool
    def __init__(self, project_id: _Optional[str] = ..., model_id: _Optional[str] = ..., data_split_id: _Optional[str] = ..., include_feedback_aggregations: bool = ..., trace_id: _Optional[str] = ..., include_spans: bool = ...) -> None: ...

class TraceDataResponse(_message.Message):
    __slots__ = ("traces",)
    TRACES_FIELD_NUMBER: _ClassVar[int]
    traces: _containers.RepeatedCompositeFieldContainer[TraceData]
    def __init__(self, traces: _Optional[_Iterable[_Union[TraceData, _Mapping]]] = ...) -> None: ...

class FeedbackFunctionEvalRequest(_message.Message):
    __slots__ = ("project_id", "model_id", "data_split_id", "trace_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_id: str
    data_split_id: str
    trace_id: str
    def __init__(self, project_id: _Optional[str] = ..., model_id: _Optional[str] = ..., data_split_id: _Optional[str] = ..., trace_id: _Optional[str] = ...) -> None: ...

class FeedbackFunctionEvalsResponse(_message.Message):
    __slots__ = ("feedback_function_evals",)
    FEEDBACK_FUNCTION_EVALS_FIELD_NUMBER: _ClassVar[int]
    feedback_function_evals: _containers.RepeatedCompositeFieldContainer[FeedbackFunctionEval]
    def __init__(self, feedback_function_evals: _Optional[_Iterable[_Union[FeedbackFunctionEval, _Mapping]]] = ...) -> None: ...

class FeedbackFunctionMetadataRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class FeedbackFunctionMetadataResponse(_message.Message):
    __slots__ = ("feedback_function_metadata",)
    FEEDBACK_FUNCTION_METADATA_FIELD_NUMBER: _ClassVar[int]
    feedback_function_metadata: _containers.RepeatedCompositeFieldContainer[_metadata_message_types_pb2.FeedbackFunctionMetadata]
    def __init__(self, feedback_function_metadata: _Optional[_Iterable[_Union[_metadata_message_types_pb2.FeedbackFunctionMetadata, _Mapping]]] = ...) -> None: ...

class ReliabilityRequest(_message.Message):
    __slots__ = ("model_id", "model_input_spec", "score_type", "reliability_metric_types")
    class ReliabilityMetricType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[ReliabilityRequest.ReliabilityMetricType]
        CALIBRATION: _ClassVar[ReliabilityRequest.ReliabilityMetricType]
        QII_L2: _ClassVar[ReliabilityRequest.ReliabilityMetricType]
        QII_CLIPPING: _ClassVar[ReliabilityRequest.ReliabilityMetricType]
    UNKNOWN: ReliabilityRequest.ReliabilityMetricType
    CALIBRATION: ReliabilityRequest.ReliabilityMetricType
    QII_L2: ReliabilityRequest.ReliabilityMetricType
    QII_CLIPPING: ReliabilityRequest.ReliabilityMetricType
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RELIABILITY_METRIC_TYPES_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    model_input_spec: ModelInputSpec
    score_type: _qoi_pb2.QuantityOfInterest
    reliability_metric_types: _containers.RepeatedScalarFieldContainer[ReliabilityRequest.ReliabilityMetricType]
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., model_input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., reliability_metric_types: _Optional[_Iterable[_Union[ReliabilityRequest.ReliabilityMetricType, str]]] = ...) -> None: ...

class ReliabilityResponse(_message.Message):
    __slots__ = ("reliabilities", "pending_operations")
    RELIABILITIES_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    reliabilities: _containers.RepeatedCompositeFieldContainer[_elementary_types_pb2.FloatList]
    pending_operations: PendingOperations
    def __init__(self, reliabilities: _Optional[_Iterable[_Union[_elementary_types_pb2.FloatList, _Mapping]]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ...) -> None: ...

class FeatureAssociationsGraphRequest(_message.Message):
    __slots__ = ("model_id", "model_input_spec")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    model_input_spec: ModelInputSpec
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., model_input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ...) -> None: ...

class FeatureAssociationsGraphResponse(_message.Message):
    __slots__ = ("feature_associations", "visualization_node_placements", "pending_operations")
    FEATURE_ASSOCIATIONS_FIELD_NUMBER: _ClassVar[int]
    VISUALIZATION_NODE_PLACEMENTS_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    feature_associations: FloatTable
    visualization_node_placements: FloatTable
    pending_operations: PendingOperations
    def __init__(self, feature_associations: _Optional[_Union[FloatTable, _Mapping]] = ..., visualization_node_placements: _Optional[_Union[FloatTable, _Mapping]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ...) -> None: ...

class AccuracyRequest(_message.Message):
    __slots__ = ("model_id", "model_input_spec", "accuracy_types", "include_precision_recall_curve", "include_roc_curve", "include_confusion_matrix", "dont_compute_predictions", "estimate_type", "baseline_input_spec", "ignore_cache")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_TYPES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PRECISION_RECALL_CURVE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ROC_CURVE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CONFUSION_MATRIX_FIELD_NUMBER: _ClassVar[int]
    DONT_COMPUTE_PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    ESTIMATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    BASELINE_INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    IGNORE_CACHE_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    model_input_spec: ModelInputSpec
    accuracy_types: _containers.RepeatedScalarFieldContainer[_accuracy_pb2.AccuracyType.Type]
    include_precision_recall_curve: bool
    include_roc_curve: bool
    include_confusion_matrix: bool
    dont_compute_predictions: bool
    estimate_type: _accuracy_pb2.EstimateType
    baseline_input_spec: ModelInputSpec
    ignore_cache: bool
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., model_input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., accuracy_types: _Optional[_Iterable[_Union[_accuracy_pb2.AccuracyType.Type, str]]] = ..., include_precision_recall_curve: bool = ..., include_roc_curve: bool = ..., include_confusion_matrix: bool = ..., dont_compute_predictions: bool = ..., estimate_type: _Optional[_Union[_accuracy_pb2.EstimateType, str]] = ..., baseline_input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., ignore_cache: bool = ...) -> None: ...

class AccuracyRequestMapping(_message.Message):
    __slots__ = ("model_id", "model_input_spec", "estimate_type", "baseline_input_spec", "include_precision_recall_curve", "include_roc_curve", "include_confusion_matrix", "include_compute_record_count")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    ESTIMATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    BASELINE_INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PRECISION_RECALL_CURVE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ROC_CURVE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CONFUSION_MATRIX_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_COMPUTE_RECORD_COUNT_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    model_input_spec: ModelInputSpec
    estimate_type: _accuracy_pb2.EstimateType
    baseline_input_spec: ModelInputSpec
    include_precision_recall_curve: bool
    include_roc_curve: bool
    include_confusion_matrix: bool
    include_compute_record_count: bool
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., model_input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., estimate_type: _Optional[_Union[_accuracy_pb2.EstimateType, str]] = ..., baseline_input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., include_precision_recall_curve: bool = ..., include_roc_curve: bool = ..., include_confusion_matrix: bool = ..., include_compute_record_count: bool = ...) -> None: ...

class BatchAccuracyRequest(_message.Message):
    __slots__ = ("project_id", "model_data", "accuracy_types", "dont_compute_predictions", "ignore_cache")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_DATA_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_TYPES_FIELD_NUMBER: _ClassVar[int]
    DONT_COMPUTE_PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    IGNORE_CACHE_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_data: _containers.RepeatedCompositeFieldContainer[AccuracyRequestMapping]
    accuracy_types: _containers.RepeatedScalarFieldContainer[_accuracy_pb2.AccuracyType.Type]
    dont_compute_predictions: bool
    ignore_cache: bool
    def __init__(self, project_id: _Optional[str] = ..., model_data: _Optional[_Iterable[_Union[AccuracyRequestMapping, _Mapping]]] = ..., accuracy_types: _Optional[_Iterable[_Union[_accuracy_pb2.AccuracyType.Type, str]]] = ..., dont_compute_predictions: bool = ..., ignore_cache: bool = ...) -> None: ...

class AccuracyResponse(_message.Message):
    __slots__ = ("accuracies", "accuracies_map", "accuracies_result_map", "pending_operations", "precision_recall_curve", "roc_curve", "confusion_matrix", "is_estimate", "estimate_confidence")
    class AccuraciesMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class AccuraciesResultMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: _accuracy_pb2.AccuracyResult
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[_accuracy_pb2.AccuracyResult, _Mapping]] = ...) -> None: ...
    ACCURACIES_FIELD_NUMBER: _ClassVar[int]
    ACCURACIES_MAP_FIELD_NUMBER: _ClassVar[int]
    ACCURACIES_RESULT_MAP_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    PRECISION_RECALL_CURVE_FIELD_NUMBER: _ClassVar[int]
    ROC_CURVE_FIELD_NUMBER: _ClassVar[int]
    CONFUSION_MATRIX_FIELD_NUMBER: _ClassVar[int]
    IS_ESTIMATE_FIELD_NUMBER: _ClassVar[int]
    ESTIMATE_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    accuracies: _containers.RepeatedScalarFieldContainer[float]
    accuracies_map: _containers.ScalarMap[int, float]
    accuracies_result_map: _containers.MessageMap[int, _accuracy_pb2.AccuracyResult]
    pending_operations: PendingOperations
    precision_recall_curve: _accuracy_pb2.PrecisionRecallCurve
    roc_curve: _accuracy_pb2.RocCurve
    confusion_matrix: _accuracy_pb2.ConfusionMatrix
    is_estimate: bool
    estimate_confidence: _accuracy_pb2.AccuracyEstimateConfidence.Confidence
    def __init__(self, accuracies: _Optional[_Iterable[float]] = ..., accuracies_map: _Optional[_Mapping[int, float]] = ..., accuracies_result_map: _Optional[_Mapping[int, _accuracy_pb2.AccuracyResult]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ..., precision_recall_curve: _Optional[_Union[_accuracy_pb2.PrecisionRecallCurve, _Mapping]] = ..., roc_curve: _Optional[_Union[_accuracy_pb2.RocCurve, _Mapping]] = ..., confusion_matrix: _Optional[_Union[_accuracy_pb2.ConfusionMatrix, _Mapping]] = ..., is_estimate: bool = ..., estimate_confidence: _Optional[_Union[_accuracy_pb2.AccuracyEstimateConfidence.Confidence, str]] = ...) -> None: ...

class AccuracyResponseMapping(_message.Message):
    __slots__ = ("model_id", "model_input_spec", "accuracies_result_map", "pending_operations", "is_estimate", "estimate_confidence", "precision_recall_curve", "roc_curve", "confusion_matrix")
    class AccuraciesResultMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: _accuracy_pb2.AccuracyResult
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[_accuracy_pb2.AccuracyResult, _Mapping]] = ...) -> None: ...
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    ACCURACIES_RESULT_MAP_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    IS_ESTIMATE_FIELD_NUMBER: _ClassVar[int]
    ESTIMATE_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    PRECISION_RECALL_CURVE_FIELD_NUMBER: _ClassVar[int]
    ROC_CURVE_FIELD_NUMBER: _ClassVar[int]
    CONFUSION_MATRIX_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    model_input_spec: ModelInputSpec
    accuracies_result_map: _containers.MessageMap[int, _accuracy_pb2.AccuracyResult]
    pending_operations: PendingOperations
    is_estimate: bool
    estimate_confidence: _accuracy_pb2.AccuracyEstimateConfidence.Confidence
    precision_recall_curve: _accuracy_pb2.PrecisionRecallCurve
    roc_curve: _accuracy_pb2.RocCurve
    confusion_matrix: _accuracy_pb2.ConfusionMatrix
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., model_input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., accuracies_result_map: _Optional[_Mapping[int, _accuracy_pb2.AccuracyResult]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ..., is_estimate: bool = ..., estimate_confidence: _Optional[_Union[_accuracy_pb2.AccuracyEstimateConfidence.Confidence, str]] = ..., precision_recall_curve: _Optional[_Union[_accuracy_pb2.PrecisionRecallCurve, _Mapping]] = ..., roc_curve: _Optional[_Union[_accuracy_pb2.RocCurve, _Mapping]] = ..., confusion_matrix: _Optional[_Union[_accuracy_pb2.ConfusionMatrix, _Mapping]] = ...) -> None: ...

class BatchAccuracyResponse(_message.Message):
    __slots__ = ("model_accuracies",)
    MODEL_ACCURACIES_FIELD_NUMBER: _ClassVar[int]
    model_accuracies: _containers.RepeatedCompositeFieldContainer[AccuracyResponseMapping]
    def __init__(self, model_accuracies: _Optional[_Iterable[_Union[AccuracyResponseMapping, _Mapping]]] = ...) -> None: ...

class BucketizedStatsType(_message.Message):
    __slots__ = ()
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[BucketizedStatsType.Type]
        GROUND_TRUTH: _ClassVar[BucketizedStatsType.Type]
        CLASSIFICATION_ERROR: _ClassVar[BucketizedStatsType.Type]
        LOG_LOSS: _ClassVar[BucketizedStatsType.Type]
        L1_ERROR: _ClassVar[BucketizedStatsType.Type]
        L2_ERROR: _ClassVar[BucketizedStatsType.Type]
    UNKNOWN: BucketizedStatsType.Type
    GROUND_TRUTH: BucketizedStatsType.Type
    CLASSIFICATION_ERROR: BucketizedStatsType.Type
    LOG_LOSS: BucketizedStatsType.Type
    L1_ERROR: BucketizedStatsType.Type
    L2_ERROR: BucketizedStatsType.Type
    def __init__(self) -> None: ...

class NumericalBucketParams(_message.Message):
    __slots__ = ("num_buckets", "lower_bound", "upper_bound")
    NUM_BUCKETS_FIELD_NUMBER: _ClassVar[int]
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    num_buckets: int
    lower_bound: float
    upper_bound: float
    def __init__(self, num_buckets: _Optional[int] = ..., lower_bound: _Optional[float] = ..., upper_bound: _Optional[float] = ...) -> None: ...

class CategoricalBucketParams(_message.Message):
    __slots__ = ("buckets", "values")
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    buckets: _containers.RepeatedScalarFieldContainer[str]
    values: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Value]
    def __init__(self, buckets: _Optional[_Iterable[str]] = ..., values: _Optional[_Iterable[_Union[_struct_pb2.Value, _Mapping]]] = ...) -> None: ...

class GetBucketizedStatsRequest(_message.Message):
    __slots__ = ("model_id", "model_input_spec", "feature", "type", "ignore_cache")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IGNORE_CACHE_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    model_input_spec: ModelInputSpec
    feature: str
    type: BucketizedStatsType.Type
    ignore_cache: bool
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., model_input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., feature: _Optional[str] = ..., type: _Optional[_Union[BucketizedStatsType.Type, str]] = ..., ignore_cache: bool = ...) -> None: ...

class GetBucketizedStatsResponse(_message.Message):
    __slots__ = ("bucket_summary", "special_value_summary", "pending_operations")
    BUCKET_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_VALUE_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    bucket_summary: FloatTable
    special_value_summary: FloatTable
    pending_operations: PendingOperations
    def __init__(self, bucket_summary: _Optional[_Union[FloatTable, _Mapping]] = ..., special_value_summary: _Optional[_Union[FloatTable, _Mapping]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ...) -> None: ...

class HighlightDataRequest(_message.Message):
    __slots__ = ("model_id", "model_input_spec", "highlight")
    class HighlightType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NONE: _ClassVar[HighlightDataRequest.HighlightType]
        OUTLIERS: _ClassVar[HighlightDataRequest.HighlightType]
        GROUND_TRUTH_COMPARISON: _ClassVar[HighlightDataRequest.HighlightType]
        OVERFITTING_DENSITY_DIAGNOSTIC: _ClassVar[HighlightDataRequest.HighlightType]
    NONE: HighlightDataRequest.HighlightType
    OUTLIERS: HighlightDataRequest.HighlightType
    GROUND_TRUTH_COMPARISON: HighlightDataRequest.HighlightType
    OVERFITTING_DENSITY_DIAGNOSTIC: HighlightDataRequest.HighlightType
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    HIGHLIGHT_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    model_input_spec: ModelInputSpec
    highlight: HighlightDataRequest.HighlightType
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., model_input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., highlight: _Optional[_Union[HighlightDataRequest.HighlightType, str]] = ...) -> None: ...

class HighlightDataResponse(_message.Message):
    __slots__ = ("string_table", "pending_operations")
    STRING_TABLE_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    string_table: StringTable
    pending_operations: PendingOperations
    def __init__(self, string_table: _Optional[_Union[StringTable, _Mapping]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ...) -> None: ...

class SegmentationRequest(_message.Message):
    __slots__ = ("model_id", "model_input_spec", "segmentation_type", "visualization_type", "num_clusters", "top_n_influence_approximators")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    SEGMENTATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    VISUALIZATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUM_CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    TOP_N_INFLUENCE_APPROXIMATORS_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    model_input_spec: ModelInputSpec
    segmentation_type: SegmentationOptions.SegmentationMethod
    visualization_type: ReduceDimensionOptions.ReduceDimensionMethod
    num_clusters: int
    top_n_influence_approximators: int
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., model_input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., segmentation_type: _Optional[_Union[SegmentationOptions.SegmentationMethod, str]] = ..., visualization_type: _Optional[_Union[ReduceDimensionOptions.ReduceDimensionMethod, str]] = ..., num_clusters: _Optional[int] = ..., top_n_influence_approximators: _Optional[int] = ...) -> None: ...

class SegmentationOptions(_message.Message):
    __slots__ = ()
    class SegmentationMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SEG_NONE: _ClassVar[SegmentationOptions.SegmentationMethod]
        SEG_AGGLOMERATIVE: _ClassVar[SegmentationOptions.SegmentationMethod]
        SEG_KMEANS: _ClassVar[SegmentationOptions.SegmentationMethod]
        SEG_DBSCAN: _ClassVar[SegmentationOptions.SegmentationMethod]
        SEG_TSNE: _ClassVar[SegmentationOptions.SegmentationMethod]
        SEG_PCA: _ClassVar[SegmentationOptions.SegmentationMethod]
    SEG_NONE: SegmentationOptions.SegmentationMethod
    SEG_AGGLOMERATIVE: SegmentationOptions.SegmentationMethod
    SEG_KMEANS: SegmentationOptions.SegmentationMethod
    SEG_DBSCAN: SegmentationOptions.SegmentationMethod
    SEG_TSNE: SegmentationOptions.SegmentationMethod
    SEG_PCA: SegmentationOptions.SegmentationMethod
    def __init__(self) -> None: ...

class SegmentationResponse(_message.Message):
    __slots__ = ("cluster_names", "prediction_scores", "feature_cluster_descriptors", "feature_cluster_descriptors_short", "influence_cluster_descriptors", "influence_cluster_descriptors_short", "coordinates_list", "segment_info", "pending_operations")
    class FeatureClusterDescriptorsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class FeatureClusterDescriptorsShortEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class InfluenceClusterDescriptorsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class InfluenceClusterDescriptorsShortEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class SegmentInfoEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: SegmentInfo
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[SegmentInfo, _Mapping]] = ...) -> None: ...
    CLUSTER_NAMES_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_SCORES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_CLUSTER_DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_CLUSTER_DESCRIPTORS_SHORT_FIELD_NUMBER: _ClassVar[int]
    INFLUENCE_CLUSTER_DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    INFLUENCE_CLUSTER_DESCRIPTORS_SHORT_FIELD_NUMBER: _ClassVar[int]
    COORDINATES_LIST_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_INFO_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    cluster_names: _containers.RepeatedScalarFieldContainer[str]
    prediction_scores: _containers.RepeatedScalarFieldContainer[float]
    feature_cluster_descriptors: _containers.ScalarMap[str, str]
    feature_cluster_descriptors_short: _containers.ScalarMap[str, str]
    influence_cluster_descriptors: _containers.ScalarMap[str, str]
    influence_cluster_descriptors_short: _containers.ScalarMap[str, str]
    coordinates_list: CoordinatesList
    segment_info: _containers.MessageMap[str, SegmentInfo]
    pending_operations: PendingOperations
    def __init__(self, cluster_names: _Optional[_Iterable[str]] = ..., prediction_scores: _Optional[_Iterable[float]] = ..., feature_cluster_descriptors: _Optional[_Mapping[str, str]] = ..., feature_cluster_descriptors_short: _Optional[_Mapping[str, str]] = ..., influence_cluster_descriptors: _Optional[_Mapping[str, str]] = ..., influence_cluster_descriptors_short: _Optional[_Mapping[str, str]] = ..., coordinates_list: _Optional[_Union[CoordinatesList, _Mapping]] = ..., segment_info: _Optional[_Mapping[str, SegmentInfo]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ...) -> None: ...

class SegmentInfo(_message.Message):
    __slots__ = ("feature_segments", "influence_segments", "feature_segment_approximation_accuracy", "influence_segment_approximation_accuracy")
    FEATURE_SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    INFLUENCE_SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SEGMENT_APPROXIMATION_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    INFLUENCE_SEGMENT_APPROXIMATION_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    feature_segments: SegmentDescriptors
    influence_segments: SegmentDescriptors
    feature_segment_approximation_accuracy: float
    influence_segment_approximation_accuracy: float
    def __init__(self, feature_segments: _Optional[_Union[SegmentDescriptors, _Mapping]] = ..., influence_segments: _Optional[_Union[SegmentDescriptors, _Mapping]] = ..., feature_segment_approximation_accuracy: _Optional[float] = ..., influence_segment_approximation_accuracy: _Optional[float] = ...) -> None: ...

class SegmentDescriptors(_message.Message):
    __slots__ = ("subsegment_list",)
    SUBSEGMENT_LIST_FIELD_NUMBER: _ClassVar[int]
    subsegment_list: _containers.RepeatedCompositeFieldContainer[SubsegmentDescriptors]
    def __init__(self, subsegment_list: _Optional[_Iterable[_Union[SubsegmentDescriptors, _Mapping]]] = ...) -> None: ...

class SubsegmentDescriptors(_message.Message):
    __slots__ = ("id", "predicates")
    ID_FIELD_NUMBER: _ClassVar[int]
    PREDICATES_FIELD_NUMBER: _ClassVar[int]
    id: str
    predicates: _containers.RepeatedCompositeFieldContainer[Predicate]
    def __init__(self, id: _Optional[str] = ..., predicates: _Optional[_Iterable[_Union[Predicate, _Mapping]]] = ...) -> None: ...

class UpdateManualSegmentationRequest(_message.Message):
    __slots__ = ("segmentation", "segmentation_id_to_delete", "project_id")
    SEGMENTATION_FIELD_NUMBER: _ClassVar[int]
    SEGMENTATION_ID_TO_DELETE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    segmentation: _segment_pb2.Segmentation
    segmentation_id_to_delete: str
    project_id: str
    def __init__(self, segmentation: _Optional[_Union[_segment_pb2.Segmentation, _Mapping]] = ..., segmentation_id_to_delete: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...

class UpdateManualSegmentationResponse(_message.Message):
    __slots__ = ("segmentation",)
    SEGMENTATION_FIELD_NUMBER: _ClassVar[int]
    segmentation: _segment_pb2.Segmentation
    def __init__(self, segmentation: _Optional[_Union[_segment_pb2.Segmentation, _Mapping]] = ...) -> None: ...

class GetManualSegmentationRequest(_message.Message):
    __slots__ = ("project_id", "segmentation_id", "include_unaccepted_interesting_segments")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENTATION_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_UNACCEPTED_INTERESTING_SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    segmentation_id: str
    include_unaccepted_interesting_segments: bool
    def __init__(self, project_id: _Optional[str] = ..., segmentation_id: _Optional[str] = ..., include_unaccepted_interesting_segments: bool = ...) -> None: ...

class GetManualSegmentationResponse(_message.Message):
    __slots__ = ("segmentations",)
    SEGMENTATIONS_FIELD_NUMBER: _ClassVar[int]
    segmentations: _containers.RepeatedCompositeFieldContainer[_segment_pb2.Segmentation]
    def __init__(self, segmentations: _Optional[_Iterable[_Union[_segment_pb2.Segmentation, _Mapping]]] = ...) -> None: ...

class Predicate(_message.Message):
    __slots__ = ("variable_name", "predicate_type", "float_vals", "string_vals")
    VARIABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    PREDICATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALS_FIELD_NUMBER: _ClassVar[int]
    STRING_VALS_FIELD_NUMBER: _ClassVar[int]
    variable_name: str
    predicate_type: PredicateType
    float_vals: _containers.RepeatedScalarFieldContainer[float]
    string_vals: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, variable_name: _Optional[str] = ..., predicate_type: _Optional[_Union[PredicateType, str]] = ..., float_vals: _Optional[_Iterable[float]] = ..., string_vals: _Optional[_Iterable[str]] = ...) -> None: ...

class CoordinatesList(_message.Message):
    __slots__ = ("x_list", "y_list")
    X_LIST_FIELD_NUMBER: _ClassVar[int]
    Y_LIST_FIELD_NUMBER: _ClassVar[int]
    x_list: _containers.RepeatedScalarFieldContainer[float]
    y_list: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, x_list: _Optional[_Iterable[float]] = ..., y_list: _Optional[_Iterable[float]] = ...) -> None: ...

class IndexRange(_message.Message):
    __slots__ = ("start", "stop")
    START_FIELD_NUMBER: _ClassVar[int]
    STOP_FIELD_NUMBER: _ClassVar[int]
    start: int
    stop: int
    def __init__(self, start: _Optional[int] = ..., stop: _Optional[int] = ...) -> None: ...

class CompareModelOutputRequest(_message.Message):
    __slots__ = ("output_spec1", "output_spec2", "options")
    class OutputSpec(_message.Message):
        __slots__ = ("model_id", "model_input_spec", "score_type")
        MODEL_ID_FIELD_NUMBER: _ClassVar[int]
        MODEL_INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
        SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
        model_id: ModelId
        model_input_spec: ModelInputSpec
        score_type: _qoi_pb2.QuantityOfInterest
        def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., model_input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ...) -> None: ...
    class Options(_message.Message):
        __slots__ = ("include_breakdown_by_feature", "normalize")
        INCLUDE_BREAKDOWN_BY_FEATURE_FIELD_NUMBER: _ClassVar[int]
        NORMALIZE_FIELD_NUMBER: _ClassVar[int]
        include_breakdown_by_feature: bool
        normalize: bool
        def __init__(self, include_breakdown_by_feature: bool = ..., normalize: bool = ...) -> None: ...
    OUTPUT_SPEC1_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SPEC2_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    output_spec1: CompareModelOutputRequest.OutputSpec
    output_spec2: CompareModelOutputRequest.OutputSpec
    options: CompareModelOutputRequest.Options
    def __init__(self, output_spec1: _Optional[_Union[CompareModelOutputRequest.OutputSpec, _Mapping]] = ..., output_spec2: _Optional[_Union[CompareModelOutputRequest.OutputSpec, _Mapping]] = ..., options: _Optional[_Union[CompareModelOutputRequest.Options, _Mapping]] = ...) -> None: ...

class BatchCompareModelOutputRequest(_message.Message):
    __slots__ = ("project_id", "distance_type_to_output_specs", "options")
    class OutputSpecPair(_message.Message):
        __slots__ = ("output_spec1", "output_spec2")
        OUTPUT_SPEC1_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_SPEC2_FIELD_NUMBER: _ClassVar[int]
        output_spec1: CompareModelOutputRequest.OutputSpec
        output_spec2: CompareModelOutputRequest.OutputSpec
        def __init__(self, output_spec1: _Optional[_Union[CompareModelOutputRequest.OutputSpec, _Mapping]] = ..., output_spec2: _Optional[_Union[CompareModelOutputRequest.OutputSpec, _Mapping]] = ...) -> None: ...
    class ListOfOutputSpecPairs(_message.Message):
        __slots__ = ("output_spec_pairs",)
        OUTPUT_SPEC_PAIRS_FIELD_NUMBER: _ClassVar[int]
        output_spec_pairs: _containers.RepeatedCompositeFieldContainer[BatchCompareModelOutputRequest.OutputSpecPair]
        def __init__(self, output_spec_pairs: _Optional[_Iterable[_Union[BatchCompareModelOutputRequest.OutputSpecPair, _Mapping]]] = ...) -> None: ...
    class DistanceTypeToOutputSpecsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: BatchCompareModelOutputRequest.ListOfOutputSpecPairs
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[BatchCompareModelOutputRequest.ListOfOutputSpecPairs, _Mapping]] = ...) -> None: ...
    class Options(_message.Message):
        __slots__ = ("include_breakdown_by_feature", "normalize")
        INCLUDE_BREAKDOWN_BY_FEATURE_FIELD_NUMBER: _ClassVar[int]
        NORMALIZE_FIELD_NUMBER: _ClassVar[int]
        include_breakdown_by_feature: bool
        normalize: bool
        def __init__(self, include_breakdown_by_feature: bool = ..., normalize: bool = ...) -> None: ...
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_TYPE_TO_OUTPUT_SPECS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    distance_type_to_output_specs: _containers.MessageMap[int, BatchCompareModelOutputRequest.ListOfOutputSpecPairs]
    options: BatchCompareModelOutputRequest.Options
    def __init__(self, project_id: _Optional[str] = ..., distance_type_to_output_specs: _Optional[_Mapping[int, BatchCompareModelOutputRequest.ListOfOutputSpecPairs]] = ..., options: _Optional[_Union[BatchCompareModelOutputRequest.Options, _Mapping]] = ...) -> None: ...

class BatchCompareModelOutputResponse(_message.Message):
    __slots__ = ("distance_type_to_comparison_results",)
    class CompareModelOutputResultType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNDEFINED: _ClassVar[BatchCompareModelOutputResponse.CompareModelOutputResultType]
        VALUE: _ClassVar[BatchCompareModelOutputResponse.CompareModelOutputResultType]
        SPLIT_NOT_FOUND: _ClassVar[BatchCompareModelOutputResponse.CompareModelOutputResultType]
        CANNOT_COMPUTE_PREDICTIONS: _ClassVar[BatchCompareModelOutputResponse.CompareModelOutputResultType]
        PREDICTION_UNAVAILABLE: _ClassVar[BatchCompareModelOutputResponse.CompareModelOutputResultType]
        INFLUENCE_UNAVAILBLE: _ClassVar[BatchCompareModelOutputResponse.CompareModelOutputResultType]
        UNKNOWN_EXCEPTION: _ClassVar[BatchCompareModelOutputResponse.CompareModelOutputResultType]
    UNDEFINED: BatchCompareModelOutputResponse.CompareModelOutputResultType
    VALUE: BatchCompareModelOutputResponse.CompareModelOutputResultType
    SPLIT_NOT_FOUND: BatchCompareModelOutputResponse.CompareModelOutputResultType
    CANNOT_COMPUTE_PREDICTIONS: BatchCompareModelOutputResponse.CompareModelOutputResultType
    PREDICTION_UNAVAILABLE: BatchCompareModelOutputResponse.CompareModelOutputResultType
    INFLUENCE_UNAVAILBLE: BatchCompareModelOutputResponse.CompareModelOutputResultType
    UNKNOWN_EXCEPTION: BatchCompareModelOutputResponse.CompareModelOutputResultType
    class ResponseEntry(_message.Message):
        __slots__ = ("num_points1", "num_points2", "distance_value", "result_type", "feature_breakdown", "pending_operations", "error_message")
        class FeatureBreakdownEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: float
            def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
        NUM_POINTS1_FIELD_NUMBER: _ClassVar[int]
        NUM_POINTS2_FIELD_NUMBER: _ClassVar[int]
        DISTANCE_VALUE_FIELD_NUMBER: _ClassVar[int]
        RESULT_TYPE_FIELD_NUMBER: _ClassVar[int]
        FEATURE_BREAKDOWN_FIELD_NUMBER: _ClassVar[int]
        PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
        ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
        num_points1: int
        num_points2: int
        distance_value: float
        result_type: BatchCompareModelOutputResponse.CompareModelOutputResultType
        feature_breakdown: _containers.ScalarMap[str, float]
        pending_operations: PendingOperations
        error_message: str
        def __init__(self, num_points1: _Optional[int] = ..., num_points2: _Optional[int] = ..., distance_value: _Optional[float] = ..., result_type: _Optional[_Union[BatchCompareModelOutputResponse.CompareModelOutputResultType, str]] = ..., feature_breakdown: _Optional[_Mapping[str, float]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ..., error_message: _Optional[str] = ...) -> None: ...
    class ListOfResponseEntries(_message.Message):
        __slots__ = ("comparison_results",)
        COMPARISON_RESULTS_FIELD_NUMBER: _ClassVar[int]
        comparison_results: _containers.RepeatedCompositeFieldContainer[BatchCompareModelOutputResponse.ResponseEntry]
        def __init__(self, comparison_results: _Optional[_Iterable[_Union[BatchCompareModelOutputResponse.ResponseEntry, _Mapping]]] = ...) -> None: ...
    class DistanceTypeToComparisonResultsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: BatchCompareModelOutputResponse.ListOfResponseEntries
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[BatchCompareModelOutputResponse.ListOfResponseEntries, _Mapping]] = ...) -> None: ...
    DISTANCE_TYPE_TO_COMPARISON_RESULTS_FIELD_NUMBER: _ClassVar[int]
    distance_type_to_comparison_results: _containers.MessageMap[int, BatchCompareModelOutputResponse.ListOfResponseEntries]
    def __init__(self, distance_type_to_comparison_results: _Optional[_Mapping[int, BatchCompareModelOutputResponse.ListOfResponseEntries]] = ...) -> None: ...

class DistributionResponseEntry(_message.Message):
    __slots__ = ("distance_type", "distance_value", "feature_breakdown")
    class FeatureBreakdownEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    DISTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_VALUE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_BREAKDOWN_FIELD_NUMBER: _ClassVar[int]
    distance_type: _distance_pb2.DistanceType
    distance_value: float
    feature_breakdown: _containers.ScalarMap[str, float]
    def __init__(self, distance_type: _Optional[_Union[_distance_pb2.DistanceType, str]] = ..., distance_value: _Optional[float] = ..., feature_breakdown: _Optional[_Mapping[str, float]] = ...) -> None: ...

class CompareModelOutputResponse(_message.Message):
    __slots__ = ("num_points1", "num_points2", "distribution_comparisons", "pending_operations")
    NUM_POINTS1_FIELD_NUMBER: _ClassVar[int]
    NUM_POINTS2_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTION_COMPARISONS_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    num_points1: int
    num_points2: int
    distribution_comparisons: _containers.RepeatedCompositeFieldContainer[DistributionResponseEntry]
    pending_operations: PendingOperations
    def __init__(self, num_points1: _Optional[int] = ..., num_points2: _Optional[int] = ..., distribution_comparisons: _Optional[_Iterable[_Union[DistributionResponseEntry, _Mapping]]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ...) -> None: ...

class ModelThresholdScoreType(_message.Message):
    __slots__ = ()
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEFAULT_SCORE_TYPE: _ClassVar[ModelThresholdScoreType.Type]
        PROBITS: _ClassVar[ModelThresholdScoreType.Type]
        LOGITS: _ClassVar[ModelThresholdScoreType.Type]
    DEFAULT_SCORE_TYPE: ModelThresholdScoreType.Type
    PROBITS: ModelThresholdScoreType.Type
    LOGITS: ModelThresholdScoreType.Type
    def __init__(self) -> None: ...

class ModelThresholdConfigRequest(_message.Message):
    __slots__ = ("threshold_request_type", "default_threshold_options", "manual_threshold_options", "percentile_threshold_options")
    class ModelThresholdRequestType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEFAULT_THRESHOLD: _ClassVar[ModelThresholdConfigRequest.ModelThresholdRequestType]
        MANUAL_THRESHOLDS: _ClassVar[ModelThresholdConfigRequest.ModelThresholdRequestType]
        THRESHOLD_BY_PERCENTILE: _ClassVar[ModelThresholdConfigRequest.ModelThresholdRequestType]
    DEFAULT_THRESHOLD: ModelThresholdConfigRequest.ModelThresholdRequestType
    MANUAL_THRESHOLDS: ModelThresholdConfigRequest.ModelThresholdRequestType
    THRESHOLD_BY_PERCENTILE: ModelThresholdConfigRequest.ModelThresholdRequestType
    class DefaultThresholdOptions(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ManualThresholdOptions(_message.Message):
        __slots__ = ("threshold_score_type", "classifier_thresholds")
        THRESHOLD_SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
        CLASSIFIER_THRESHOLDS_FIELD_NUMBER: _ClassVar[int]
        threshold_score_type: ModelThresholdScoreType.Type
        classifier_thresholds: _containers.RepeatedScalarFieldContainer[float]
        def __init__(self, threshold_score_type: _Optional[_Union[ModelThresholdScoreType.Type, str]] = ..., classifier_thresholds: _Optional[_Iterable[float]] = ...) -> None: ...
    class PercentileThresholdOptions(_message.Message):
        __slots__ = ("threshold_score_type",)
        THRESHOLD_SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
        threshold_score_type: ModelThresholdScoreType.Type
        def __init__(self, threshold_score_type: _Optional[_Union[ModelThresholdScoreType.Type, str]] = ...) -> None: ...
    THRESHOLD_REQUEST_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_THRESHOLD_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    MANUAL_THRESHOLD_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PERCENTILE_THRESHOLD_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    threshold_request_type: ModelThresholdConfigRequest.ModelThresholdRequestType
    default_threshold_options: ModelThresholdConfigRequest.DefaultThresholdOptions
    manual_threshold_options: ModelThresholdConfigRequest.ManualThresholdOptions
    percentile_threshold_options: ModelThresholdConfigRequest.PercentileThresholdOptions
    def __init__(self, threshold_request_type: _Optional[_Union[ModelThresholdConfigRequest.ModelThresholdRequestType, str]] = ..., default_threshold_options: _Optional[_Union[ModelThresholdConfigRequest.DefaultThresholdOptions, _Mapping]] = ..., manual_threshold_options: _Optional[_Union[ModelThresholdConfigRequest.ManualThresholdOptions, _Mapping]] = ..., percentile_threshold_options: _Optional[_Union[ModelThresholdConfigRequest.PercentileThresholdOptions, _Mapping]] = ...) -> None: ...

class ModelThresholdConfigResponse(_message.Message):
    __slots__ = ("threshold_score_type", "threshold_value", "threshold_percentile")
    THRESHOLD_SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_PERCENTILE_FIELD_NUMBER: _ClassVar[int]
    threshold_score_type: ModelThresholdScoreType.Type
    threshold_value: float
    threshold_percentile: float
    def __init__(self, threshold_score_type: _Optional[_Union[ModelThresholdScoreType.Type, str]] = ..., threshold_value: _Optional[float] = ..., threshold_percentile: _Optional[float] = ...) -> None: ...

class BiasType(_message.Message):
    __slots__ = ()
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[BiasType.Type]
        DISPARATE_IMPACT_RATIO: _ClassVar[BiasType.Type]
        STATISTICAL_PARITY_DIFFERENCE: _ClassVar[BiasType.Type]
        TRUE_POSITIVE_RATIO: _ClassVar[BiasType.Type]
        FALSE_POSITIVE_RATIO: _ClassVar[BiasType.Type]
        TRUE_NEGATIVE_RATIO: _ClassVar[BiasType.Type]
        FALSE_NEGATIVE_RATIO: _ClassVar[BiasType.Type]
        TRUE_POSITIVE_DIFFERENCE: _ClassVar[BiasType.Type]
        FALSE_POSITIVE_DIFFERENCE: _ClassVar[BiasType.Type]
        TRUE_NEGATIVE_DIFFERENCE: _ClassVar[BiasType.Type]
        FALSE_NEGATIVE_DIFFERENCE: _ClassVar[BiasType.Type]
        TREATMENT_EQUALITY_DIFFERENCE: _ClassVar[BiasType.Type]
        EQUALITY_OF_OPPORTUNITY_DIFFERENCE: _ClassVar[BiasType.Type]
        EQUALITY_OF_OPPORTUNITY_RATIO: _ClassVar[BiasType.Type]
        AVERAGE_ODDS_DIFFERENCE: _ClassVar[BiasType.Type]
        CONDITIONAL_ACCEPTANCE_DIFFERENCE: _ClassVar[BiasType.Type]
        CONDITIONAL_REJECTION_DIFFERENCE: _ClassVar[BiasType.Type]
        ACCEPTANCE_RATE_DIFFERENCE: _ClassVar[BiasType.Type]
        REJECTION_RATE_DIFFERENCE: _ClassVar[BiasType.Type]
        L1_ERROR_DIFFERENCE: _ClassVar[BiasType.Type]
        L2_ERROR_DIFFERENCE: _ClassVar[BiasType.Type]
        MEAN_SCORE_DIFFERENCE: _ClassVar[BiasType.Type]
    UNKNOWN: BiasType.Type
    DISPARATE_IMPACT_RATIO: BiasType.Type
    STATISTICAL_PARITY_DIFFERENCE: BiasType.Type
    TRUE_POSITIVE_RATIO: BiasType.Type
    FALSE_POSITIVE_RATIO: BiasType.Type
    TRUE_NEGATIVE_RATIO: BiasType.Type
    FALSE_NEGATIVE_RATIO: BiasType.Type
    TRUE_POSITIVE_DIFFERENCE: BiasType.Type
    FALSE_POSITIVE_DIFFERENCE: BiasType.Type
    TRUE_NEGATIVE_DIFFERENCE: BiasType.Type
    FALSE_NEGATIVE_DIFFERENCE: BiasType.Type
    TREATMENT_EQUALITY_DIFFERENCE: BiasType.Type
    EQUALITY_OF_OPPORTUNITY_DIFFERENCE: BiasType.Type
    EQUALITY_OF_OPPORTUNITY_RATIO: BiasType.Type
    AVERAGE_ODDS_DIFFERENCE: BiasType.Type
    CONDITIONAL_ACCEPTANCE_DIFFERENCE: BiasType.Type
    CONDITIONAL_REJECTION_DIFFERENCE: BiasType.Type
    ACCEPTANCE_RATE_DIFFERENCE: BiasType.Type
    REJECTION_RATE_DIFFERENCE: BiasType.Type
    L1_ERROR_DIFFERENCE: BiasType.Type
    L2_ERROR_DIFFERENCE: BiasType.Type
    MEAN_SCORE_DIFFERENCE: BiasType.Type
    def __init__(self) -> None: ...

class GetModelBiasRequest(_message.Message):
    __slots__ = ("model_id", "segment1", "segment2", "bias_types", "threshold_config")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENT1_FIELD_NUMBER: _ClassVar[int]
    SEGMENT2_FIELD_NUMBER: _ClassVar[int]
    BIAS_TYPES_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_CONFIG_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    segment1: ModelInputSpec
    segment2: ModelInputSpec
    bias_types: _containers.RepeatedScalarFieldContainer[BiasType.Type]
    threshold_config: ModelThresholdConfigRequest
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., segment1: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., segment2: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., bias_types: _Optional[_Iterable[_Union[BiasType.Type, str]]] = ..., threshold_config: _Optional[_Union[ModelThresholdConfigRequest, _Mapping]] = ...) -> None: ...

class GetBatchModelBiasRequest(_message.Message):
    __slots__ = ("project_id", "bias_requests")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    BIAS_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    bias_requests: _containers.RepeatedCompositeFieldContainer[GetModelBiasRequest]
    def __init__(self, project_id: _Optional[str] = ..., bias_requests: _Optional[_Iterable[_Union[GetModelBiasRequest, _Mapping]]] = ...) -> None: ...

class BiasResult(_message.Message):
    __slots__ = ("bias_type", "segment1_metric", "segment2_metric", "aggregate_metric", "segment1_favored", "result_type", "threshold_config", "error_message")
    class BiasResultType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNDEFINED: _ClassVar[BiasResult.BiasResultType]
        VALUE: _ClassVar[BiasResult.BiasResultType]
        ONLY_ONE_LABEL_CLASS: _ClassVar[BiasResult.BiasResultType]
        CANNOT_COMPUTE_PREDICTIONS: _ClassVar[BiasResult.BiasResultType]
        PREDICTION_UNAVAILABLE: _ClassVar[BiasResult.BiasResultType]
        UNKNOWN_EXCEPTION: _ClassVar[BiasResult.BiasResultType]
    UNDEFINED: BiasResult.BiasResultType
    VALUE: BiasResult.BiasResultType
    ONLY_ONE_LABEL_CLASS: BiasResult.BiasResultType
    CANNOT_COMPUTE_PREDICTIONS: BiasResult.BiasResultType
    PREDICTION_UNAVAILABLE: BiasResult.BiasResultType
    UNKNOWN_EXCEPTION: BiasResult.BiasResultType
    BIAS_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEGMENT1_METRIC_FIELD_NUMBER: _ClassVar[int]
    SEGMENT2_METRIC_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_METRIC_FIELD_NUMBER: _ClassVar[int]
    SEGMENT1_FAVORED_FIELD_NUMBER: _ClassVar[int]
    RESULT_TYPE_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    bias_type: BiasType.Type
    segment1_metric: float
    segment2_metric: float
    aggregate_metric: float
    segment1_favored: bool
    result_type: BiasResult.BiasResultType
    threshold_config: ModelThresholdConfigResponse
    error_message: str
    def __init__(self, bias_type: _Optional[_Union[BiasType.Type, str]] = ..., segment1_metric: _Optional[float] = ..., segment2_metric: _Optional[float] = ..., aggregate_metric: _Optional[float] = ..., segment1_favored: bool = ..., result_type: _Optional[_Union[BiasResult.BiasResultType, str]] = ..., threshold_config: _Optional[_Union[ModelThresholdConfigResponse, _Mapping]] = ..., error_message: _Optional[str] = ...) -> None: ...

class GetModelBiasResponse(_message.Message):
    __slots__ = ("bias_results", "num_points_segment1", "num_points_segment2", "pending_operations")
    BIAS_RESULTS_FIELD_NUMBER: _ClassVar[int]
    NUM_POINTS_SEGMENT1_FIELD_NUMBER: _ClassVar[int]
    NUM_POINTS_SEGMENT2_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    bias_results: _containers.RepeatedCompositeFieldContainer[BiasResult]
    num_points_segment1: int
    num_points_segment2: int
    pending_operations: PendingOperations
    def __init__(self, bias_results: _Optional[_Iterable[_Union[BiasResult, _Mapping]]] = ..., num_points_segment1: _Optional[int] = ..., num_points_segment2: _Optional[int] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ...) -> None: ...

class GetBatchModelBiasResponse(_message.Message):
    __slots__ = ("bias_responses",)
    BIAS_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    bias_responses: _containers.RepeatedCompositeFieldContainer[GetModelBiasResponse]
    def __init__(self, bias_responses: _Optional[_Iterable[_Union[GetModelBiasResponse, _Mapping]]] = ...) -> None: ...

class FeatureDriftRequest(_message.Message):
    __slots__ = ("input_spec1", "input_spec2", "distances", "features")
    INPUT_SPEC1_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC2_FIELD_NUMBER: _ClassVar[int]
    DISTANCES_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    input_spec1: ModelInputSpec
    input_spec2: ModelInputSpec
    distances: _containers.RepeatedScalarFieldContainer[_distance_pb2.DistanceType]
    features: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, input_spec1: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., input_spec2: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., distances: _Optional[_Iterable[_Union[_distance_pb2.DistanceType, str]]] = ..., features: _Optional[_Iterable[str]] = ...) -> None: ...

class FeatureDriftResponse(_message.Message):
    __slots__ = ("drifts",)
    DRIFTS_FIELD_NUMBER: _ClassVar[int]
    drifts: _containers.RepeatedCompositeFieldContainer[FeatureDrift]
    def __init__(self, drifts: _Optional[_Iterable[_Union[FeatureDrift, _Mapping]]] = ...) -> None: ...

class PartialDependencePlotRequest(_message.Message):
    __slots__ = ("model_id", "quantity_of_interest", "background_data_split_info")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_OF_INTEREST_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_DATA_SPLIT_INFO_FIELD_NUMBER: _ClassVar[int]
    model_id: ModelId
    quantity_of_interest: _qoi_pb2.QuantityOfInterest
    background_data_split_info: _background_data_split_info_pb2.BackgroundDataSplitInfo
    def __init__(self, model_id: _Optional[_Union[ModelId, _Mapping]] = ..., quantity_of_interest: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., background_data_split_info: _Optional[_Union[_background_data_split_info_pb2.BackgroundDataSplitInfo, _Mapping]] = ...) -> None: ...

class PartialDependencePlotResponse(_message.Message):
    __slots__ = ("pending_operations", "prefeatures", "xs", "ys", "special_values_xs", "special_values_ys")
    class XsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _elementary_types_pb2.ValueList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_elementary_types_pb2.ValueList, _Mapping]] = ...) -> None: ...
    class YsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _elementary_types_pb2.FloatList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_elementary_types_pb2.FloatList, _Mapping]] = ...) -> None: ...
    class SpecialValuesXsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _elementary_types_pb2.ValueList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_elementary_types_pb2.ValueList, _Mapping]] = ...) -> None: ...
    class SpecialValuesYsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _elementary_types_pb2.FloatList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_elementary_types_pb2.FloatList, _Mapping]] = ...) -> None: ...
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    PREFEATURES_FIELD_NUMBER: _ClassVar[int]
    XS_FIELD_NUMBER: _ClassVar[int]
    YS_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_VALUES_XS_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_VALUES_YS_FIELD_NUMBER: _ClassVar[int]
    pending_operations: PendingOperations
    prefeatures: _containers.RepeatedScalarFieldContainer[str]
    xs: _containers.MessageMap[str, _elementary_types_pb2.ValueList]
    ys: _containers.MessageMap[str, _elementary_types_pb2.FloatList]
    special_values_xs: _containers.MessageMap[str, _elementary_types_pb2.ValueList]
    special_values_ys: _containers.MessageMap[str, _elementary_types_pb2.FloatList]
    def __init__(self, pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ..., prefeatures: _Optional[_Iterable[str]] = ..., xs: _Optional[_Mapping[str, _elementary_types_pb2.ValueList]] = ..., ys: _Optional[_Mapping[str, _elementary_types_pb2.FloatList]] = ..., special_values_xs: _Optional[_Mapping[str, _elementary_types_pb2.ValueList]] = ..., special_values_ys: _Optional[_Mapping[str, _elementary_types_pb2.FloatList]] = ...) -> None: ...

class InterestingSegmentsRequest(_message.Message):
    __slots__ = ("project_id", "model_ids", "model_input_specs", "interesting_segment_type", "num_features", "max_num_responses", "bootstrapping_fraction", "random_state", "num_samples", "pointwise_metrics_aggregator", "use_labels")
    class PointwiseMetricsAggregator(_message.Message):
        __slots__ = ("minimum_size", "size_exponent", "minimum_metric_of_interest_threshold")
        MINIMUM_SIZE_FIELD_NUMBER: _ClassVar[int]
        SIZE_EXPONENT_FIELD_NUMBER: _ClassVar[int]
        MINIMUM_METRIC_OF_INTEREST_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
        minimum_size: int
        size_exponent: float
        minimum_metric_of_interest_threshold: float
        def __init__(self, minimum_size: _Optional[int] = ..., size_exponent: _Optional[float] = ..., minimum_metric_of_interest_threshold: _Optional[float] = ...) -> None: ...
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_IDS_FIELD_NUMBER: _ClassVar[int]
    MODEL_INPUT_SPECS_FIELD_NUMBER: _ClassVar[int]
    INTERESTING_SEGMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUM_FEATURES_FIELD_NUMBER: _ClassVar[int]
    MAX_NUM_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    BOOTSTRAPPING_FRACTION_FIELD_NUMBER: _ClassVar[int]
    RANDOM_STATE_FIELD_NUMBER: _ClassVar[int]
    NUM_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    POINTWISE_METRICS_AGGREGATOR_FIELD_NUMBER: _ClassVar[int]
    USE_LABELS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_ids: _containers.RepeatedScalarFieldContainer[str]
    model_input_specs: _containers.RepeatedCompositeFieldContainer[ModelInputSpec]
    interesting_segment_type: _segment_pb2.InterestingSegment.Type
    num_features: int
    max_num_responses: int
    bootstrapping_fraction: float
    random_state: int
    num_samples: int
    pointwise_metrics_aggregator: InterestingSegmentsRequest.PointwiseMetricsAggregator
    use_labels: bool
    def __init__(self, project_id: _Optional[str] = ..., model_ids: _Optional[_Iterable[str]] = ..., model_input_specs: _Optional[_Iterable[_Union[ModelInputSpec, _Mapping]]] = ..., interesting_segment_type: _Optional[_Union[_segment_pb2.InterestingSegment.Type, str]] = ..., num_features: _Optional[int] = ..., max_num_responses: _Optional[int] = ..., bootstrapping_fraction: _Optional[float] = ..., random_state: _Optional[int] = ..., num_samples: _Optional[int] = ..., pointwise_metrics_aggregator: _Optional[_Union[InterestingSegmentsRequest.PointwiseMetricsAggregator, _Mapping]] = ..., use_labels: bool = ...) -> None: ...

class InterestingSegmentsResponse(_message.Message):
    __slots__ = ("pending_operations", "segmentation_ids")
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    SEGMENTATION_IDS_FIELD_NUMBER: _ClassVar[int]
    pending_operations: PendingOperations
    segmentation_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ..., segmentation_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class FeatureDrift(_message.Message):
    __slots__ = ("feature", "distance_type", "distance_value")
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_VALUE_FIELD_NUMBER: _ClassVar[int]
    feature: str
    distance_type: _distance_pb2.DistanceType
    distance_value: float
    def __init__(self, feature: _Optional[str] = ..., distance_type: _Optional[_Union[_distance_pb2.DistanceType, str]] = ..., distance_value: _Optional[float] = ...) -> None: ...

class DataSummaryRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "input_spec", "artifact_type", "pre_operation_types", "aggregation_types", "columns_to_summarize", "model_id", "prediction_options", "feature_influence_options", "ignore_cache")
    class ArtifactType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ARTIFACT_TYPE_UNKNOWN: _ClassVar[DataSummaryRequest.ArtifactType]
        ARTIFACT_TYPE_PREPROCESSED_DATA: _ClassVar[DataSummaryRequest.ArtifactType]
        ARTIFACT_TYPE_POSTPROCESSED_DATA: _ClassVar[DataSummaryRequest.ArtifactType]
        ARTIFACT_TYPE_EXTRA_DATA: _ClassVar[DataSummaryRequest.ArtifactType]
        ARTIFACT_TYPE_GROUND_TRUTH_LABELS: _ClassVar[DataSummaryRequest.ArtifactType]
        ARTIFACT_TYPE_MODEL_PREDICTIONS: _ClassVar[DataSummaryRequest.ArtifactType]
        ARTIFACT_TYPE_MODEL_FEATURE_INFLUENCES: _ClassVar[DataSummaryRequest.ArtifactType]
    ARTIFACT_TYPE_UNKNOWN: DataSummaryRequest.ArtifactType
    ARTIFACT_TYPE_PREPROCESSED_DATA: DataSummaryRequest.ArtifactType
    ARTIFACT_TYPE_POSTPROCESSED_DATA: DataSummaryRequest.ArtifactType
    ARTIFACT_TYPE_EXTRA_DATA: DataSummaryRequest.ArtifactType
    ARTIFACT_TYPE_GROUND_TRUTH_LABELS: DataSummaryRequest.ArtifactType
    ARTIFACT_TYPE_MODEL_PREDICTIONS: DataSummaryRequest.ArtifactType
    ARTIFACT_TYPE_MODEL_FEATURE_INFLUENCES: DataSummaryRequest.ArtifactType
    class OperationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OPERATION_TYPE_UNKNOWN: _ClassVar[DataSummaryRequest.OperationType]
        OPERATION_TYPE_ABSOLUTE_VALUE: _ClassVar[DataSummaryRequest.OperationType]
        OPERATION_TYPE_DISTINCT: _ClassVar[DataSummaryRequest.OperationType]
    OPERATION_TYPE_UNKNOWN: DataSummaryRequest.OperationType
    OPERATION_TYPE_ABSOLUTE_VALUE: DataSummaryRequest.OperationType
    OPERATION_TYPE_DISTINCT: DataSummaryRequest.OperationType
    class AggregationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AGGREGATION_TYPE_UNKNOWN: _ClassVar[DataSummaryRequest.AggregationType]
        AGGREGATION_TYPE_MEAN: _ClassVar[DataSummaryRequest.AggregationType]
        AGGREGATION_TYPE_SUM: _ClassVar[DataSummaryRequest.AggregationType]
        AGGREGATION_TYPE_COUNT: _ClassVar[DataSummaryRequest.AggregationType]
        AGGREGATION_TYPE_COUNT_NON_NA: _ClassVar[DataSummaryRequest.AggregationType]
        AGGREGATION_TYPE_MIN: _ClassVar[DataSummaryRequest.AggregationType]
        AGGREGATION_TYPE_MAX: _ClassVar[DataSummaryRequest.AggregationType]
        AGGREGATION_TYPE_VARIANCE: _ClassVar[DataSummaryRequest.AggregationType]
        AGGREGATION_TYPE_HISTOGRAM: _ClassVar[DataSummaryRequest.AggregationType]
        AGGREGATION_TYPE_SUM_OF_ONES_COMPLIMENTS: _ClassVar[DataSummaryRequest.AggregationType]
    AGGREGATION_TYPE_UNKNOWN: DataSummaryRequest.AggregationType
    AGGREGATION_TYPE_MEAN: DataSummaryRequest.AggregationType
    AGGREGATION_TYPE_SUM: DataSummaryRequest.AggregationType
    AGGREGATION_TYPE_COUNT: DataSummaryRequest.AggregationType
    AGGREGATION_TYPE_COUNT_NON_NA: DataSummaryRequest.AggregationType
    AGGREGATION_TYPE_MIN: DataSummaryRequest.AggregationType
    AGGREGATION_TYPE_MAX: DataSummaryRequest.AggregationType
    AGGREGATION_TYPE_VARIANCE: DataSummaryRequest.AggregationType
    AGGREGATION_TYPE_HISTOGRAM: DataSummaryRequest.AggregationType
    AGGREGATION_TYPE_SUM_OF_ONES_COMPLIMENTS: DataSummaryRequest.AggregationType
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PRE_OPERATION_TYPES_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_TYPES_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_TO_SUMMARIZE_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_INFLUENCE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    IGNORE_CACHE_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    input_spec: ModelInputSpec
    artifact_type: DataSummaryRequest.ArtifactType
    pre_operation_types: _containers.RepeatedScalarFieldContainer[DataSummaryRequest.OperationType]
    aggregation_types: _containers.RepeatedScalarFieldContainer[DataSummaryRequest.AggregationType]
    columns_to_summarize: _containers.RepeatedScalarFieldContainer[str]
    model_id: str
    prediction_options: _common_pb2.PredictionOptions
    feature_influence_options: _common_pb2.FeatureInfluenceOptions
    ignore_cache: bool
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., artifact_type: _Optional[_Union[DataSummaryRequest.ArtifactType, str]] = ..., pre_operation_types: _Optional[_Iterable[_Union[DataSummaryRequest.OperationType, str]]] = ..., aggregation_types: _Optional[_Iterable[_Union[DataSummaryRequest.AggregationType, str]]] = ..., columns_to_summarize: _Optional[_Iterable[str]] = ..., model_id: _Optional[str] = ..., prediction_options: _Optional[_Union[_common_pb2.PredictionOptions, _Mapping]] = ..., feature_influence_options: _Optional[_Union[_common_pb2.FeatureInfluenceOptions, _Mapping]] = ..., ignore_cache: bool = ...) -> None: ...

class DataSummaryResponse(_message.Message):
    __slots__ = ("summaries", "pending_operations")
    class DataSummary(_message.Message):
        __slots__ = ("summary_value", "summary_value_table")
        SUMMARY_VALUE_FIELD_NUMBER: _ClassVar[int]
        SUMMARY_VALUE_TABLE_FIELD_NUMBER: _ClassVar[int]
        summary_value: float
        summary_value_table: ValueTable
        def __init__(self, summary_value: _Optional[float] = ..., summary_value_table: _Optional[_Union[ValueTable, _Mapping]] = ...) -> None: ...
    SUMMARIES_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    summaries: _containers.RepeatedCompositeFieldContainer[DataSummaryResponse.DataSummary]
    pending_operations: PendingOperations
    def __init__(self, summaries: _Optional[_Iterable[_Union[DataSummaryResponse.DataSummary, _Mapping]]] = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ...) -> None: ...

class BatchDataSummaryRequestEntry(_message.Message):
    __slots__ = ("input_spec", "artifact_type", "pre_operation_types", "aggregation_types", "columns_to_summarize", "model_id", "prediction_options", "feature_influence_options")
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PRE_OPERATION_TYPES_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_TYPES_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_TO_SUMMARIZE_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_INFLUENCE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    input_spec: ModelInputSpec
    artifact_type: DataSummaryRequest.ArtifactType
    pre_operation_types: _containers.RepeatedScalarFieldContainer[DataSummaryRequest.OperationType]
    aggregation_types: _containers.RepeatedScalarFieldContainer[DataSummaryRequest.AggregationType]
    columns_to_summarize: _containers.RepeatedScalarFieldContainer[str]
    model_id: str
    prediction_options: _common_pb2.PredictionOptions
    feature_influence_options: _common_pb2.FeatureInfluenceOptions
    def __init__(self, input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., artifact_type: _Optional[_Union[DataSummaryRequest.ArtifactType, str]] = ..., pre_operation_types: _Optional[_Iterable[_Union[DataSummaryRequest.OperationType, str]]] = ..., aggregation_types: _Optional[_Iterable[_Union[DataSummaryRequest.AggregationType, str]]] = ..., columns_to_summarize: _Optional[_Iterable[str]] = ..., model_id: _Optional[str] = ..., prediction_options: _Optional[_Union[_common_pb2.PredictionOptions, _Mapping]] = ..., feature_influence_options: _Optional[_Union[_common_pb2.FeatureInfluenceOptions, _Mapping]] = ...) -> None: ...

class BatchDataSummaryRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "request_entries", "ignore_cache")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    IGNORE_CACHE_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    request_entries: _containers.RepeatedCompositeFieldContainer[BatchDataSummaryRequestEntry]
    ignore_cache: bool
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., request_entries: _Optional[_Iterable[_Union[BatchDataSummaryRequestEntry, _Mapping]]] = ..., ignore_cache: bool = ...) -> None: ...

class BatchDataSummaryResponseEntry(_message.Message):
    __slots__ = ("summaries", "error")
    SUMMARIES_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    summaries: _containers.RepeatedCompositeFieldContainer[DataSummaryResponse.DataSummary]
    error: _common_pb2.Error
    def __init__(self, summaries: _Optional[_Iterable[_Union[DataSummaryResponse.DataSummary, _Mapping]]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class BatchDataSummaryResponse(_message.Message):
    __slots__ = ("resp_entries",)
    RESP_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    resp_entries: _containers.RepeatedCompositeFieldContainer[BatchDataSummaryResponseEntry]
    def __init__(self, resp_entries: _Optional[_Iterable[_Union[BatchDataSummaryResponseEntry, _Mapping]]] = ...) -> None: ...

class BatchISPRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "model_id", "input_spec", "features", "feature_influence_options", "ignore_cache")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_INFLUENCE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    IGNORE_CACHE_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    model_id: str
    input_spec: ModelInputSpec
    features: _containers.RepeatedScalarFieldContainer[str]
    feature_influence_options: _common_pb2.FeatureInfluenceOptions
    ignore_cache: bool
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., model_id: _Optional[str] = ..., input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., features: _Optional[_Iterable[str]] = ..., feature_influence_options: _Optional[_Union[_common_pb2.FeatureInfluenceOptions, _Mapping]] = ..., ignore_cache: bool = ...) -> None: ...

class BatchISPResponse(_message.Message):
    __slots__ = ("grid_summary_per_feature", "error")
    class GridBasedDensity(_message.Message):
        __slots__ = ("grid_summary", "error", "is_categorical")
        GRID_SUMMARY_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        IS_CATEGORICAL_FIELD_NUMBER: _ClassVar[int]
        grid_summary: FloatTable
        error: _common_pb2.Error
        is_categorical: bool
        def __init__(self, grid_summary: _Optional[_Union[FloatTable, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ..., is_categorical: bool = ...) -> None: ...
    class GridSummaryPerFeatureEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: BatchISPResponse.GridBasedDensity
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[BatchISPResponse.GridBasedDensity, _Mapping]] = ...) -> None: ...
    GRID_SUMMARY_PER_FEATURE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    grid_summary_per_feature: _containers.MessageMap[str, BatchISPResponse.GridBasedDensity]
    error: _common_pb2.Error
    def __init__(self, grid_summary_per_feature: _Optional[_Mapping[str, BatchISPResponse.GridBasedDensity]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class HistogramRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "input_spec", "data_type", "model_id", "prediction_options", "feature_influence_options", "feature_name", "ignore_cache")
    class HistogramDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        HISTOGRAM_DATA_TYPE_UNKNOWN: _ClassVar[HistogramRequest.HistogramDataType]
        HISTOGRAM_DATA_TYPE_PREDICTIONS: _ClassVar[HistogramRequest.HistogramDataType]
        HISTOGRAM_DATA_TYPE_GROUND_TRUTH: _ClassVar[HistogramRequest.HistogramDataType]
        HISTOGRAM_DATA_TYPE_PREPROCESSED_DATA: _ClassVar[HistogramRequest.HistogramDataType]
        HISTOGRAM_DATA_TYPE_EXTRA_DATA: _ClassVar[HistogramRequest.HistogramDataType]
        HISTOGRAM_DATA_TYPE_FEATURE_INFLUENCES: _ClassVar[HistogramRequest.HistogramDataType]
    HISTOGRAM_DATA_TYPE_UNKNOWN: HistogramRequest.HistogramDataType
    HISTOGRAM_DATA_TYPE_PREDICTIONS: HistogramRequest.HistogramDataType
    HISTOGRAM_DATA_TYPE_GROUND_TRUTH: HistogramRequest.HistogramDataType
    HISTOGRAM_DATA_TYPE_PREPROCESSED_DATA: HistogramRequest.HistogramDataType
    HISTOGRAM_DATA_TYPE_EXTRA_DATA: HistogramRequest.HistogramDataType
    HISTOGRAM_DATA_TYPE_FEATURE_INFLUENCES: HistogramRequest.HistogramDataType
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_INFLUENCE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_NAME_FIELD_NUMBER: _ClassVar[int]
    IGNORE_CACHE_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    input_spec: ModelInputSpec
    data_type: HistogramRequest.HistogramDataType
    model_id: str
    prediction_options: _common_pb2.PredictionOptions
    feature_influence_options: _common_pb2.FeatureInfluenceOptions
    feature_name: str
    ignore_cache: bool
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., input_spec: _Optional[_Union[ModelInputSpec, _Mapping]] = ..., data_type: _Optional[_Union[HistogramRequest.HistogramDataType, str]] = ..., model_id: _Optional[str] = ..., prediction_options: _Optional[_Union[_common_pb2.PredictionOptions, _Mapping]] = ..., feature_influence_options: _Optional[_Union[_common_pb2.FeatureInfluenceOptions, _Mapping]] = ..., feature_name: _Optional[str] = ..., ignore_cache: bool = ...) -> None: ...

class HistogramResponse(_message.Message):
    __slots__ = ("numerical_bins", "categorical_bins", "is_categorical", "pending_operations")
    class NumericalHistogramBin(_message.Message):
        __slots__ = ("bin_start", "bin_end", "bin_count")
        BIN_START_FIELD_NUMBER: _ClassVar[int]
        BIN_END_FIELD_NUMBER: _ClassVar[int]
        BIN_COUNT_FIELD_NUMBER: _ClassVar[int]
        bin_start: float
        bin_end: float
        bin_count: int
        def __init__(self, bin_start: _Optional[float] = ..., bin_end: _Optional[float] = ..., bin_count: _Optional[int] = ...) -> None: ...
    class CategoricalHistogramBin(_message.Message):
        __slots__ = ("bin_category", "bin_count")
        BIN_CATEGORY_FIELD_NUMBER: _ClassVar[int]
        BIN_COUNT_FIELD_NUMBER: _ClassVar[int]
        bin_category: str
        bin_count: int
        def __init__(self, bin_category: _Optional[str] = ..., bin_count: _Optional[int] = ...) -> None: ...
    NUMERICAL_BINS_FIELD_NUMBER: _ClassVar[int]
    CATEGORICAL_BINS_FIELD_NUMBER: _ClassVar[int]
    IS_CATEGORICAL_FIELD_NUMBER: _ClassVar[int]
    PENDING_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    numerical_bins: _containers.RepeatedCompositeFieldContainer[HistogramResponse.NumericalHistogramBin]
    categorical_bins: _containers.RepeatedCompositeFieldContainer[HistogramResponse.CategoricalHistogramBin]
    is_categorical: bool
    pending_operations: PendingOperations
    def __init__(self, numerical_bins: _Optional[_Iterable[_Union[HistogramResponse.NumericalHistogramBin, _Mapping]]] = ..., categorical_bins: _Optional[_Iterable[_Union[HistogramResponse.CategoricalHistogramBin, _Mapping]]] = ..., is_categorical: bool = ..., pending_operations: _Optional[_Union[PendingOperations, _Mapping]] = ...) -> None: ...
