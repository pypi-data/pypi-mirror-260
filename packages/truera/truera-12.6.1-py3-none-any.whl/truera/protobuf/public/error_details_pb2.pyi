from truera.protobuf.public import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorDetails(_message.Message):
    __slots__ = ("trace_id", "source_service", "model_runner_job_id")
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_SERVICE_FIELD_NUMBER: _ClassVar[int]
    MODEL_RUNNER_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    trace_id: str
    source_service: str
    model_runner_job_id: str
    def __init__(self, trace_id: _Optional[str] = ..., source_service: _Optional[str] = ..., model_runner_job_id: _Optional[str] = ...) -> None: ...

class ErrorContext(_message.Message):
    __slots__ = ("error_code", "trace_id", "service_namespace")
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    error_code: int
    trace_id: str
    service_namespace: _common_pb2.ServiceNamespace
    def __init__(self, error_code: _Optional[int] = ..., trace_id: _Optional[str] = ..., service_namespace: _Optional[_Union[_common_pb2.ServiceNamespace, str]] = ...) -> None: ...
