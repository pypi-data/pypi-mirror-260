from google.protobuf import struct_pb2 as _struct_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FilterExpressionOperator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[FilterExpressionOperator]
    FEO_AND: _ClassVar[FilterExpressionOperator]
    FEO_OR: _ClassVar[FilterExpressionOperator]
    FEO_NOT: _ClassVar[FilterExpressionOperator]
UNKNOWN: FilterExpressionOperator
FEO_AND: FilterExpressionOperator
FEO_OR: FilterExpressionOperator
FEO_NOT: FilterExpressionOperator

class FilterExpression(_message.Message):
    __slots__ = ("filter_leaf", "operator", "sub_expressions")
    FILTER_LEAF_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    SUB_EXPRESSIONS_FIELD_NUMBER: _ClassVar[int]
    filter_leaf: FilterLeaf
    operator: FilterExpressionOperator
    sub_expressions: _containers.RepeatedCompositeFieldContainer[FilterExpression]
    def __init__(self, filter_leaf: _Optional[_Union[FilterLeaf, _Mapping]] = ..., operator: _Optional[_Union[FilterExpressionOperator, str]] = ..., sub_expressions: _Optional[_Iterable[_Union[FilterExpression, _Mapping]]] = ...) -> None: ...

class FilterLeaf(_message.Message):
    __slots__ = ("value_type", "column_name", "segmentation_id", "score_type", "model_id", "filter_type", "values", "range_options")
    class FilterLeafValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[FilterLeaf.FilterLeafValueType]
        COLUMN_VALUE: _ClassVar[FilterLeaf.FilterLeafValueType]
        OUTPUT: _ClassVar[FilterLeaf.FilterLeafValueType]
        GROUND_TRUTH: _ClassVar[FilterLeaf.FilterLeafValueType]
        GROUND_TRUTH_CONFORMANCE: _ClassVar[FilterLeaf.FilterLeafValueType]
        SEGMENT: _ClassVar[FilterLeaf.FilterLeafValueType]
        INDEX: _ClassVar[FilterLeaf.FilterLeafValueType]
        RANKING_GROUP_ID: _ClassVar[FilterLeaf.FilterLeafValueType]
    UNKNOWN: FilterLeaf.FilterLeafValueType
    COLUMN_VALUE: FilterLeaf.FilterLeafValueType
    OUTPUT: FilterLeaf.FilterLeafValueType
    GROUND_TRUTH: FilterLeaf.FilterLeafValueType
    GROUND_TRUTH_CONFORMANCE: FilterLeaf.FilterLeafValueType
    SEGMENT: FilterLeaf.FilterLeafValueType
    INDEX: FilterLeaf.FilterLeafValueType
    RANKING_GROUP_ID: FilterLeaf.FilterLeafValueType
    class FilterLeafComparisonType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FilterLeafComparisonType_UNKNOWN: _ClassVar[FilterLeaf.FilterLeafComparisonType]
        EQUALS: _ClassVar[FilterLeaf.FilterLeafComparisonType]
        NOT_EQUALS: _ClassVar[FilterLeaf.FilterLeafComparisonType]
        LESS_THAN: _ClassVar[FilterLeaf.FilterLeafComparisonType]
        LESS_THAN_EQUAL_TO: _ClassVar[FilterLeaf.FilterLeafComparisonType]
        GREATER_THAN: _ClassVar[FilterLeaf.FilterLeafComparisonType]
        GREATER_THAN_EQUAL_TO: _ClassVar[FilterLeaf.FilterLeafComparisonType]
        IN_LIST: _ClassVar[FilterLeaf.FilterLeafComparisonType]
        NOT_IN_LIST: _ClassVar[FilterLeaf.FilterLeafComparisonType]
        IN_RANGE: _ClassVar[FilterLeaf.FilterLeafComparisonType]
        NOT_IN_RANGE: _ClassVar[FilterLeaf.FilterLeafComparisonType]
    FilterLeafComparisonType_UNKNOWN: FilterLeaf.FilterLeafComparisonType
    EQUALS: FilterLeaf.FilterLeafComparisonType
    NOT_EQUALS: FilterLeaf.FilterLeafComparisonType
    LESS_THAN: FilterLeaf.FilterLeafComparisonType
    LESS_THAN_EQUAL_TO: FilterLeaf.FilterLeafComparisonType
    GREATER_THAN: FilterLeaf.FilterLeafComparisonType
    GREATER_THAN_EQUAL_TO: FilterLeaf.FilterLeafComparisonType
    IN_LIST: FilterLeaf.FilterLeafComparisonType
    NOT_IN_LIST: FilterLeaf.FilterLeafComparisonType
    IN_RANGE: FilterLeaf.FilterLeafComparisonType
    NOT_IN_RANGE: FilterLeaf.FilterLeafComparisonType
    class RangeOptions(_message.Message):
        __slots__ = ("lowerStrict", "upperStrict")
        LOWERSTRICT_FIELD_NUMBER: _ClassVar[int]
        UPPERSTRICT_FIELD_NUMBER: _ClassVar[int]
        lowerStrict: bool
        upperStrict: bool
        def __init__(self, lowerStrict: bool = ..., upperStrict: bool = ...) -> None: ...
    VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    SEGMENTATION_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    FILTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    RANGE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    value_type: FilterLeaf.FilterLeafValueType
    column_name: str
    segmentation_id: str
    score_type: int
    model_id: str
    filter_type: FilterLeaf.FilterLeafComparisonType
    values: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Value]
    range_options: FilterLeaf.RangeOptions
    def __init__(self, value_type: _Optional[_Union[FilterLeaf.FilterLeafValueType, str]] = ..., column_name: _Optional[str] = ..., segmentation_id: _Optional[str] = ..., score_type: _Optional[int] = ..., model_id: _Optional[str] = ..., filter_type: _Optional[_Union[FilterLeaf.FilterLeafComparisonType, str]] = ..., values: _Optional[_Iterable[_Union[_struct_pb2.Value, _Mapping]]] = ..., range_options: _Optional[_Union[FilterLeaf.RangeOptions, _Mapping]] = ...) -> None: ...
