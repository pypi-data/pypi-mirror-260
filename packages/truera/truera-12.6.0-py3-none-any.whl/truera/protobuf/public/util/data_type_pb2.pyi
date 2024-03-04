from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StaticDataTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID: _ClassVar[StaticDataTypeEnum]
    STRING: _ClassVar[StaticDataTypeEnum]
    BOOL: _ClassVar[StaticDataTypeEnum]
    INT8: _ClassVar[StaticDataTypeEnum]
    INT16: _ClassVar[StaticDataTypeEnum]
    INT32: _ClassVar[StaticDataTypeEnum]
    INT64: _ClassVar[StaticDataTypeEnum]
    INTPTR: _ClassVar[StaticDataTypeEnum]
    UINT8: _ClassVar[StaticDataTypeEnum]
    UINT16: _ClassVar[StaticDataTypeEnum]
    UINT32: _ClassVar[StaticDataTypeEnum]
    UINT64: _ClassVar[StaticDataTypeEnum]
    UINTPTR: _ClassVar[StaticDataTypeEnum]
    FLOAT32: _ClassVar[StaticDataTypeEnum]
    FLOAT64: _ClassVar[StaticDataTypeEnum]
    DATE: _ClassVar[StaticDataTypeEnum]
    DATETIME: _ClassVar[StaticDataTypeEnum]
    DATETIME64: _ClassVar[StaticDataTypeEnum]
    COMPLEXFLOAT32: _ClassVar[StaticDataTypeEnum]
    COMPLEXFLOAT64: _ClassVar[StaticDataTypeEnum]
    COERCEDBINARY: _ClassVar[StaticDataTypeEnum]
    BYTES: _ClassVar[StaticDataTypeEnum]
INVALID: StaticDataTypeEnum
STRING: StaticDataTypeEnum
BOOL: StaticDataTypeEnum
INT8: StaticDataTypeEnum
INT16: StaticDataTypeEnum
INT32: StaticDataTypeEnum
INT64: StaticDataTypeEnum
INTPTR: StaticDataTypeEnum
UINT8: StaticDataTypeEnum
UINT16: StaticDataTypeEnum
UINT32: StaticDataTypeEnum
UINT64: StaticDataTypeEnum
UINTPTR: StaticDataTypeEnum
FLOAT32: StaticDataTypeEnum
FLOAT64: StaticDataTypeEnum
DATE: StaticDataTypeEnum
DATETIME: StaticDataTypeEnum
DATETIME64: StaticDataTypeEnum
COMPLEXFLOAT32: StaticDataTypeEnum
COMPLEXFLOAT64: StaticDataTypeEnum
COERCEDBINARY: StaticDataTypeEnum
BYTES: StaticDataTypeEnum

class DataType(_message.Message):
    __slots__ = ("static_data_type", "parameterized_data_type", "integer_options_type", "string_options_type", "array_type")
    STATIC_DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARAMETERIZED_DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    INTEGER_OPTIONS_TYPE_FIELD_NUMBER: _ClassVar[int]
    STRING_OPTIONS_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARRAY_TYPE_FIELD_NUMBER: _ClassVar[int]
    static_data_type: StaticDataTypeEnum
    parameterized_data_type: ParameterizedDataType
    integer_options_type: DiscreteIntegerOptions
    string_options_type: DiscreteStringOptions
    array_type: ArrayType
    def __init__(self, static_data_type: _Optional[_Union[StaticDataTypeEnum, str]] = ..., parameterized_data_type: _Optional[_Union[ParameterizedDataType, _Mapping]] = ..., integer_options_type: _Optional[_Union[DiscreteIntegerOptions, _Mapping]] = ..., string_options_type: _Optional[_Union[DiscreteStringOptions, _Mapping]] = ..., array_type: _Optional[_Union[ArrayType, _Mapping]] = ...) -> None: ...

class ParameterizedDataType(_message.Message):
    __slots__ = ("decimal_type", "range_numeric_type")
    DECIMAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    RANGE_NUMERIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    decimal_type: Decimal
    range_numeric_type: RangeNumericType
    def __init__(self, decimal_type: _Optional[_Union[Decimal, _Mapping]] = ..., range_numeric_type: _Optional[_Union[RangeNumericType, _Mapping]] = ...) -> None: ...

class DiscreteIntegerOptions(_message.Message):
    __slots__ = ("possible_values",)
    POSSIBLE_VALUES_FIELD_NUMBER: _ClassVar[int]
    possible_values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, possible_values: _Optional[_Iterable[int]] = ...) -> None: ...

class DiscreteStringOptions(_message.Message):
    __slots__ = ("possible_values",)
    POSSIBLE_VALUES_FIELD_NUMBER: _ClassVar[int]
    possible_values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, possible_values: _Optional[_Iterable[str]] = ...) -> None: ...

class Decimal(_message.Message):
    __slots__ = ("precision", "scale")
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    precision: int
    scale: int
    def __init__(self, precision: _Optional[int] = ..., scale: _Optional[int] = ...) -> None: ...

class IntRangeType(_message.Message):
    __slots__ = ("min", "max")
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    min: int
    max: int
    def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...

class LongRangeType(_message.Message):
    __slots__ = ("min", "max")
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    min: int
    max: int
    def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...

class FloatRangeType(_message.Message):
    __slots__ = ("min", "max")
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    min: float
    max: float
    def __init__(self, min: _Optional[float] = ..., max: _Optional[float] = ...) -> None: ...

class DoubleRangeType(_message.Message):
    __slots__ = ("min", "max")
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    min: float
    max: float
    def __init__(self, min: _Optional[float] = ..., max: _Optional[float] = ...) -> None: ...

class RangeNumericType(_message.Message):
    __slots__ = ("int_range_type", "long_range_type", "float_range_type", "double_range_type")
    INT_RANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    LONG_RANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_RANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_RANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    int_range_type: IntRangeType
    long_range_type: LongRangeType
    float_range_type: FloatRangeType
    double_range_type: DoubleRangeType
    def __init__(self, int_range_type: _Optional[_Union[IntRangeType, _Mapping]] = ..., long_range_type: _Optional[_Union[LongRangeType, _Mapping]] = ..., float_range_type: _Optional[_Union[FloatRangeType, _Mapping]] = ..., double_range_type: _Optional[_Union[DoubleRangeType, _Mapping]] = ...) -> None: ...

class ArrayType(_message.Message):
    __slots__ = ("data_type",)
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    data_type: DataType
    def __init__(self, data_type: _Optional[_Union[DataType, _Mapping]] = ...) -> None: ...
