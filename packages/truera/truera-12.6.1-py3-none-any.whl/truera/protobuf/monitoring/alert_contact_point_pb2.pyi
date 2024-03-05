from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestDashboardContactPointResponseStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_TEST_DASHBOARD_CONTACT_POINT_RESPONSE_STATUS: _ClassVar[TestDashboardContactPointResponseStatus]
    OK: _ClassVar[TestDashboardContactPointResponseStatus]
    FAILED: _ClassVar[TestDashboardContactPointResponseStatus]

class ContactPointType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_CONTACT_POINT_TYPE: _ClassVar[ContactPointType]
    EMAIL: _ClassVar[ContactPointType]
    WEBHOOK: _ClassVar[ContactPointType]

class WebhookHttpMethods(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_WEBHOOK_HTTP_METHODS: _ClassVar[WebhookHttpMethods]
    PUT: _ClassVar[WebhookHttpMethods]
    POST: _ClassVar[WebhookHttpMethods]
UNKNOWN_TEST_DASHBOARD_CONTACT_POINT_RESPONSE_STATUS: TestDashboardContactPointResponseStatus
OK: TestDashboardContactPointResponseStatus
FAILED: TestDashboardContactPointResponseStatus
UNKNOWN_CONTACT_POINT_TYPE: ContactPointType
EMAIL: ContactPointType
WEBHOOK: ContactPointType
UNKNOWN_WEBHOOK_HTTP_METHODS: WebhookHttpMethods
PUT: WebhookHttpMethods
POST: WebhookHttpMethods

class AddDashboardContactPointRequest(_message.Message):
    __slots__ = ("detail",)
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    detail: ContactPointDetail
    def __init__(self, detail: _Optional[_Union[ContactPointDetail, _Mapping]] = ...) -> None: ...

class AddDashboardContactPointResponse(_message.Message):
    __slots__ = ("detail",)
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    detail: ContactPointDetail
    def __init__(self, detail: _Optional[_Union[ContactPointDetail, _Mapping]] = ...) -> None: ...

class GetDashboardContactPointRequest(_message.Message):
    __slots__ = ("dashboard_id", "contact_point_id")
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    CONTACT_POINT_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    contact_point_id: str
    def __init__(self, dashboard_id: _Optional[str] = ..., contact_point_id: _Optional[str] = ...) -> None: ...

class GetDashboardContactPointResponse(_message.Message):
    __slots__ = ("detail",)
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    detail: ContactPointDetail
    def __init__(self, detail: _Optional[_Union[ContactPointDetail, _Mapping]] = ...) -> None: ...

class GetDashboardContactPointsRequest(_message.Message):
    __slots__ = ("dashboard_id", "contact_point_id")
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    CONTACT_POINT_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    contact_point_id: str
    def __init__(self, dashboard_id: _Optional[str] = ..., contact_point_id: _Optional[str] = ...) -> None: ...

class GetDashboardContactPointsResponse(_message.Message):
    __slots__ = ("details",)
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: _containers.RepeatedCompositeFieldContainer[ContactPointDetail]
    def __init__(self, details: _Optional[_Iterable[_Union[ContactPointDetail, _Mapping]]] = ...) -> None: ...

class ModifyDashboardContactPointRequest(_message.Message):
    __slots__ = ("detail",)
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    detail: ContactPointDetail
    def __init__(self, detail: _Optional[_Union[ContactPointDetail, _Mapping]] = ...) -> None: ...

class ModifyDashboardContactPointResponse(_message.Message):
    __slots__ = ("detail",)
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    detail: ContactPointDetail
    def __init__(self, detail: _Optional[_Union[ContactPointDetail, _Mapping]] = ...) -> None: ...

class DeleteDashboardContactPointRequest(_message.Message):
    __slots__ = ("dashboard_id", "contact_point_id")
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    CONTACT_POINT_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    contact_point_id: str
    def __init__(self, dashboard_id: _Optional[str] = ..., contact_point_id: _Optional[str] = ...) -> None: ...

class TestDashboardContactPointResponse(_message.Message):
    __slots__ = ("notified_at", "status", "message")
    NOTIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    notified_at: str
    status: TestDashboardContactPointResponseStatus
    message: str
    def __init__(self, notified_at: _Optional[str] = ..., status: _Optional[_Union[TestDashboardContactPointResponseStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class DeleteDashboardContactPointResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ContactPointDetail(_message.Message):
    __slots__ = ("id", "dashboard_id", "contact_point_id", "name", "grafana_contact_point_id", "template", "contact_point", "webhook_contact_point", "created_by_user_id", "last_updated_by_user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    CONTACT_POINT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    GRAFANA_CONTACT_POINT_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    CONTACT_POINT_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_CONTACT_POINT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    dashboard_id: str
    contact_point_id: str
    name: str
    grafana_contact_point_id: str
    template: NotificationTemplate
    contact_point: EmailContactPoint
    webhook_contact_point: WebhookContactPoint
    created_by_user_id: str
    last_updated_by_user_id: str
    def __init__(self, id: _Optional[str] = ..., dashboard_id: _Optional[str] = ..., contact_point_id: _Optional[str] = ..., name: _Optional[str] = ..., grafana_contact_point_id: _Optional[str] = ..., template: _Optional[_Union[NotificationTemplate, _Mapping]] = ..., contact_point: _Optional[_Union[EmailContactPoint, _Mapping]] = ..., webhook_contact_point: _Optional[_Union[WebhookContactPoint, _Mapping]] = ..., created_by_user_id: _Optional[str] = ..., last_updated_by_user_id: _Optional[str] = ...) -> None: ...

class EmailContactPoint(_message.Message):
    __slots__ = ("contact_point_type", "addresses")
    CONTACT_POINT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    contact_point_type: str
    addresses: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, contact_point_type: _Optional[str] = ..., addresses: _Optional[_Iterable[str]] = ...) -> None: ...

class NotificationTemplate(_message.Message):
    __slots__ = ("notification_header", "notification_body")
    NOTIFICATION_HEADER_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_BODY_FIELD_NUMBER: _ClassVar[int]
    notification_header: str
    notification_body: str
    def __init__(self, notification_header: _Optional[str] = ..., notification_body: _Optional[str] = ...) -> None: ...

class WebhookContactPoint(_message.Message):
    __slots__ = ("url", "http_method", "basic_auth", "token_auth")
    URL_FIELD_NUMBER: _ClassVar[int]
    HTTP_METHOD_FIELD_NUMBER: _ClassVar[int]
    BASIC_AUTH_FIELD_NUMBER: _ClassVar[int]
    TOKEN_AUTH_FIELD_NUMBER: _ClassVar[int]
    url: str
    http_method: WebhookHttpMethods
    basic_auth: ContactPointBasicAuth
    token_auth: ContactPointTokenAuth
    def __init__(self, url: _Optional[str] = ..., http_method: _Optional[_Union[WebhookHttpMethods, str]] = ..., basic_auth: _Optional[_Union[ContactPointBasicAuth, _Mapping]] = ..., token_auth: _Optional[_Union[ContactPointTokenAuth, _Mapping]] = ...) -> None: ...

class ContactPointBasicAuth(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class ContactPointTokenAuth(_message.Message):
    __slots__ = ("scheme", "auth_token")
    SCHEME_FIELD_NUMBER: _ClassVar[int]
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    scheme: str
    auth_token: str
    def __init__(self, scheme: _Optional[str] = ..., auth_token: _Optional[str] = ...) -> None: ...
