from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from truera.protobuf.monitoring import monitoring_enums_pb2 as _monitoring_enums_pb2
from truera.protobuf.monitoring import monitoring_dashboard_pb2 as _monitoring_dashboard_pb2
from truera.protobuf.monitoring import alert_contact_point_pb2 as _alert_contact_point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HealthCheckRequest(_message.Message):
    __slots__ = ("ping_string",)
    PING_STRING_FIELD_NUMBER: _ClassVar[int]
    ping_string: str
    def __init__(self, ping_string: _Optional[str] = ...) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ("ping_response",)
    PING_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ping_response: str
    def __init__(self, ping_response: _Optional[str] = ...) -> None: ...

class EnableAlertingRequest(_message.Message):
    __slots__ = ("dashboard_id",)
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    def __init__(self, dashboard_id: _Optional[str] = ...) -> None: ...

class EnableAlertingResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DisableAlertingRequest(_message.Message):
    __slots__ = ("dashboard_id",)
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    def __init__(self, dashboard_id: _Optional[str] = ...) -> None: ...

class DisableAlertingResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AddAlertRuleRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: Rule
    def __init__(self, request: _Optional[_Union[Rule, _Mapping]] = ...) -> None: ...

class AddAlertRuleResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: Rule
    def __init__(self, response: _Optional[_Union[Rule, _Mapping]] = ...) -> None: ...

class GetAlertRuleRequest(_message.Message):
    __slots__ = ("dashboard_id", "rule_id")
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    rule_id: str
    def __init__(self, dashboard_id: _Optional[str] = ..., rule_id: _Optional[str] = ...) -> None: ...

class GetAlertRuleResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: Rule
    def __init__(self, response: _Optional[_Union[Rule, _Mapping]] = ...) -> None: ...

class ModifyAlertRuleRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: Rule
    def __init__(self, request: _Optional[_Union[Rule, _Mapping]] = ...) -> None: ...

class ModifyAlertRuleResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: Rule
    def __init__(self, response: _Optional[_Union[Rule, _Mapping]] = ...) -> None: ...

class DeleteAlertRuleRequest(_message.Message):
    __slots__ = ("dashboard_id", "rule_id")
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    rule_id: str
    def __init__(self, dashboard_id: _Optional[str] = ..., rule_id: _Optional[str] = ...) -> None: ...

class DeleteAlertRuleResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListDashboardAlertsWithStatusRequest(_message.Message):
    __slots__ = ("dashboard_id",)
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    def __init__(self, dashboard_id: _Optional[str] = ...) -> None: ...

class ListDashboardAlertsWithStatusResponse(_message.Message):
    __slots__ = ("alerts_with_status",)
    ALERTS_WITH_STATUS_FIELD_NUMBER: _ClassVar[int]
    alerts_with_status: _containers.RepeatedCompositeFieldContainer[AlertsWithStatus]
    def __init__(self, alerts_with_status: _Optional[_Iterable[_Union[AlertsWithStatus, _Mapping]]] = ...) -> None: ...

class AlertsWithStatus(_message.Message):
    __slots__ = ("id", "rule", "state", "notification_enabled", "silence")
    ID_FIELD_NUMBER: _ClassVar[int]
    RULE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SILENCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    rule: Rule
    state: _monitoring_enums_pb2.AlertRuleState
    notification_enabled: bool
    silence: _containers.RepeatedCompositeFieldContainer[Silence]
    def __init__(self, id: _Optional[str] = ..., rule: _Optional[_Union[Rule, _Mapping]] = ..., state: _Optional[_Union[_monitoring_enums_pb2.AlertRuleState, str]] = ..., notification_enabled: bool = ..., silence: _Optional[_Iterable[_Union[Silence, _Mapping]]] = ...) -> None: ...

class Rule(_message.Message):
    __slots__ = ("id", "name", "aggregator", "query_info", "condition", "condition_threshold_one", "condition_threshold_two", "metric_time_window", "evaluation_frequency", "evaluate_for", "rule_id", "models_info", "dashboard_id", "grafana_numeric_rule_id", "severity", "monitoring_panel_type", "is_notification_disabled", "notification_silence_id", "contact_point_name", "created_by_user_id", "last_updated_by_user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AGGREGATOR_FIELD_NUMBER: _ClassVar[int]
    QUERY_INFO_FIELD_NUMBER: _ClassVar[int]
    CONDITION_FIELD_NUMBER: _ClassVar[int]
    CONDITION_THRESHOLD_ONE_FIELD_NUMBER: _ClassVar[int]
    CONDITION_THRESHOLD_TWO_FIELD_NUMBER: _ClassVar[int]
    METRIC_TIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    EVALUATE_FOR_FIELD_NUMBER: _ClassVar[int]
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    MODELS_INFO_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    GRAFANA_NUMERIC_RULE_ID_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    MONITORING_PANEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_NOTIFICATION_DISABLED_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_SILENCE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTACT_POINT_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    aggregator: _monitoring_enums_pb2.AlertOperator
    query_info: _monitoring_dashboard_pb2.QueryInfo
    condition: _monitoring_enums_pb2.AlertCondition
    condition_threshold_one: float
    condition_threshold_two: float
    metric_time_window: str
    evaluation_frequency: str
    evaluate_for: str
    rule_id: str
    models_info: _containers.RepeatedCompositeFieldContainer[_monitoring_dashboard_pb2.ModelInfo]
    dashboard_id: str
    grafana_numeric_rule_id: int
    severity: _monitoring_enums_pb2.AlertSeverity
    monitoring_panel_type: _monitoring_dashboard_pb2.PanelType
    is_notification_disabled: bool
    notification_silence_id: str
    contact_point_name: str
    created_by_user_id: str
    last_updated_by_user_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., aggregator: _Optional[_Union[_monitoring_enums_pb2.AlertOperator, str]] = ..., query_info: _Optional[_Union[_monitoring_dashboard_pb2.QueryInfo, _Mapping]] = ..., condition: _Optional[_Union[_monitoring_enums_pb2.AlertCondition, str]] = ..., condition_threshold_one: _Optional[float] = ..., condition_threshold_two: _Optional[float] = ..., metric_time_window: _Optional[str] = ..., evaluation_frequency: _Optional[str] = ..., evaluate_for: _Optional[str] = ..., rule_id: _Optional[str] = ..., models_info: _Optional[_Iterable[_Union[_monitoring_dashboard_pb2.ModelInfo, _Mapping]]] = ..., dashboard_id: _Optional[str] = ..., grafana_numeric_rule_id: _Optional[int] = ..., severity: _Optional[_Union[_monitoring_enums_pb2.AlertSeverity, str]] = ..., monitoring_panel_type: _Optional[_Union[_monitoring_dashboard_pb2.PanelType, str]] = ..., is_notification_disabled: bool = ..., notification_silence_id: _Optional[str] = ..., contact_point_name: _Optional[str] = ..., created_by_user_id: _Optional[str] = ..., last_updated_by_user_id: _Optional[str] = ...) -> None: ...

class AlertSystemMetadata(_message.Message):
    __slots__ = ("id", "dashboard_id", "grafana_dashboard_id", "grafana_folder_id", "grafana_contact_point_ids", "grafana_labels")
    ID_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    GRAFANA_DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    GRAFANA_FOLDER_ID_FIELD_NUMBER: _ClassVar[int]
    GRAFANA_CONTACT_POINT_IDS_FIELD_NUMBER: _ClassVar[int]
    GRAFANA_LABELS_FIELD_NUMBER: _ClassVar[int]
    id: str
    dashboard_id: str
    grafana_dashboard_id: str
    grafana_folder_id: str
    grafana_contact_point_ids: _containers.RepeatedScalarFieldContainer[str]
    grafana_labels: str
    def __init__(self, id: _Optional[str] = ..., dashboard_id: _Optional[str] = ..., grafana_dashboard_id: _Optional[str] = ..., grafana_folder_id: _Optional[str] = ..., grafana_contact_point_ids: _Optional[_Iterable[str]] = ..., grafana_labels: _Optional[str] = ...) -> None: ...

class GetAlertRuleHistoryRequest(_message.Message):
    __slots__ = ("dashboard_id", "history_from", "rule_id")
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FROM_FIELD_NUMBER: _ClassVar[int]
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    history_from: _timestamp_pb2.Timestamp
    rule_id: str
    def __init__(self, dashboard_id: _Optional[str] = ..., history_from: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., rule_id: _Optional[str] = ...) -> None: ...

class GetAlertRuleHistoryResponse(_message.Message):
    __slots__ = ("history_event",)
    HISTORY_EVENT_FIELD_NUMBER: _ClassVar[int]
    history_event: _containers.RepeatedCompositeFieldContainer[AlertRuleHistoryEvent]
    def __init__(self, history_event: _Optional[_Iterable[_Union[AlertRuleHistoryEvent, _Mapping]]] = ...) -> None: ...

class AlertRuleHistoryEvent(_message.Message):
    __slots__ = ("event_begin", "event_end", "model_id", "rule_id", "model_ids")
    EVENT_BEGIN_FIELD_NUMBER: _ClassVar[int]
    EVENT_END_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_IDS_FIELD_NUMBER: _ClassVar[int]
    event_begin: _timestamp_pb2.Timestamp
    event_end: _timestamp_pb2.Timestamp
    model_id: str
    rule_id: str
    model_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, event_begin: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., event_end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., model_id: _Optional[str] = ..., rule_id: _Optional[str] = ..., model_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class Silence(_message.Message):
    __slots__ = ("dashboard_id", "alert_rule_id", "silence_from", "silence_till", "silence_id", "is_active")
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    ALERT_RULE_ID_FIELD_NUMBER: _ClassVar[int]
    SILENCE_FROM_FIELD_NUMBER: _ClassVar[int]
    SILENCE_TILL_FIELD_NUMBER: _ClassVar[int]
    SILENCE_ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    alert_rule_id: str
    silence_from: _timestamp_pb2.Timestamp
    silence_till: _timestamp_pb2.Timestamp
    silence_id: str
    is_active: bool
    def __init__(self, dashboard_id: _Optional[str] = ..., alert_rule_id: _Optional[str] = ..., silence_from: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., silence_till: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., silence_id: _Optional[str] = ..., is_active: bool = ...) -> None: ...

class AddSilenceRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: Silence
    def __init__(self, request: _Optional[_Union[Silence, _Mapping]] = ...) -> None: ...

class AddSilenceResponse(_message.Message):
    __slots__ = ("silence_id",)
    SILENCE_ID_FIELD_NUMBER: _ClassVar[int]
    silence_id: str
    def __init__(self, silence_id: _Optional[str] = ...) -> None: ...

class DeleteSilenceRequest(_message.Message):
    __slots__ = ("silence_id", "dashboard_id")
    SILENCE_ID_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    silence_id: str
    dashboard_id: str
    def __init__(self, silence_id: _Optional[str] = ..., dashboard_id: _Optional[str] = ...) -> None: ...

class DeleteSilenceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateSilenceRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: Silence
    def __init__(self, request: _Optional[_Union[Silence, _Mapping]] = ...) -> None: ...

class UpdateSilenceResponse(_message.Message):
    __slots__ = ("silence_id",)
    SILENCE_ID_FIELD_NUMBER: _ClassVar[int]
    silence_id: str
    def __init__(self, silence_id: _Optional[str] = ...) -> None: ...

class GetSilenceRequest(_message.Message):
    __slots__ = ("silence_id", "dashboard_id")
    SILENCE_ID_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    silence_id: str
    dashboard_id: str
    def __init__(self, silence_id: _Optional[str] = ..., dashboard_id: _Optional[str] = ...) -> None: ...

class GetSilenceResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: Silence
    def __init__(self, response: _Optional[_Union[Silence, _Mapping]] = ...) -> None: ...

class ListSilenceRequest(_message.Message):
    __slots__ = ("dashboard_id", "alert_id", "active_only")
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    ALERT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ONLY_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    alert_id: str
    active_only: bool
    def __init__(self, dashboard_id: _Optional[str] = ..., alert_id: _Optional[str] = ..., active_only: bool = ...) -> None: ...

class ListSilenceResponse(_message.Message):
    __slots__ = ("silences",)
    SILENCES_FIELD_NUMBER: _ClassVar[int]
    silences: _containers.RepeatedCompositeFieldContainer[Silence]
    def __init__(self, silences: _Optional[_Iterable[_Union[Silence, _Mapping]]] = ...) -> None: ...
