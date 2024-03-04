from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.api import annotations_pb2 as _annotations_pb2
from truera.protobuf.useranalytics import analytics_event_schema_pb2 as _analytics_event_schema_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserAnalyticsPingRequest(_message.Message):
    __slots__ = ("ping_string",)
    PING_STRING_FIELD_NUMBER: _ClassVar[int]
    ping_string: str
    def __init__(self, ping_string: _Optional[str] = ...) -> None: ...

class UserAnalyticsPingResponse(_message.Message):
    __slots__ = ("ping_response",)
    PING_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ping_response: str
    def __init__(self, ping_response: _Optional[str] = ...) -> None: ...

class TrueraEntityIdentifier(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "data_source_id", "data_split_id", "model_id", "feedback_function_id", "dashboard_id", "report_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FUNCTION_ID_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    REPORT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    data_source_id: str
    data_split_id: str
    model_id: str
    feedback_function_id: str
    dashboard_id: str
    report_id: str
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., data_source_id: _Optional[str] = ..., data_split_id: _Optional[str] = ..., model_id: _Optional[str] = ..., feedback_function_id: _Optional[str] = ..., dashboard_id: _Optional[str] = ..., report_id: _Optional[str] = ...) -> None: ...

class SendAnalyticsEventRequest(_message.Message):
    __slots__ = ("event_name", "event_id", "event_timestamp", "truera_entity_identifiers", "event_properties", "event_user_properties", "event_source_properties", "event_ingestion_timestamp", "server_build_version", "is_success", "structured_event_properties")
    class EventPropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TRUERA_ENTITY_IDENTIFIERS_FIELD_NUMBER: _ClassVar[int]
    EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    EVENT_USER_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    EVENT_SOURCE_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    EVENT_INGESTION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SERVER_BUILD_VERSION_FIELD_NUMBER: _ClassVar[int]
    IS_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STRUCTURED_EVENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    event_name: str
    event_id: str
    event_timestamp: _timestamp_pb2.Timestamp
    truera_entity_identifiers: _containers.RepeatedCompositeFieldContainer[TrueraEntityIdentifier]
    event_properties: _containers.ScalarMap[str, str]
    event_user_properties: EventUserProperties
    event_source_properties: EventSourceProperties
    event_ingestion_timestamp: _timestamp_pb2.Timestamp
    server_build_version: str
    is_success: bool
    structured_event_properties: _analytics_event_schema_pb2.StructuredEventProperties
    def __init__(self, event_name: _Optional[str] = ..., event_id: _Optional[str] = ..., event_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., truera_entity_identifiers: _Optional[_Iterable[_Union[TrueraEntityIdentifier, _Mapping]]] = ..., event_properties: _Optional[_Mapping[str, str]] = ..., event_user_properties: _Optional[_Union[EventUserProperties, _Mapping]] = ..., event_source_properties: _Optional[_Union[EventSourceProperties, _Mapping]] = ..., event_ingestion_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., server_build_version: _Optional[str] = ..., is_success: bool = ..., structured_event_properties: _Optional[_Union[_analytics_event_schema_pb2.StructuredEventProperties, _Mapping]] = ...) -> None: ...

class EventUserProperties(_message.Message):
    __slots__ = ("user_id", "tenant_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    tenant_id: str
    def __init__(self, user_id: _Optional[str] = ..., tenant_id: _Optional[str] = ...) -> None: ...

class EventSourceProperties(_message.Message):
    __slots__ = ("event_source", "event_platform_properties", "sdk_version", "experimentation_flags")
    class EventSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[EventSourceProperties.EventSource]
        SDK: _ClassVar[EventSourceProperties.EventSource]
        UI: _ClassVar[EventSourceProperties.EventSource]
        BACKEND: _ClassVar[EventSourceProperties.EventSource]
        CLI: _ClassVar[EventSourceProperties.EventSource]
    SOURCE_UNKNOWN: EventSourceProperties.EventSource
    SDK: EventSourceProperties.EventSource
    UI: EventSourceProperties.EventSource
    BACKEND: EventSourceProperties.EventSource
    CLI: EventSourceProperties.EventSource
    class ExperimentationFlagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    EVENT_PLATFORM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENTATION_FLAGS_FIELD_NUMBER: _ClassVar[int]
    event_source: EventSourceProperties.EventSource
    event_platform_properties: EventPlatformProperties
    sdk_version: str
    experimentation_flags: _containers.ScalarMap[str, str]
    def __init__(self, event_source: _Optional[_Union[EventSourceProperties.EventSource, str]] = ..., event_platform_properties: _Optional[_Union[EventPlatformProperties, _Mapping]] = ..., sdk_version: _Optional[str] = ..., experimentation_flags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class EventPlatformProperties(_message.Message):
    __slots__ = ("os_name", "os_version", "browser_name", "browser_version")
    OS_NAME_FIELD_NUMBER: _ClassVar[int]
    OS_VERSION_FIELD_NUMBER: _ClassVar[int]
    BROWSER_NAME_FIELD_NUMBER: _ClassVar[int]
    BROWSER_VERSION_FIELD_NUMBER: _ClassVar[int]
    os_name: str
    os_version: str
    browser_name: str
    browser_version: str
    def __init__(self, os_name: _Optional[str] = ..., os_version: _Optional[str] = ..., browser_name: _Optional[str] = ..., browser_version: _Optional[str] = ...) -> None: ...

class SendAnalyticsEventResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SendAnalyticsEventsBatchRequest(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[SendAnalyticsEventRequest]
    def __init__(self, events: _Optional[_Iterable[_Union[SendAnalyticsEventRequest, _Mapping]]] = ...) -> None: ...

class SendAnalyticsEventsBatchResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
