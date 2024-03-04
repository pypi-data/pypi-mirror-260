from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ColumnType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNTYPED: _ClassVar[ColumnType]
    INT: _ClassVar[ColumnType]
    BOOL: _ClassVar[ColumnType]
    FLOAT: _ClassVar[ColumnType]
    STRING: _ClassVar[ColumnType]
    EMBEDDING: _ClassVar[ColumnType]
    TOKENS: _ClassVar[ColumnType]

class OutputType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNDEFINED_OUTPUT_TYPE: _ClassVar[OutputType]
    PROBITS: _ClassVar[OutputType]
    LOGITS: _ClassVar[OutputType]
    REGRESSION: _ClassVar[OutputType]
    CLASSIFICATION: _ClassVar[OutputType]
UNTYPED: ColumnType
INT: ColumnType
BOOL: ColumnType
FLOAT: ColumnType
STRING: ColumnType
EMBEDDING: ColumnType
TOKENS: ColumnType
UNDEFINED_OUTPUT_TYPE: OutputType
PROBITS: OutputType
LOGITS: OutputType
REGRESSION: OutputType
CLASSIFICATION: OutputType

class Column(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: ColumnType
    def __init__(self, type: _Optional[_Union[ColumnType, str]] = ...) -> None: ...

class OutputColumn(_message.Message):
    __slots__ = ("output_type",)
    OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    output_type: OutputType
    def __init__(self, output_type: _Optional[_Union[OutputType, str]] = ...) -> None: ...

class Schema(_message.Message):
    __slots__ = ("id_column_name", "timestamp_column_name", "tags_column_name", "input_columns", "output_columns", "label_columns", "extra_columns", "post_data_columns")
    class InputColumnsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Column
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Column, _Mapping]] = ...) -> None: ...
    class OutputColumnsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: OutputColumn
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[OutputColumn, _Mapping]] = ...) -> None: ...
    class LabelColumnsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Column
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Column, _Mapping]] = ...) -> None: ...
    class ExtraColumnsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Column
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Column, _Mapping]] = ...) -> None: ...
    class PostDataColumnsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Column
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Column, _Mapping]] = ...) -> None: ...
    ID_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    LABEL_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    EXTRA_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    POST_DATA_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    id_column_name: str
    timestamp_column_name: str
    tags_column_name: str
    input_columns: _containers.MessageMap[str, Column]
    output_columns: _containers.MessageMap[str, OutputColumn]
    label_columns: _containers.MessageMap[str, Column]
    extra_columns: _containers.MessageMap[str, Column]
    post_data_columns: _containers.MessageMap[str, Column]
    def __init__(self, id_column_name: _Optional[str] = ..., timestamp_column_name: _Optional[str] = ..., tags_column_name: _Optional[str] = ..., input_columns: _Optional[_Mapping[str, Column]] = ..., output_columns: _Optional[_Mapping[str, OutputColumn]] = ..., label_columns: _Optional[_Mapping[str, Column]] = ..., extra_columns: _Optional[_Mapping[str, Column]] = ..., post_data_columns: _Optional[_Mapping[str, Column]] = ...) -> None: ...
