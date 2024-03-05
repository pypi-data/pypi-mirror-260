from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DimensionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIMENSION_TYPE_UNSPECIFIED: _ClassVar[DimensionType]
    DIMENSION_TYPE_STRING: _ClassVar[DimensionType]
    DIMENSION_TYPE_LONG: _ClassVar[DimensionType]
    DIMENSION_TYPE_FLOAT: _ClassVar[DimensionType]
    DIMENSION_TYPE_DOUBLE: _ClassVar[DimensionType]

class MultiValueHandling(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MULTI_VALUE_UNSPECIFIED: _ClassVar[MultiValueHandling]
    MULTI_VALUE_SORTED_ARRAY: _ClassVar[MultiValueHandling]
    MULTI_VALUE_SORTED_SET: _ClassVar[MultiValueHandling]
    MULTI_VALUE_ARRAY: _ClassVar[MultiValueHandling]

class ExactAggregatorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EXACT_AGGREGATOR_TYPE_UNSPECIFIED: _ClassVar[ExactAggregatorType]
    EXACT_AGGREGATOR_TYPE_LONG_SUM: _ClassVar[ExactAggregatorType]
    EXACT_AGGREGATOR_TYPE_DOUBLE_SUM: _ClassVar[ExactAggregatorType]
    EXACT_AGGREGATOR_TYPE_FLOAT_SUM: _ClassVar[ExactAggregatorType]
    EXACT_AGGREGATOR_TYPE_LONG_MIN: _ClassVar[ExactAggregatorType]
    EXACT_AGGREGATOR_TYPE_LONG_MAX: _ClassVar[ExactAggregatorType]
    EXACT_AGGREGATOR_TYPE_DOUBLE_MIN: _ClassVar[ExactAggregatorType]
    EXACT_AGGREGATOR_TYPE_DOUBLE_MAX: _ClassVar[ExactAggregatorType]
    EXACT_AGGREGATOR_TYPE_FLOAT_MIN: _ClassVar[ExactAggregatorType]
    EXACT_AGGREGATOR_TYPE_FLOAT_MAX: _ClassVar[ExactAggregatorType]

class FirstLastAggregatorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FIRST_LAST_AGGREGATOR_TYPE_UNSPECIFIED: _ClassVar[FirstLastAggregatorType]
    FIRST_LAST_AGGREGATOR_TYPE_STRING_FIRST: _ClassVar[FirstLastAggregatorType]
    FIRST_LAST_AGGREGATOR_TYPE_STRING_LAST: _ClassVar[FirstLastAggregatorType]

class Granularity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GRANULARITY_UNSPECIFIED: _ClassVar[Granularity]
    GRANULARITY_ALL: _ClassVar[Granularity]
    GRANULARITY_SECOND: _ClassVar[Granularity]
    GRANULARITY_MINUTE: _ClassVar[Granularity]
    GRANULARITY_15_MINUTE: _ClassVar[Granularity]
    GRANULARITY_30_MINUTE: _ClassVar[Granularity]
    GRANULARITY_HOUR: _ClassVar[Granularity]
    GRANULARITY_DAY: _ClassVar[Granularity]
    GRANULARITY_WEEK: _ClassVar[Granularity]
    GRANULARITY_MONTH: _ClassVar[Granularity]
    GRANULARITY_QUARTER: _ClassVar[Granularity]
    GRANULARITY_YEAR: _ClassVar[Granularity]
    GRANULARITY_NONE: _ClassVar[Granularity]
DIMENSION_TYPE_UNSPECIFIED: DimensionType
DIMENSION_TYPE_STRING: DimensionType
DIMENSION_TYPE_LONG: DimensionType
DIMENSION_TYPE_FLOAT: DimensionType
DIMENSION_TYPE_DOUBLE: DimensionType
MULTI_VALUE_UNSPECIFIED: MultiValueHandling
MULTI_VALUE_SORTED_ARRAY: MultiValueHandling
MULTI_VALUE_SORTED_SET: MultiValueHandling
MULTI_VALUE_ARRAY: MultiValueHandling
EXACT_AGGREGATOR_TYPE_UNSPECIFIED: ExactAggregatorType
EXACT_AGGREGATOR_TYPE_LONG_SUM: ExactAggregatorType
EXACT_AGGREGATOR_TYPE_DOUBLE_SUM: ExactAggregatorType
EXACT_AGGREGATOR_TYPE_FLOAT_SUM: ExactAggregatorType
EXACT_AGGREGATOR_TYPE_LONG_MIN: ExactAggregatorType
EXACT_AGGREGATOR_TYPE_LONG_MAX: ExactAggregatorType
EXACT_AGGREGATOR_TYPE_DOUBLE_MIN: ExactAggregatorType
EXACT_AGGREGATOR_TYPE_DOUBLE_MAX: ExactAggregatorType
EXACT_AGGREGATOR_TYPE_FLOAT_MIN: ExactAggregatorType
EXACT_AGGREGATOR_TYPE_FLOAT_MAX: ExactAggregatorType
FIRST_LAST_AGGREGATOR_TYPE_UNSPECIFIED: FirstLastAggregatorType
FIRST_LAST_AGGREGATOR_TYPE_STRING_FIRST: FirstLastAggregatorType
FIRST_LAST_AGGREGATOR_TYPE_STRING_LAST: FirstLastAggregatorType
GRANULARITY_UNSPECIFIED: Granularity
GRANULARITY_ALL: Granularity
GRANULARITY_SECOND: Granularity
GRANULARITY_MINUTE: Granularity
GRANULARITY_15_MINUTE: Granularity
GRANULARITY_30_MINUTE: Granularity
GRANULARITY_HOUR: Granularity
GRANULARITY_DAY: Granularity
GRANULARITY_WEEK: Granularity
GRANULARITY_MONTH: Granularity
GRANULARITY_QUARTER: Granularity
GRANULARITY_YEAR: Granularity
GRANULARITY_NONE: Granularity

class DataSchema(_message.Message):
    __slots__ = ("data_source_name", "timestamp_spec", "dimensions_spec", "metrics_spec", "granularity_spec", "transform_spec")
    DATA_SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_SPEC_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_SPEC_FIELD_NUMBER: _ClassVar[int]
    METRICS_SPEC_FIELD_NUMBER: _ClassVar[int]
    GRANULARITY_SPEC_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_SPEC_FIELD_NUMBER: _ClassVar[int]
    data_source_name: str
    timestamp_spec: TimestampSpec
    dimensions_spec: DimensionsSpec
    metrics_spec: MetricsSpec
    granularity_spec: GranularitySpec
    transform_spec: TransformSpec
    def __init__(self, data_source_name: _Optional[str] = ..., timestamp_spec: _Optional[_Union[TimestampSpec, _Mapping]] = ..., dimensions_spec: _Optional[_Union[DimensionsSpec, _Mapping]] = ..., metrics_spec: _Optional[_Union[MetricsSpec, _Mapping]] = ..., granularity_spec: _Optional[_Union[GranularitySpec, _Mapping]] = ..., transform_spec: _Optional[_Union[TransformSpec, _Mapping]] = ...) -> None: ...

class TimestampSpec(_message.Message):
    __slots__ = ("timestamp_field_name", "missing_value")
    TIMESTAMP_FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    MISSING_VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp_field_name: str
    missing_value: _timestamp_pb2.Timestamp
    def __init__(self, timestamp_field_name: _Optional[str] = ..., missing_value: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DimensionsSpec(_message.Message):
    __slots__ = ("dimensions", "dimension_exclusions")
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_EXCLUSIONS_FIELD_NUMBER: _ClassVar[int]
    dimensions: _containers.RepeatedCompositeFieldContainer[Dimension]
    dimension_exclusions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, dimensions: _Optional[_Iterable[_Union[Dimension, _Mapping]]] = ..., dimension_exclusions: _Optional[_Iterable[str]] = ...) -> None: ...

class Dimension(_message.Message):
    __slots__ = ("type", "name", "create_bitmap_index", "multi_value_handling")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATE_BITMAP_INDEX_FIELD_NUMBER: _ClassVar[int]
    MULTI_VALUE_HANDLING_FIELD_NUMBER: _ClassVar[int]
    type: DimensionType
    name: str
    create_bitmap_index: bool
    multi_value_handling: MultiValueHandling
    def __init__(self, type: _Optional[_Union[DimensionType, str]] = ..., name: _Optional[str] = ..., create_bitmap_index: bool = ..., multi_value_handling: _Optional[_Union[MultiValueHandling, str]] = ...) -> None: ...

class MetricsSpec(_message.Message):
    __slots__ = ("exact_aggregators", "first_last_aggregators", "quantile_sketch_aggregators", "count_aggregator")
    EXACT_AGGREGATORS_FIELD_NUMBER: _ClassVar[int]
    FIRST_LAST_AGGREGATORS_FIELD_NUMBER: _ClassVar[int]
    QUANTILE_SKETCH_AGGREGATORS_FIELD_NUMBER: _ClassVar[int]
    COUNT_AGGREGATOR_FIELD_NUMBER: _ClassVar[int]
    exact_aggregators: _containers.RepeatedCompositeFieldContainer[ExactAggregator]
    first_last_aggregators: _containers.RepeatedCompositeFieldContainer[FirstLastAggregator]
    quantile_sketch_aggregators: _containers.RepeatedCompositeFieldContainer[QuantileSketchAggregator]
    count_aggregator: CountAggregator
    def __init__(self, exact_aggregators: _Optional[_Iterable[_Union[ExactAggregator, _Mapping]]] = ..., first_last_aggregators: _Optional[_Iterable[_Union[FirstLastAggregator, _Mapping]]] = ..., quantile_sketch_aggregators: _Optional[_Iterable[_Union[QuantileSketchAggregator, _Mapping]]] = ..., count_aggregator: _Optional[_Union[CountAggregator, _Mapping]] = ...) -> None: ...

class ExactAggregator(_message.Message):
    __slots__ = ("type", "output_field_name", "input_field_name")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    type: ExactAggregatorType
    output_field_name: str
    input_field_name: str
    def __init__(self, type: _Optional[_Union[ExactAggregatorType, str]] = ..., output_field_name: _Optional[str] = ..., input_field_name: _Optional[str] = ...) -> None: ...

class FirstLastAggregator(_message.Message):
    __slots__ = ("type", "output_field_name", "input_field_name", "time_field_name")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    type: FirstLastAggregatorType
    output_field_name: str
    input_field_name: str
    time_field_name: str
    def __init__(self, type: _Optional[_Union[FirstLastAggregatorType, str]] = ..., output_field_name: _Optional[str] = ..., input_field_name: _Optional[str] = ..., time_field_name: _Optional[str] = ...) -> None: ...

class QuantileSketchAggregator(_message.Message):
    __slots__ = ("output_field_name", "input_field_name", "k", "max_stream_length")
    OUTPUT_FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    K_FIELD_NUMBER: _ClassVar[int]
    MAX_STREAM_LENGTH_FIELD_NUMBER: _ClassVar[int]
    output_field_name: str
    input_field_name: str
    k: int
    max_stream_length: int
    def __init__(self, output_field_name: _Optional[str] = ..., input_field_name: _Optional[str] = ..., k: _Optional[int] = ..., max_stream_length: _Optional[int] = ...) -> None: ...

class CountAggregator(_message.Message):
    __slots__ = ("output_field_name",)
    OUTPUT_FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    output_field_name: str
    def __init__(self, output_field_name: _Optional[str] = ...) -> None: ...

class GranularitySpec(_message.Message):
    __slots__ = ("segment_granularity", "query_granularity", "rollup")
    SEGMENT_GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    QUERY_GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    ROLLUP_FIELD_NUMBER: _ClassVar[int]
    segment_granularity: Granularity
    query_granularity: Granularity
    rollup: bool
    def __init__(self, segment_granularity: _Optional[_Union[Granularity, str]] = ..., query_granularity: _Optional[_Union[Granularity, str]] = ..., rollup: bool = ...) -> None: ...

class TransformSpec(_message.Message):
    __slots__ = ("transforms", "string_selector_filters")
    TRANSFORMS_FIELD_NUMBER: _ClassVar[int]
    STRING_SELECTOR_FILTERS_FIELD_NUMBER: _ClassVar[int]
    transforms: _containers.RepeatedCompositeFieldContainer[InputTransform]
    string_selector_filters: _containers.RepeatedCompositeFieldContainer[StringSelectorFilter]
    def __init__(self, transforms: _Optional[_Iterable[_Union[InputTransform, _Mapping]]] = ..., string_selector_filters: _Optional[_Iterable[_Union[StringSelectorFilter, _Mapping]]] = ...) -> None: ...

class StringSelectorFilter(_message.Message):
    __slots__ = ("dimension", "value")
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dimension: str
    value: str
    def __init__(self, dimension: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class InputTransform(_message.Message):
    __slots__ = ("output_field_name", "expression")
    OUTPUT_FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    output_field_name: str
    expression: str
    def __init__(self, output_field_name: _Optional[str] = ..., expression: _Optional[str] = ...) -> None: ...
