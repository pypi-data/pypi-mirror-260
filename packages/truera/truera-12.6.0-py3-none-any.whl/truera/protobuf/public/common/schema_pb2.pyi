from truera.protobuf.public.common import data_kind_pb2 as _data_kind_pb2
from truera.protobuf.public.util import data_type_pb2 as _data_type_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SchemaType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID: _ClassVar[SchemaType]
    INPUT: _ClassVar[SchemaType]
    OUTPUT: _ClassVar[SchemaType]
INVALID: SchemaType
INPUT: SchemaType
OUTPUT: SchemaType

class ColumnDetails(_message.Message):
    __slots__ = ("name", "data_type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    data_type: _data_type_pb2.DataType
    def __init__(self, name: _Optional[str] = ..., data_type: _Optional[_Union[_data_type_pb2.DataType, _Mapping]] = ...) -> None: ...

class Schema(_message.Message):
    __slots__ = ("id", "project_id", "data_collection_id", "data_kind", "column_details")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_KIND_FIELD_NUMBER: _ClassVar[int]
    COLUMN_DETAILS_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    data_collection_id: str
    data_kind: _data_kind_pb2.DataKindDescribed
    column_details: _containers.RepeatedCompositeFieldContainer[ColumnDetails]
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., data_kind: _Optional[_Union[_data_kind_pb2.DataKindDescribed, str]] = ..., column_details: _Optional[_Iterable[_Union[ColumnDetails, _Mapping]]] = ...) -> None: ...

class SchemaCollection(_message.Message):
    __slots__ = ("schemas",)
    SCHEMAS_FIELD_NUMBER: _ClassVar[int]
    schemas: _containers.RepeatedCompositeFieldContainer[Schema]
    def __init__(self, schemas: _Optional[_Iterable[_Union[Schema, _Mapping]]] = ...) -> None: ...
