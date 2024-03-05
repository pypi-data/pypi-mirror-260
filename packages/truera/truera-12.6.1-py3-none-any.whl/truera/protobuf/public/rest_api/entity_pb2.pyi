from google.api import annotations_pb2 as _annotations_pb2
from google.api import visibility_pb2 as _visibility_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from truera.protobuf.public.common import ingestion_schema_pb2 as _ingestion_schema_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CredentialType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[CredentialType]
    SECRET_KEY: _ClassVar[CredentialType]
    AWS_IAM_ROLE: _ClassVar[CredentialType]
UNSPECIFIED: CredentialType
SECRET_KEY: CredentialType
AWS_IAM_ROLE: CredentialType

class Project(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class CreateProjectRequest(_message.Message):
    __slots__ = ("name", "score_type", "input_type", "workspace_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    INPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    score_type: str
    input_type: str
    workspace_id: str
    def __init__(self, name: _Optional[str] = ..., score_type: _Optional[str] = ..., input_type: _Optional[str] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class ListProjectsRequest(_message.Message):
    __slots__ = ("workspace_id",)
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    def __init__(self, workspace_id: _Optional[str] = ...) -> None: ...

class ListProjectsResponse(_message.Message):
    __slots__ = ("projects",)
    PROJECTS_FIELD_NUMBER: _ClassVar[int]
    projects: _containers.RepeatedCompositeFieldContainer[Project]
    def __init__(self, projects: _Optional[_Iterable[_Union[Project, _Mapping]]] = ...) -> None: ...

class GetProjectRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class DeleteProjectRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class DeleteProjectResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DataCollection(_message.Message):
    __slots__ = ("id", "name", "project_id", "schema")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    project_id: str
    schema: _ingestion_schema_pb2.Schema
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., project_id: _Optional[str] = ..., schema: _Optional[_Union[_ingestion_schema_pb2.Schema, _Mapping]] = ...) -> None: ...

class CreateDataCollectionRequest(_message.Message):
    __slots__ = ("project_id", "name", "schema")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    name: str
    schema: _ingestion_schema_pb2.Schema
    def __init__(self, project_id: _Optional[str] = ..., name: _Optional[str] = ..., schema: _Optional[_Union[_ingestion_schema_pb2.Schema, _Mapping]] = ...) -> None: ...

class ListDataCollectionsRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class ListDataCollectionsResponse(_message.Message):
    __slots__ = ("data_collections",)
    DATA_COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    data_collections: _containers.RepeatedCompositeFieldContainer[DataCollection]
    def __init__(self, data_collections: _Optional[_Iterable[_Union[DataCollection, _Mapping]]] = ...) -> None: ...

class GetDataCollectionRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ...) -> None: ...

class DeleteDataCollectionRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ...) -> None: ...

class DeleteDataCollectionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Model(_message.Message):
    __slots__ = ("id", "name", "project_id", "data_collection_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    project_id: str
    data_collection_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ...) -> None: ...

class CreateModelRequest(_message.Message):
    __slots__ = ("project_id", "name", "data_collection_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    name: str
    data_collection_id: str
    def __init__(self, project_id: _Optional[str] = ..., name: _Optional[str] = ..., data_collection_id: _Optional[str] = ...) -> None: ...

class ListModelsRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class ListModelsResponse(_message.Message):
    __slots__ = ("models",)
    MODELS_FIELD_NUMBER: _ClassVar[int]
    models: _containers.RepeatedCompositeFieldContainer[Model]
    def __init__(self, models: _Optional[_Iterable[_Union[Model, _Mapping]]] = ...) -> None: ...

class GetModelRequest(_message.Message):
    __slots__ = ("project_id", "model_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_id: str
    def __init__(self, project_id: _Optional[str] = ..., model_id: _Optional[str] = ...) -> None: ...

class DeleteModelRequest(_message.Message):
    __slots__ = ("project_id", "model_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_id: str
    def __init__(self, project_id: _Optional[str] = ..., model_id: _Optional[str] = ...) -> None: ...

class DeleteModelResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Credential(_message.Message):
    __slots__ = ("type", "identity", "secret", "token")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    type: CredentialType
    identity: str
    secret: str
    token: str
    def __init__(self, type: _Optional[_Union[CredentialType, str]] = ..., identity: _Optional[str] = ..., secret: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class CreateCredentialRequest(_message.Message):
    __slots__ = ("name", "credential")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    name: str
    credential: Credential
    def __init__(self, name: _Optional[str] = ..., credential: _Optional[_Union[Credential, _Mapping]] = ...) -> None: ...

class ListCredentialsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCredentialsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetCredentialRequest(_message.Message):
    __slots__ = ("credential_id",)
    CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    credential_id: str
    def __init__(self, credential_id: _Optional[str] = ...) -> None: ...

class UpdateCredentialRequest(_message.Message):
    __slots__ = ("credential_id", "credential")
    CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    credential_id: str
    credential: Credential
    def __init__(self, credential_id: _Optional[str] = ..., credential: _Optional[_Union[Credential, _Mapping]] = ...) -> None: ...

class DeleteCredentialRequest(_message.Message):
    __slots__ = ("credential_id",)
    CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    credential_id: str
    def __init__(self, credential_id: _Optional[str] = ...) -> None: ...

class DeleteCredentialResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DataSplit(_message.Message):
    __slots__ = ("id", "name", "project_id", "data_collection_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    project_id: str
    data_collection_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ...) -> None: ...

class CreateDataSplitRequest(_message.Message):
    __slots__ = ("project_id", "name", "data_collection_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    name: str
    data_collection_id: str
    def __init__(self, project_id: _Optional[str] = ..., name: _Optional[str] = ..., data_collection_id: _Optional[str] = ...) -> None: ...

class ListDataSplitsRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ...) -> None: ...

class ListDataSplitsResponse(_message.Message):
    __slots__ = ("data_splits",)
    DATA_SPLITS_FIELD_NUMBER: _ClassVar[int]
    data_splits: _containers.RepeatedCompositeFieldContainer[DataSplit]
    def __init__(self, data_splits: _Optional[_Iterable[_Union[DataSplit, _Mapping]]] = ...) -> None: ...

class GetDataSplitRequest(_message.Message):
    __slots__ = ("project_id", "data_split_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_split_id: str
    def __init__(self, project_id: _Optional[str] = ..., data_split_id: _Optional[str] = ...) -> None: ...

class DeleteDataSplitRequest(_message.Message):
    __slots__ = ("project_id", "data_split_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_split_id: str
    def __init__(self, project_id: _Optional[str] = ..., data_split_id: _Optional[str] = ...) -> None: ...

class DeleteDataSplitResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
