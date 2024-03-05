from google.api import annotations_pb2 as _annotations_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModelSourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MS_INVALID: _ClassVar[ModelSourceType]
    MS_SAGEMAKER: _ClassVar[ModelSourceType]
MS_INVALID: ModelSourceType
MS_SAGEMAKER: ModelSourceType

class LoadModelRequest(_message.Message):
    __slots__ = ("name", "project_id", "data_collection_id", "credential_id", "source")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    name: str
    project_id: str
    data_collection_id: str
    credential_id: str
    source: ModelSource
    def __init__(self, name: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., credential_id: _Optional[str] = ..., source: _Optional[_Union[ModelSource, _Mapping]] = ...) -> None: ...

class LoadModelResponse(_message.Message):
    __slots__ = ("model_id",)
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    def __init__(self, model_id: _Optional[str] = ...) -> None: ...

class ModelSource(_message.Message):
    __slots__ = ("uri", "type")
    URI_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    uri: str
    type: ModelSourceType
    def __init__(self, uri: _Optional[str] = ..., type: _Optional[_Union[ModelSourceType, str]] = ...) -> None: ...
