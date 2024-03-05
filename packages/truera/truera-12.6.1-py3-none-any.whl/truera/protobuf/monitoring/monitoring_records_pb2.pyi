from truera.protobuf.monitoring import monitoring_computation_pb2 as _monitoring_computation_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MonitoringComputationTaskRecord(_message.Message):
    __slots__ = ("id", "task")
    ID_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    id: str
    task: _monitoring_computation_pb2.MonitoringComputationTask
    def __init__(self, id: _Optional[str] = ..., task: _Optional[_Union[_monitoring_computation_pb2.MonitoringComputationTask, _Mapping]] = ...) -> None: ...

class MonitoringTaskCollectionRecord(_message.Message):
    __slots__ = ("id", "monitoring_task_collection")
    ID_FIELD_NUMBER: _ClassVar[int]
    MONITORING_TASK_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    monitoring_task_collection: _monitoring_computation_pb2.MonitoringTaskCollection
    def __init__(self, id: _Optional[str] = ..., monitoring_task_collection: _Optional[_Union[_monitoring_computation_pb2.MonitoringTaskCollection, _Mapping]] = ...) -> None: ...
