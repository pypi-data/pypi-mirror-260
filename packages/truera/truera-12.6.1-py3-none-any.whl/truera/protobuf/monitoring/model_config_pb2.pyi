from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModelMonitoringConfig(_message.Message):
    __slots__ = ("project_id", "model_id", "monitoring_enabled", "data_collection_state")
    class DataCollectionState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNDEFINED: _ClassVar[ModelMonitoringConfig.DataCollectionState]
        STATIC: _ClassVar[ModelMonitoringConfig.DataCollectionState]
        PERIODIC: _ClassVar[ModelMonitoringConfig.DataCollectionState]
    UNDEFINED: ModelMonitoringConfig.DataCollectionState
    STATIC: ModelMonitoringConfig.DataCollectionState
    PERIODIC: ModelMonitoringConfig.DataCollectionState
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MONITORING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_STATE_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    model_id: str
    monitoring_enabled: bool
    data_collection_state: ModelMonitoringConfig.DataCollectionState
    def __init__(self, project_id: _Optional[str] = ..., model_id: _Optional[str] = ..., monitoring_enabled: bool = ..., data_collection_state: _Optional[_Union[ModelMonitoringConfig.DataCollectionState, str]] = ...) -> None: ...
