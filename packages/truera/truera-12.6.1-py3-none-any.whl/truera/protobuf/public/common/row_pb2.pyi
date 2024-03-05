from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from truera.protobuf.public.common import schema_pb2 as _schema_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SchemaEmbeddedRow(_message.Message):
    __slots__ = ("schema", "rows")
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    schema: _containers.RepeatedCompositeFieldContainer[_schema_pb2.ColumnDetails]
    rows: _containers.RepeatedCompositeFieldContainer[Row]
    def __init__(self, schema: _Optional[_Iterable[_Union[_schema_pb2.ColumnDetails, _Mapping]]] = ..., rows: _Optional[_Iterable[_Union[Row, _Mapping]]] = ...) -> None: ...

class Row(_message.Message):
    __slots__ = ("index", "columns")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    index: int
    columns: _containers.RepeatedCompositeFieldContainer[ColumnValue]
    def __init__(self, index: _Optional[int] = ..., columns: _Optional[_Iterable[_Union[ColumnValue, _Mapping]]] = ...) -> None: ...

class ColumnValue(_message.Message):
    __slots__ = ("column_index", "bool_value", "byte_value", "double_value", "float_value", "int_value", "long_value", "short_value", "string_value", "timestamp_value", "null_indicator", "array_value", "coerced_binary_value", "bytes_value")
    COLUMN_INDEX_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    BYTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    LONG_VALUE_FIELD_NUMBER: _ClassVar[int]
    SHORT_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_VALUE_FIELD_NUMBER: _ClassVar[int]
    NULL_INDICATOR_FIELD_NUMBER: _ClassVar[int]
    ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    COERCED_BINARY_VALUE_FIELD_NUMBER: _ClassVar[int]
    BYTES_VALUE_FIELD_NUMBER: _ClassVar[int]
    column_index: int
    bool_value: bool
    byte_value: int
    double_value: float
    float_value: float
    int_value: int
    long_value: int
    short_value: int
    string_value: str
    timestamp_value: _timestamp_pb2.Timestamp
    null_indicator: _struct_pb2.NullValue
    array_value: ArrayValue
    coerced_binary_value: str
    bytes_value: bytes
    def __init__(self, column_index: _Optional[int] = ..., bool_value: bool = ..., byte_value: _Optional[int] = ..., double_value: _Optional[float] = ..., float_value: _Optional[float] = ..., int_value: _Optional[int] = ..., long_value: _Optional[int] = ..., short_value: _Optional[int] = ..., string_value: _Optional[str] = ..., timestamp_value: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., null_indicator: _Optional[_Union[_struct_pb2.NullValue, str]] = ..., array_value: _Optional[_Union[ArrayValue, _Mapping]] = ..., coerced_binary_value: _Optional[str] = ..., bytes_value: _Optional[bytes] = ...) -> None: ...

class IntArrayValue(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class LongArrayValue(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class FloatArrayValue(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, values: _Optional[_Iterable[float]] = ...) -> None: ...

class DoubleArrayValue(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, values: _Optional[_Iterable[float]] = ...) -> None: ...

class StringArrayValue(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class NestedArrayValue(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[ArrayValue]
    def __init__(self, values: _Optional[_Iterable[_Union[ArrayValue, _Mapping]]] = ...) -> None: ...

class ArrayValue(_message.Message):
    __slots__ = ("double", "float", "int", "long", "string", "nested")
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    LONG_FIELD_NUMBER: _ClassVar[int]
    STRING_FIELD_NUMBER: _ClassVar[int]
    NESTED_FIELD_NUMBER: _ClassVar[int]
    double: DoubleArrayValue
    float: FloatArrayValue
    int: IntArrayValue
    long: LongArrayValue
    string: StringArrayValue
    nested: NestedArrayValue
    def __init__(self, double: _Optional[_Union[DoubleArrayValue, _Mapping]] = ..., float: _Optional[_Union[FloatArrayValue, _Mapping]] = ..., int: _Optional[_Union[IntArrayValue, _Mapping]] = ..., long: _Optional[_Union[LongArrayValue, _Mapping]] = ..., string: _Optional[_Union[StringArrayValue, _Mapping]] = ..., nested: _Optional[_Union[NestedArrayValue, _Mapping]] = ...) -> None: ...
