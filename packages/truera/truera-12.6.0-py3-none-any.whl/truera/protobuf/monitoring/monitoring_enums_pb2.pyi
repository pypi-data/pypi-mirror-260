from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class MonitoringTaskStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNDEFINED: _ClassVar[MonitoringTaskStatus]
    SUCCESS: _ClassVar[MonitoringTaskStatus]
    PENDING: _ClassVar[MonitoringTaskStatus]
    ERROR: _ClassVar[MonitoringTaskStatus]
    QUEUED: _ClassVar[MonitoringTaskStatus]
    CONSISTENTLY_FAILING: _ClassVar[MonitoringTaskStatus]
    CREATED: _ClassVar[MonitoringTaskStatus]

class GrafanaDashboardType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_DASHBOARD_TYPE: _ClassVar[GrafanaDashboardType]
    MODEL_OVERVIEW: _ClassVar[GrafanaDashboardType]
    SEGMENT_OVERVIEW: _ClassVar[GrafanaDashboardType]
    CATEGORICAL_FEATURES_OVERVIEW: _ClassVar[GrafanaDashboardType]
    NUMERICAL_FEATURES_OVERVIEW: _ClassVar[GrafanaDashboardType]
    DATA_QUALITY_OVERVIEW: _ClassVar[GrafanaDashboardType]
    BIAS_OVERVIEW: _ClassVar[GrafanaDashboardType]
    ALERTS: _ClassVar[GrafanaDashboardType]
    MODEL_COMPARISON: _ClassVar[GrafanaDashboardType]
    BIAS_COMPARISON: _ClassVar[GrafanaDashboardType]
    SEGMENT_COMPARISON: _ClassVar[GrafanaDashboardType]
    DQ_FOLDER_OVERVIEW: _ClassVar[GrafanaDashboardType]
    DQ_FOLDER_METRIC_DRILLDOWN: _ClassVar[GrafanaDashboardType]
    DQ_FOLDER_FEATURE_DRILLDOWN: _ClassVar[GrafanaDashboardType]
    DQ_FOLDER_FEATURE_NUMERICAL_DEBUGGING: _ClassVar[GrafanaDashboardType]
    DQ_FOLDER_FEATURE_CATEGORICAL_DEBUGGING: _ClassVar[GrafanaDashboardType]
    MODEL_OVERWATCH: _ClassVar[GrafanaDashboardType]

class GrafanaGraphType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[GrafanaGraphType]
    MODEL_STABILITY_SCORE: _ClassVar[GrafanaGraphType]
    MODEL_PREDICTION_SCORES: _ClassVar[GrafanaGraphType]
    MODEL_DISPARITY_SCORE: _ClassVar[GrafanaGraphType]
    MODEL_PERFORMANCE_METRIC: _ClassVar[GrafanaGraphType]
    MODEL_CLASSIFICATION: _ClassVar[GrafanaGraphType]
    FEATURE_INFLUENCE_STABILITY_SCORE: _ClassVar[GrafanaGraphType]
    FEATURE_VALUES: _ClassVar[GrafanaGraphType]
    FEATURE_CONTRIBUTION_TO_BIAS: _ClassVar[GrafanaGraphType]
    MODEL_RUNNER_OUTPUT: _ClassVar[GrafanaGraphType]
    MODEL_BIAS: _ClassVar[GrafanaGraphType]
    GROUND_TRUTH_LABELS: _ClassVar[GrafanaGraphType]
    DATA_QUALITY_VIOLATIONS_OVERVIEW: _ClassVar[GrafanaGraphType]
    DATA_QUALITY_FEATURE: _ClassVar[GrafanaGraphType]
    FEATURE_DRIFT: _ClassVar[GrafanaGraphType]
    CATEGORICAL_FEATURES_DRIFT_OVERVIEW: _ClassVar[GrafanaGraphType]
    NUMERICAL_FEATURES_DRIFT_OVERVIEW: _ClassVar[GrafanaGraphType]

class GrafanaDataLinkParams(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_DATALINK_PARAM: _ClassVar[GrafanaDataLinkParams]
    PROJECT_ID: _ClassVar[GrafanaDataLinkParams]
    MODEL_ID: _ClassVar[GrafanaDataLinkParams]
    DASHBOARD_TYPE: _ClassVar[GrafanaDataLinkParams]
    GRAPH_TYPE: _ClassVar[GrafanaDataLinkParams]
    SEGMENT: _ClassVar[GrafanaDataLinkParams]
    FEATURE: _ClassVar[GrafanaDataLinkParams]
    SERIES_NAME: _ClassVar[GrafanaDataLinkParams]
    TIME: _ClassVar[GrafanaDataLinkParams]

class AlertOperator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UKNOWN_ALERT_OPERATOR: _ClassVar[AlertOperator]
    AVG: _ClassVar[AlertOperator]
    MIN: _ClassVar[AlertOperator]
    MAX: _ClassVar[AlertOperator]
    SUM: _ClassVar[AlertOperator]
    COUNT: _ClassVar[AlertOperator]
    LAST: _ClassVar[AlertOperator]
    MEDIAN: _ClassVar[AlertOperator]
    DIFF: _ClassVar[AlertOperator]
    DIFF_ABS: _ClassVar[AlertOperator]
    PERCENT_DIFF: _ClassVar[AlertOperator]
    PERCENT_DIFF_ABS: _ClassVar[AlertOperator]
    COUNT_NON_NULL: _ClassVar[AlertOperator]

class AlertCondition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UKNOWN_ALERT_CONDITION: _ClassVar[AlertCondition]
    IS_ABOVE: _ClassVar[AlertCondition]
    IS_BELOW: _ClassVar[AlertCondition]
    IS_OUTSIDE_RANGE: _ClassVar[AlertCondition]
    IS_WITHIN_RANGE: _ClassVar[AlertCondition]
    HAS_NO_VALUE: _ClassVar[AlertCondition]

class AlertSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_ALERT_SEVERITY: _ClassVar[AlertSeverity]
    CRITICAL: _ClassVar[AlertSeverity]
    WARNING: _ClassVar[AlertSeverity]
    FYI: _ClassVar[AlertSeverity]

class AlertRuleState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_ALERT_RULE_STATE: _ClassVar[AlertRuleState]
    ALERT_RULE_STATE_NORMAL: _ClassVar[AlertRuleState]
    ALERT_RULE_STATE_PENDING: _ClassVar[AlertRuleState]
    ALERT_RULE_STATE_FIRING: _ClassVar[AlertRuleState]

class AlertInstanceState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKOWN_ALERT_INSTANCE: _ClassVar[AlertInstanceState]
    ALERT_INSTANCE_STATE_NORMAL: _ClassVar[AlertInstanceState]
    ALERT_INSTANCE_STATE_PENDING: _ClassVar[AlertInstanceState]
    ALERT_INSTANCE_STATE_ALERTING: _ClassVar[AlertInstanceState]
    ALERT_INSTANCE_STATE_NO_DATA: _ClassVar[AlertInstanceState]
    ALERT_INSTANCE_STATE_ERROR: _ClassVar[AlertInstanceState]

class AlertRuleHealth(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_ALERT_RULE_HEALTH: _ClassVar[AlertRuleHealth]
    ALERT_RULE_HEALTH_OK: _ClassVar[AlertRuleHealth]
    ALERT_RULE_HEALTH_ERROR: _ClassVar[AlertRuleHealth]
    ALERT_RULE_HEALTH_NO_DATA: _ClassVar[AlertRuleHealth]

class MonitoringServiceErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MONITORING_SERVICE_NO_ERROR: _ClassVar[MonitoringServiceErrorCode]
    MONITORING_SERVICE_UNKNOWN_ERROR: _ClassVar[MonitoringServiceErrorCode]
UNDEFINED: MonitoringTaskStatus
SUCCESS: MonitoringTaskStatus
PENDING: MonitoringTaskStatus
ERROR: MonitoringTaskStatus
QUEUED: MonitoringTaskStatus
CONSISTENTLY_FAILING: MonitoringTaskStatus
CREATED: MonitoringTaskStatus
UNKNOWN_DASHBOARD_TYPE: GrafanaDashboardType
MODEL_OVERVIEW: GrafanaDashboardType
SEGMENT_OVERVIEW: GrafanaDashboardType
CATEGORICAL_FEATURES_OVERVIEW: GrafanaDashboardType
NUMERICAL_FEATURES_OVERVIEW: GrafanaDashboardType
DATA_QUALITY_OVERVIEW: GrafanaDashboardType
BIAS_OVERVIEW: GrafanaDashboardType
ALERTS: GrafanaDashboardType
MODEL_COMPARISON: GrafanaDashboardType
BIAS_COMPARISON: GrafanaDashboardType
SEGMENT_COMPARISON: GrafanaDashboardType
DQ_FOLDER_OVERVIEW: GrafanaDashboardType
DQ_FOLDER_METRIC_DRILLDOWN: GrafanaDashboardType
DQ_FOLDER_FEATURE_DRILLDOWN: GrafanaDashboardType
DQ_FOLDER_FEATURE_NUMERICAL_DEBUGGING: GrafanaDashboardType
DQ_FOLDER_FEATURE_CATEGORICAL_DEBUGGING: GrafanaDashboardType
MODEL_OVERWATCH: GrafanaDashboardType
UNKNOWN: GrafanaGraphType
MODEL_STABILITY_SCORE: GrafanaGraphType
MODEL_PREDICTION_SCORES: GrafanaGraphType
MODEL_DISPARITY_SCORE: GrafanaGraphType
MODEL_PERFORMANCE_METRIC: GrafanaGraphType
MODEL_CLASSIFICATION: GrafanaGraphType
FEATURE_INFLUENCE_STABILITY_SCORE: GrafanaGraphType
FEATURE_VALUES: GrafanaGraphType
FEATURE_CONTRIBUTION_TO_BIAS: GrafanaGraphType
MODEL_RUNNER_OUTPUT: GrafanaGraphType
MODEL_BIAS: GrafanaGraphType
GROUND_TRUTH_LABELS: GrafanaGraphType
DATA_QUALITY_VIOLATIONS_OVERVIEW: GrafanaGraphType
DATA_QUALITY_FEATURE: GrafanaGraphType
FEATURE_DRIFT: GrafanaGraphType
CATEGORICAL_FEATURES_DRIFT_OVERVIEW: GrafanaGraphType
NUMERICAL_FEATURES_DRIFT_OVERVIEW: GrafanaGraphType
UNKNOWN_DATALINK_PARAM: GrafanaDataLinkParams
PROJECT_ID: GrafanaDataLinkParams
MODEL_ID: GrafanaDataLinkParams
DASHBOARD_TYPE: GrafanaDataLinkParams
GRAPH_TYPE: GrafanaDataLinkParams
SEGMENT: GrafanaDataLinkParams
FEATURE: GrafanaDataLinkParams
SERIES_NAME: GrafanaDataLinkParams
TIME: GrafanaDataLinkParams
UKNOWN_ALERT_OPERATOR: AlertOperator
AVG: AlertOperator
MIN: AlertOperator
MAX: AlertOperator
SUM: AlertOperator
COUNT: AlertOperator
LAST: AlertOperator
MEDIAN: AlertOperator
DIFF: AlertOperator
DIFF_ABS: AlertOperator
PERCENT_DIFF: AlertOperator
PERCENT_DIFF_ABS: AlertOperator
COUNT_NON_NULL: AlertOperator
UKNOWN_ALERT_CONDITION: AlertCondition
IS_ABOVE: AlertCondition
IS_BELOW: AlertCondition
IS_OUTSIDE_RANGE: AlertCondition
IS_WITHIN_RANGE: AlertCondition
HAS_NO_VALUE: AlertCondition
UNKNOWN_ALERT_SEVERITY: AlertSeverity
CRITICAL: AlertSeverity
WARNING: AlertSeverity
FYI: AlertSeverity
UNKNOWN_ALERT_RULE_STATE: AlertRuleState
ALERT_RULE_STATE_NORMAL: AlertRuleState
ALERT_RULE_STATE_PENDING: AlertRuleState
ALERT_RULE_STATE_FIRING: AlertRuleState
UNKOWN_ALERT_INSTANCE: AlertInstanceState
ALERT_INSTANCE_STATE_NORMAL: AlertInstanceState
ALERT_INSTANCE_STATE_PENDING: AlertInstanceState
ALERT_INSTANCE_STATE_ALERTING: AlertInstanceState
ALERT_INSTANCE_STATE_NO_DATA: AlertInstanceState
ALERT_INSTANCE_STATE_ERROR: AlertInstanceState
UNKNOWN_ALERT_RULE_HEALTH: AlertRuleHealth
ALERT_RULE_HEALTH_OK: AlertRuleHealth
ALERT_RULE_HEALTH_ERROR: AlertRuleHealth
ALERT_RULE_HEALTH_NO_DATA: AlertRuleHealth
MONITORING_SERVICE_NO_ERROR: MonitoringServiceErrorCode
MONITORING_SERVICE_UNKNOWN_ERROR: MonitoringServiceErrorCode
