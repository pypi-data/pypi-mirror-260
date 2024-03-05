from truera.protobuf.monitoring import monitoring_enums_pb2 as _monitoring_enums_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GrafanaModelRecord(_message.Message):
    __slots__ = ("id", "grafana_model_detail")
    ID_FIELD_NUMBER: _ClassVar[int]
    GRAFANA_MODEL_DETAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    grafana_model_detail: GrafanaModelDetail
    def __init__(self, id: _Optional[str] = ..., grafana_model_detail: _Optional[_Union[GrafanaModelDetail, _Mapping]] = ...) -> None: ...

class GrafanaModelDetail(_message.Message):
    __slots__ = ("project_id", "model_id", "organization_id", "automated_dashboard_folder_id", "dashboardDetails")
    class AutomatedDashboardFolderId(_message.Message):
        __slots__ = ("primitive_folder_id", "overview_folder_id")
        PRIMITIVE_FOLDER_ID_FIELD_NUMBER: _ClassVar[int]
        OVERVIEW_FOLDER_ID_FIELD_NUMBER: _ClassVar[int]
        primitive_folder_id: int
        overview_folder_id: int
        def __init__(self, primitive_folder_id: _Optional[int] = ..., overview_folder_id: _Optional[int] = ...) -> None: ...
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    AUTOMATED_DASHBOARD_FOLDER_ID_FIELD_NUMBER: _ClassVar[int]
    DASHBOARDDETAILS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_id: str
    organization_id: int
    automated_dashboard_folder_id: GrafanaModelDetail.AutomatedDashboardFolderId
    dashboardDetails: _containers.RepeatedCompositeFieldContainer[GrafanaDashboardDetail]
    def __init__(self, project_id: _Optional[str] = ..., model_id: _Optional[str] = ..., organization_id: _Optional[int] = ..., automated_dashboard_folder_id: _Optional[_Union[GrafanaModelDetail.AutomatedDashboardFolderId, _Mapping]] = ..., dashboardDetails: _Optional[_Iterable[_Union[GrafanaDashboardDetail, _Mapping]]] = ...) -> None: ...

class GrafanaDashboardDetail(_message.Message):
    __slots__ = ("dashboardType", "uid", "id", "parent_folder_id")
    DASHBOARDTYPE_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_FOLDER_ID_FIELD_NUMBER: _ClassVar[int]
    dashboardType: _monitoring_enums_pb2.GrafanaDashboardType
    uid: str
    id: int
    parent_folder_id: int
    def __init__(self, dashboardType: _Optional[_Union[_monitoring_enums_pb2.GrafanaDashboardType, str]] = ..., uid: _Optional[str] = ..., id: _Optional[int] = ..., parent_folder_id: _Optional[int] = ...) -> None: ...
