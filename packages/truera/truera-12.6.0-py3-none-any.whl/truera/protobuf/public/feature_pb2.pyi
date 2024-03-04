from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from truera.protobuf.public.util import data_type_pb2 as _data_type_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FeatureList(_message.Message):
    __slots__ = ("id", "project_id", "data_collection_id", "features", "created_at", "missing_values")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MISSING_VALUES_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    data_collection_id: str
    features: _containers.RepeatedCompositeFieldContainer[Feature]
    created_at: _timestamp_pb2.Timestamp
    missing_values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., features: _Optional[_Iterable[_Union[Feature, _Mapping]]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., missing_values: _Optional[_Iterable[str]] = ...) -> None: ...

class Feature(_message.Message):
    __slots__ = ("id", "name", "description", "groups", "derived_model_readable_columns", "data_type", "is_index_column", "special_values", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    DERIVED_MODEL_READABLE_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_INDEX_COLUMN_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_VALUES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    groups: _containers.RepeatedScalarFieldContainer[str]
    derived_model_readable_columns: _containers.RepeatedScalarFieldContainer[str]
    data_type: _data_type_pb2.DataType
    is_index_column: bool
    special_values: _containers.RepeatedCompositeFieldContainer[SpecialValue]
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., groups: _Optional[_Iterable[str]] = ..., derived_model_readable_columns: _Optional[_Iterable[str]] = ..., data_type: _Optional[_Union[_data_type_pb2.DataType, _Mapping]] = ..., is_index_column: bool = ..., special_values: _Optional[_Iterable[_Union[SpecialValue, _Mapping]]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SpecialValue(_message.Message):
    __slots__ = ("value", "description")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    value: _struct_pb2.Value
    description: str
    def __init__(self, value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., description: _Optional[str] = ...) -> None: ...
