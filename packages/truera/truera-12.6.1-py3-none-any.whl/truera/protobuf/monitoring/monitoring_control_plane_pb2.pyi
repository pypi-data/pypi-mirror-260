from google.api import annotations_pb2 as _annotations_pb2
from truera.protobuf.druid import ingestion_spec_pb2 as _ingestion_spec_pb2
from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from truera.protobuf.public.common import data_locator_pb2 as _data_locator_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateIngestionRequest(_message.Message):
    __slots__ = ("spec", "project_id")
    SPEC_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    spec: _ingestion_spec_pb2.IngestionSpec
    project_id: str
    def __init__(self, spec: _Optional[_Union[_ingestion_spec_pb2.IngestionSpec, _Mapping]] = ..., project_id: _Optional[str] = ...) -> None: ...

class CreateIngestionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListDruidTablesRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class DruidTableEntry(_message.Message):
    __slots__ = ("druid_table_name", "project_id", "data_collection_id", "data_kind")
    DRUID_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_KIND_FIELD_NUMBER: _ClassVar[int]
    druid_table_name: str
    project_id: str
    data_collection_id: str
    data_kind: _data_locator_pb2.DataKindWrapper
    def __init__(self, druid_table_name: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., data_kind: _Optional[_Union[_data_locator_pb2.DataKindWrapper, _Mapping]] = ...) -> None: ...

class ListDruidTablesResponse(_message.Message):
    __slots__ = ("druidTables",)
    DRUIDTABLES_FIELD_NUMBER: _ClassVar[int]
    druidTables: _containers.RepeatedCompositeFieldContainer[DruidTableEntry]
    def __init__(self, druidTables: _Optional[_Iterable[_Union[DruidTableEntry, _Mapping]]] = ...) -> None: ...

class CreateIngestionForTopicRequest(_message.Message):
    __slots__ = ("topic_locator", "quantity_of_interest")
    TOPIC_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_OF_INTEREST_FIELD_NUMBER: _ClassVar[int]
    topic_locator: _data_locator_pb2.DataLocator
    quantity_of_interest: _qoi_pb2.QuantityOfInterest
    def __init__(self, topic_locator: _Optional[_Union[_data_locator_pb2.DataLocator, _Mapping]] = ..., quantity_of_interest: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ...) -> None: ...

class CreateIngestionForTopicResponse(_message.Message):
    __slots__ = ("submit_spec_response",)
    SUBMIT_SPEC_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    submit_spec_response: str
    def __init__(self, submit_spec_response: _Optional[str] = ...) -> None: ...
