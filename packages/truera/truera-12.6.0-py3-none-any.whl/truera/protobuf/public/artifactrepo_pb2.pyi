from truera.protobuf.public import metadata_message_types_pb2 as _metadata_message_types_pb2
from truera.protobuf.public import feature_pb2 as _feature_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OperationState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID: _ClassVar[OperationState]
    ALLOWED: _ClassVar[OperationState]
    NOT_ALLOWED: _ClassVar[OperationState]

class ExistsResponseOption(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID_EXISTS_OPTION: _ClassVar[ExistsResponseOption]
    DOES_NOT_EXIST: _ClassVar[ExistsResponseOption]
    FILE_EXISTS: _ClassVar[ExistsResponseOption]
    DIRECTORY_EXISTS: _ClassVar[ExistsResponseOption]

class ArtifactType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID_ARTIFACT_TYPE: _ClassVar[ArtifactType]
    MODEL: _ClassVar[ArtifactType]
    DATACOLLECTION: _ClassVar[ArtifactType]
    DOCUMENTATION: _ClassVar[ArtifactType]
    DATASPLIT: _ClassVar[ArtifactType]
    PROJECT: _ClassVar[ArtifactType]
    FEATURE: _ClassVar[ArtifactType]
    FEATURE_LIST: _ClassVar[ArtifactType]
    DATA_SOURCE: _ClassVar[ArtifactType]
    MATERIALIZED_FILE: _ClassVar[ArtifactType]
    CACHE: _ClassVar[ArtifactType]
    CREDENTIALS: _ClassVar[ArtifactType]
    MODELTEST: _ClassVar[ArtifactType]
    FEEDBACK_FUNCTION: _ClassVar[ArtifactType]
INVALID: OperationState
ALLOWED: OperationState
NOT_ALLOWED: OperationState
INVALID_EXISTS_OPTION: ExistsResponseOption
DOES_NOT_EXIST: ExistsResponseOption
FILE_EXISTS: ExistsResponseOption
DIRECTORY_EXISTS: ExistsResponseOption
INVALID_ARTIFACT_TYPE: ArtifactType
MODEL: ArtifactType
DATACOLLECTION: ArtifactType
DOCUMENTATION: ArtifactType
DATASPLIT: ArtifactType
PROJECT: ArtifactType
FEATURE: ArtifactType
FEATURE_LIST: ArtifactType
DATA_SOURCE: ArtifactType
MATERIALIZED_FILE: ArtifactType
CACHE: ArtifactType
CREDENTIALS: ArtifactType
MODELTEST: ArtifactType
FEEDBACK_FUNCTION: ArtifactType

class PingRequest(_message.Message):
    __slots__ = ("test_string",)
    TEST_STRING_FIELD_NUMBER: _ClassVar[int]
    test_string: str
    def __init__(self, test_string: _Optional[str] = ...) -> None: ...

class PingRequestResponse(_message.Message):
    __slots__ = ("test_string_back", "cli_version")
    TEST_STRING_BACK_FIELD_NUMBER: _ClassVar[int]
    CLI_VERSION_FIELD_NUMBER: _ClassVar[int]
    test_string_back: str
    cli_version: str
    def __init__(self, test_string_back: _Optional[str] = ..., cli_version: _Optional[str] = ...) -> None: ...

class GetAllowedOperationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAllowedOperationsResponse(_message.Message):
    __slots__ = ("add", "delete", "get")
    ADD_FIELD_NUMBER: _ClassVar[int]
    DELETE_FIELD_NUMBER: _ClassVar[int]
    GET_FIELD_NUMBER: _ClassVar[int]
    add: OperationRules
    delete: OperationRules
    get: OperationRules
    def __init__(self, add: _Optional[_Union[OperationRules, _Mapping]] = ..., delete: _Optional[_Union[OperationRules, _Mapping]] = ..., get: _Optional[_Union[OperationRules, _Mapping]] = ...) -> None: ...

class OperationRules(_message.Message):
    __slots__ = ("project", "model", "virtual_model", "data_collection", "datasplit", "documentation")
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_MODEL_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    DATASPLIT_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTATION_FIELD_NUMBER: _ClassVar[int]
    project: OperationState
    model: OperationState
    virtual_model: OperationState
    data_collection: OperationState
    datasplit: OperationState
    documentation: OperationState
    def __init__(self, project: _Optional[_Union[OperationState, str]] = ..., model: _Optional[_Union[OperationState, str]] = ..., virtual_model: _Optional[_Union[OperationState, str]] = ..., data_collection: _Optional[_Union[OperationState, str]] = ..., datasplit: _Optional[_Union[OperationState, str]] = ..., documentation: _Optional[_Union[OperationState, str]] = ...) -> None: ...

class PutRequest(_message.Message):
    __slots__ = ("input_chunk", "project_id", "artifact_type", "artifact_id", "intra_artifact_path", "scoping_artifact_ids", "checksum")
    INPUT_CHUNK_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    INTRA_ARTIFACT_PATH_FIELD_NUMBER: _ClassVar[int]
    SCOPING_ARTIFACT_IDS_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    input_chunk: bytes
    project_id: str
    artifact_type: ArtifactType
    artifact_id: str
    intra_artifact_path: str
    scoping_artifact_ids: _containers.RepeatedScalarFieldContainer[str]
    checksum: ResourceChecksum
    def __init__(self, input_chunk: _Optional[bytes] = ..., project_id: _Optional[str] = ..., artifact_type: _Optional[_Union[ArtifactType, str]] = ..., artifact_id: _Optional[str] = ..., intra_artifact_path: _Optional[str] = ..., scoping_artifact_ids: _Optional[_Iterable[str]] = ..., checksum: _Optional[_Union[ResourceChecksum, _Mapping]] = ...) -> None: ...

class ResourceChecksum(_message.Message):
    __slots__ = ("type", "value")
    class ChecksumType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[ResourceChecksum.ChecksumType]
        MD5: _ClassVar[ResourceChecksum.ChecksumType]
    INVALID: ResourceChecksum.ChecksumType
    MD5: ResourceChecksum.ChecksumType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    type: ResourceChecksum.ChecksumType
    value: str
    def __init__(self, type: _Optional[_Union[ResourceChecksum.ChecksumType, str]] = ..., value: _Optional[str] = ...) -> None: ...

class PutRequestResponse(_message.Message):
    __slots__ = ("repo_artifact_path", "artifact_id")
    REPO_ARTIFACT_PATH_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    repo_artifact_path: str
    artifact_id: str
    def __init__(self, repo_artifact_path: _Optional[str] = ..., artifact_id: _Optional[str] = ...) -> None: ...

class PutMetadataRequest(_message.Message):
    __slots__ = ("project", "model", "data_collection", "split", "feature_list", "data_source", "cache", "feedback_function", "insert_only", "workspace_id")
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    SPLIT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_LIST_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    CACHE_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    INSERT_ONLY_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    project: _metadata_message_types_pb2.ProjectMetadata
    model: _metadata_message_types_pb2.ModelMetadata
    data_collection: _metadata_message_types_pb2.DataCollectionMetadata
    split: _metadata_message_types_pb2.DataSplitMetadata
    feature_list: _feature_pb2.FeatureList
    data_source: _metadata_message_types_pb2.DataSourceWrapper
    cache: _metadata_message_types_pb2.CacheMetadata
    feedback_function: _metadata_message_types_pb2.FeedbackFunctionMetadata
    insert_only: bool
    workspace_id: str
    def __init__(self, project: _Optional[_Union[_metadata_message_types_pb2.ProjectMetadata, _Mapping]] = ..., model: _Optional[_Union[_metadata_message_types_pb2.ModelMetadata, _Mapping]] = ..., data_collection: _Optional[_Union[_metadata_message_types_pb2.DataCollectionMetadata, _Mapping]] = ..., split: _Optional[_Union[_metadata_message_types_pb2.DataSplitMetadata, _Mapping]] = ..., feature_list: _Optional[_Union[_feature_pb2.FeatureList, _Mapping]] = ..., data_source: _Optional[_Union[_metadata_message_types_pb2.DataSourceWrapper, _Mapping]] = ..., cache: _Optional[_Union[_metadata_message_types_pb2.CacheMetadata, _Mapping]] = ..., feedback_function: _Optional[_Union[_metadata_message_types_pb2.FeedbackFunctionMetadata, _Mapping]] = ..., insert_only: bool = ..., workspace_id: _Optional[str] = ...) -> None: ...

class PutMetadataRequestResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class PutTimerangeSplitMetadataRequest(_message.Message):
    __slots__ = ("split", "insert_only", "model_id")
    SPLIT_FIELD_NUMBER: _ClassVar[int]
    INSERT_ONLY_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    split: _metadata_message_types_pb2.DataSplitMetadata
    insert_only: bool
    model_id: str
    def __init__(self, split: _Optional[_Union[_metadata_message_types_pb2.DataSplitMetadata, _Mapping]] = ..., insert_only: bool = ..., model_id: _Optional[str] = ...) -> None: ...

class PutTimerangeSplitMetadataResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ExistsRequest(_message.Message):
    __slots__ = ("project_id", "artifact_type", "artifact_id", "intra_artifact_path", "scoping_artifact_ids")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    INTRA_ARTIFACT_PATH_FIELD_NUMBER: _ClassVar[int]
    SCOPING_ARTIFACT_IDS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    artifact_type: ArtifactType
    artifact_id: str
    intra_artifact_path: str
    scoping_artifact_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, project_id: _Optional[str] = ..., artifact_type: _Optional[_Union[ArtifactType, str]] = ..., artifact_id: _Optional[str] = ..., intra_artifact_path: _Optional[str] = ..., scoping_artifact_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ExistsRequestResponse(_message.Message):
    __slots__ = ("exists",)
    EXISTS_FIELD_NUMBER: _ClassVar[int]
    exists: ExistsResponseOption
    def __init__(self, exists: _Optional[_Union[ExistsResponseOption, str]] = ...) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ("project_id", "artifact_type", "artifact_id", "intra_artifact_path", "max_chunk_size", "scoping_artifact_ids")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    INTRA_ARTIFACT_PATH_FIELD_NUMBER: _ClassVar[int]
    MAX_CHUNK_SIZE_FIELD_NUMBER: _ClassVar[int]
    SCOPING_ARTIFACT_IDS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    artifact_type: ArtifactType
    artifact_id: str
    intra_artifact_path: str
    max_chunk_size: int
    scoping_artifact_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, project_id: _Optional[str] = ..., artifact_type: _Optional[_Union[ArtifactType, str]] = ..., artifact_id: _Optional[str] = ..., intra_artifact_path: _Optional[str] = ..., max_chunk_size: _Optional[int] = ..., scoping_artifact_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetRequestResponse(_message.Message):
    __slots__ = ("output_chunk", "intra_artifact_path")
    OUTPUT_CHUNK_FIELD_NUMBER: _ClassVar[int]
    INTRA_ARTIFACT_PATH_FIELD_NUMBER: _ClassVar[int]
    output_chunk: bytes
    intra_artifact_path: str
    def __init__(self, output_chunk: _Optional[bytes] = ..., intra_artifact_path: _Optional[str] = ...) -> None: ...

class GetMetadataForEntityRequest(_message.Message):
    __slots__ = ("project_id", "artifact_type", "entity_id", "entity_name", "data_collection_name")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    artifact_type: ArtifactType
    entity_id: str
    entity_name: str
    data_collection_name: str
    def __init__(self, project_id: _Optional[str] = ..., artifact_type: _Optional[_Union[ArtifactType, str]] = ..., entity_id: _Optional[str] = ..., entity_name: _Optional[str] = ..., data_collection_name: _Optional[str] = ...) -> None: ...

class GetMetadataForEntityRequestResponse(_message.Message):
    __slots__ = ("project", "model", "data_collection", "split", "feature_list", "data_source", "feedback_function")
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    SPLIT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_LIST_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    project: _metadata_message_types_pb2.ProjectMetadata
    model: _metadata_message_types_pb2.ModelMetadata
    data_collection: _metadata_message_types_pb2.DataCollectionMetadata
    split: _metadata_message_types_pb2.DataSplitMetadata
    feature_list: _feature_pb2.FeatureList
    data_source: _metadata_message_types_pb2.DataSource
    feedback_function: _metadata_message_types_pb2.FeedbackFunctionMetadata
    def __init__(self, project: _Optional[_Union[_metadata_message_types_pb2.ProjectMetadata, _Mapping]] = ..., model: _Optional[_Union[_metadata_message_types_pb2.ModelMetadata, _Mapping]] = ..., data_collection: _Optional[_Union[_metadata_message_types_pb2.DataCollectionMetadata, _Mapping]] = ..., split: _Optional[_Union[_metadata_message_types_pb2.DataSplitMetadata, _Mapping]] = ..., feature_list: _Optional[_Union[_feature_pb2.FeatureList, _Mapping]] = ..., data_source: _Optional[_Union[_metadata_message_types_pb2.DataSource, _Mapping]] = ..., feedback_function: _Optional[_Union[_metadata_message_types_pb2.FeedbackFunctionMetadata, _Mapping]] = ...) -> None: ...

class GetSplitsRequestItem(_message.Message):
    __slots__ = ("model_id", "data_collection_id", "limit", "sort_by_property")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    SORT_BY_PROPERTY_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    data_collection_id: str
    limit: int
    sort_by_property: str
    def __init__(self, model_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., limit: _Optional[int] = ..., sort_by_property: _Optional[str] = ...) -> None: ...

class GetSplitsRequest(_message.Message):
    __slots__ = ("project_id", "for_items", "include_non_active_splits")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    FOR_ITEMS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_NON_ACTIVE_SPLITS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    for_items: _containers.RepeatedCompositeFieldContainer[GetSplitsRequestItem]
    include_non_active_splits: bool
    def __init__(self, project_id: _Optional[str] = ..., for_items: _Optional[_Iterable[_Union[GetSplitsRequestItem, _Mapping]]] = ..., include_non_active_splits: bool = ...) -> None: ...

class GetSplitsItem(_message.Message):
    __slots__ = ("model_id", "data_collection_id", "splits")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SPLITS_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    data_collection_id: str
    splits: _containers.RepeatedCompositeFieldContainer[_metadata_message_types_pb2.DataSplitMetadata]
    def __init__(self, model_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., splits: _Optional[_Iterable[_Union[_metadata_message_types_pb2.DataSplitMetadata, _Mapping]]] = ...) -> None: ...

class GetSplitsResponse(_message.Message):
    __slots__ = ("split_items",)
    SPLIT_ITEMS_FIELD_NUMBER: _ClassVar[int]
    split_items: _containers.RepeatedCompositeFieldContainer[GetSplitsItem]
    def __init__(self, split_items: _Optional[_Iterable[_Union[GetSplitsItem, _Mapping]]] = ...) -> None: ...

class GetDataCollectionsRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class GetDataCollectionsResponse(_message.Message):
    __slots__ = ("data_collections",)
    DATA_COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    data_collections: _containers.RepeatedCompositeFieldContainer[_metadata_message_types_pb2.DataCollectionMetadata]
    def __init__(self, data_collections: _Optional[_Iterable[_Union[_metadata_message_types_pb2.DataCollectionMetadata, _Mapping]]] = ...) -> None: ...

class GetModelsRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ...) -> None: ...

class GetModelsResponse(_message.Message):
    __slots__ = ("models",)
    MODELS_FIELD_NUMBER: _ClassVar[int]
    models: _containers.RepeatedCompositeFieldContainer[_metadata_message_types_pb2.ModelMetadata]
    def __init__(self, models: _Optional[_Iterable[_Union[_metadata_message_types_pb2.ModelMetadata, _Mapping]]] = ...) -> None: ...

class GetFeedbackFunctionsRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class GetFeedbackFunctionsResponse(_message.Message):
    __slots__ = ("feedback_functions",)
    FEEDBACK_FUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    feedback_functions: _containers.RepeatedCompositeFieldContainer[_metadata_message_types_pb2.FeedbackFunctionMetadata]
    def __init__(self, feedback_functions: _Optional[_Iterable[_Union[_metadata_message_types_pb2.FeedbackFunctionMetadata, _Mapping]]] = ...) -> None: ...

class GetAllMetadataRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "data_collection_name", "artifact_type", "include_non_active_splits", "workspace_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_NON_ACTIVE_SPLITS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    data_collection_name: str
    artifact_type: ArtifactType
    include_non_active_splits: bool
    workspace_id: str
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., artifact_type: _Optional[_Union[ArtifactType, str]] = ..., include_non_active_splits: bool = ..., workspace_id: _Optional[str] = ...) -> None: ...

class GetAllMetadataRequestResponse(_message.Message):
    __slots__ = ("id", "name_id_pairs", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_ID_PAIRS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: _containers.RepeatedScalarFieldContainer[str]
    name_id_pairs: _containers.RepeatedCompositeFieldContainer[NameIdPair]
    created_at: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    def __init__(self, id: _Optional[_Iterable[str]] = ..., name_id_pairs: _Optional[_Iterable[_Union[NameIdPair, _Mapping]]] = ..., created_at: _Optional[_Iterable[_Union[_timestamp_pb2.Timestamp, _Mapping]]] = ...) -> None: ...

class NameIdPair(_message.Message):
    __slots__ = ("name", "id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: str
    def __init__(self, name: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class DeleteRequest(_message.Message):
    __slots__ = ("project_id", "artifact_type", "artifact_id", "intra_artifact_path", "scoping_artifact_ids")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    INTRA_ARTIFACT_PATH_FIELD_NUMBER: _ClassVar[int]
    SCOPING_ARTIFACT_IDS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    artifact_type: ArtifactType
    artifact_id: str
    intra_artifact_path: str
    scoping_artifact_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, project_id: _Optional[str] = ..., artifact_type: _Optional[_Union[ArtifactType, str]] = ..., artifact_id: _Optional[str] = ..., intra_artifact_path: _Optional[str] = ..., scoping_artifact_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteRequestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteMetadataRequest(_message.Message):
    __slots__ = ("project_id", "artifact_type", "entity_id", "entity_name", "data_collection_name", "recursive")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    RECURSIVE_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    artifact_type: ArtifactType
    entity_id: str
    entity_name: str
    data_collection_name: str
    recursive: bool
    def __init__(self, project_id: _Optional[str] = ..., artifact_type: _Optional[_Union[ArtifactType, str]] = ..., entity_id: _Optional[str] = ..., entity_name: _Optional[str] = ..., data_collection_name: _Optional[str] = ..., recursive: bool = ...) -> None: ...

class DeleteMetadataRequestResponse(_message.Message):
    __slots__ = ("success", "blocking_entities")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    BLOCKING_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    blocking_entities: _containers.RepeatedCompositeFieldContainer[DeleteBlockingEntity]
    def __init__(self, success: bool = ..., blocking_entities: _Optional[_Iterable[_Union[DeleteBlockingEntity, _Mapping]]] = ...) -> None: ...

class DeleteBlockingEntity(_message.Message):
    __slots__ = ("id", "name", "project_id", "scoping_artifact_ids", "type", "can_be_deleted_via_recursive_flag")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SCOPING_ARTIFACT_IDS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CAN_BE_DELETED_VIA_RECURSIVE_FLAG_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    project_id: str
    scoping_artifact_ids: _containers.RepeatedScalarFieldContainer[str]
    type: ArtifactType
    can_be_deleted_via_recursive_flag: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., project_id: _Optional[str] = ..., scoping_artifact_ids: _Optional[_Iterable[str]] = ..., type: _Optional[_Union[ArtifactType, str]] = ..., can_be_deleted_via_recursive_flag: bool = ...) -> None: ...
