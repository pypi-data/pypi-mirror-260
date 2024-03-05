from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LivyErrorResponse(_message.Message):
    __slots__ = ("msg",)
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: str
    def __init__(self, msg: _Optional[str] = ...) -> None: ...

class LivyBatchRequest(_message.Message):
    __slots__ = ("file", "proxyUser", "className", "args", "jars", "pyFiles", "files", "driverMemory", "driverCores", "executorMemory", "executorCores", "numExecutors", "archives", "queue", "name", "conf")
    class ConfEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    FILE_FIELD_NUMBER: _ClassVar[int]
    PROXYUSER_FIELD_NUMBER: _ClassVar[int]
    CLASSNAME_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    JARS_FIELD_NUMBER: _ClassVar[int]
    PYFILES_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    DRIVERMEMORY_FIELD_NUMBER: _ClassVar[int]
    DRIVERCORES_FIELD_NUMBER: _ClassVar[int]
    EXECUTORMEMORY_FIELD_NUMBER: _ClassVar[int]
    EXECUTORCORES_FIELD_NUMBER: _ClassVar[int]
    NUMEXECUTORS_FIELD_NUMBER: _ClassVar[int]
    ARCHIVES_FIELD_NUMBER: _ClassVar[int]
    QUEUE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONF_FIELD_NUMBER: _ClassVar[int]
    file: str
    proxyUser: str
    className: str
    args: _containers.RepeatedScalarFieldContainer[str]
    jars: _containers.RepeatedScalarFieldContainer[str]
    pyFiles: _containers.RepeatedScalarFieldContainer[str]
    files: _containers.RepeatedScalarFieldContainer[str]
    driverMemory: str
    driverCores: int
    executorMemory: str
    executorCores: int
    numExecutors: int
    archives: _containers.RepeatedScalarFieldContainer[str]
    queue: str
    name: str
    conf: _containers.ScalarMap[str, str]
    def __init__(self, file: _Optional[str] = ..., proxyUser: _Optional[str] = ..., className: _Optional[str] = ..., args: _Optional[_Iterable[str]] = ..., jars: _Optional[_Iterable[str]] = ..., pyFiles: _Optional[_Iterable[str]] = ..., files: _Optional[_Iterable[str]] = ..., driverMemory: _Optional[str] = ..., driverCores: _Optional[int] = ..., executorMemory: _Optional[str] = ..., executorCores: _Optional[int] = ..., numExecutors: _Optional[int] = ..., archives: _Optional[_Iterable[str]] = ..., queue: _Optional[str] = ..., name: _Optional[str] = ..., conf: _Optional[_Mapping[str, str]] = ...) -> None: ...

class LivyBatch(_message.Message):
    __slots__ = ("id", "appId", "appInfo", "log", "state")
    class AppInfoEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    APPINFO_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    id: int
    appId: str
    appInfo: _containers.MessageMap[str, _struct_pb2.Value]
    log: _containers.RepeatedScalarFieldContainer[str]
    state: str
    def __init__(self, id: _Optional[int] = ..., appId: _Optional[str] = ..., appInfo: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., log: _Optional[_Iterable[str]] = ..., state: _Optional[str] = ...) -> None: ...

class LivyCreateSessionRequest(_message.Message):
    __slots__ = ("kind", "proxyUser", "jars", "pyFiles", "files", "driverMemory", "driverCores", "executorMemory", "executorCores", "numExecutors", "archives", "queue", "name", "conf", "heartbeatTimeoutInSecond")
    class ConfEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    KIND_FIELD_NUMBER: _ClassVar[int]
    PROXYUSER_FIELD_NUMBER: _ClassVar[int]
    JARS_FIELD_NUMBER: _ClassVar[int]
    PYFILES_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    DRIVERMEMORY_FIELD_NUMBER: _ClassVar[int]
    DRIVERCORES_FIELD_NUMBER: _ClassVar[int]
    EXECUTORMEMORY_FIELD_NUMBER: _ClassVar[int]
    EXECUTORCORES_FIELD_NUMBER: _ClassVar[int]
    NUMEXECUTORS_FIELD_NUMBER: _ClassVar[int]
    ARCHIVES_FIELD_NUMBER: _ClassVar[int]
    QUEUE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONF_FIELD_NUMBER: _ClassVar[int]
    HEARTBEATTIMEOUTINSECOND_FIELD_NUMBER: _ClassVar[int]
    kind: str
    proxyUser: str
    jars: _containers.RepeatedScalarFieldContainer[str]
    pyFiles: _containers.RepeatedScalarFieldContainer[str]
    files: _containers.RepeatedScalarFieldContainer[str]
    driverMemory: str
    driverCores: int
    executorMemory: str
    executorCores: int
    numExecutors: int
    archives: _containers.RepeatedScalarFieldContainer[str]
    queue: str
    name: str
    conf: _containers.ScalarMap[str, str]
    heartbeatTimeoutInSecond: int
    def __init__(self, kind: _Optional[str] = ..., proxyUser: _Optional[str] = ..., jars: _Optional[_Iterable[str]] = ..., pyFiles: _Optional[_Iterable[str]] = ..., files: _Optional[_Iterable[str]] = ..., driverMemory: _Optional[str] = ..., driverCores: _Optional[int] = ..., executorMemory: _Optional[str] = ..., executorCores: _Optional[int] = ..., numExecutors: _Optional[int] = ..., archives: _Optional[_Iterable[str]] = ..., queue: _Optional[str] = ..., name: _Optional[str] = ..., conf: _Optional[_Mapping[str, str]] = ..., heartbeatTimeoutInSecond: _Optional[int] = ...) -> None: ...

class LivySession(_message.Message):
    __slots__ = ("id", "appId", "owner", "kind", "logs", "state", "appInfo", "name")
    class AppInfoEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    APPINFO_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    appId: str
    owner: str
    kind: str
    logs: _containers.RepeatedScalarFieldContainer[str]
    state: str
    appInfo: _containers.MessageMap[str, _struct_pb2.Value]
    name: str
    def __init__(self, id: _Optional[int] = ..., appId: _Optional[str] = ..., owner: _Optional[str] = ..., kind: _Optional[str] = ..., logs: _Optional[_Iterable[str]] = ..., state: _Optional[str] = ..., appInfo: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., name: _Optional[str] = ...) -> None: ...

class LivySessions(_message.Message):
    __slots__ = ("total", "sessions")
    FROM_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    total: int
    sessions: _containers.RepeatedCompositeFieldContainer[LivySession]
    def __init__(self, total: _Optional[int] = ..., sessions: _Optional[_Iterable[_Union[LivySession, _Mapping]]] = ..., **kwargs) -> None: ...
