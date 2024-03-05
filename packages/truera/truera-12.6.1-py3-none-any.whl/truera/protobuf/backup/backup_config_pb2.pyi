from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BackupConfig(_message.Message):
    __slots__ = ("enable_backup", "duration_between_backup", "backup_retain_duration", "backup_folder", "mongodb_service_host", "auth_modes", "enable_restore", "enable_token_auth")
    ENABLE_BACKUP_FIELD_NUMBER: _ClassVar[int]
    DURATION_BETWEEN_BACKUP_FIELD_NUMBER: _ClassVar[int]
    BACKUP_RETAIN_DURATION_FIELD_NUMBER: _ClassVar[int]
    BACKUP_FOLDER_FIELD_NUMBER: _ClassVar[int]
    MONGODB_SERVICE_HOST_FIELD_NUMBER: _ClassVar[int]
    AUTH_MODES_FIELD_NUMBER: _ClassVar[int]
    ENABLE_RESTORE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_TOKEN_AUTH_FIELD_NUMBER: _ClassVar[int]
    enable_backup: bool
    duration_between_backup: _duration_pb2.Duration
    backup_retain_duration: _duration_pb2.Duration
    backup_folder: str
    mongodb_service_host: str
    auth_modes: _containers.RepeatedScalarFieldContainer[str]
    enable_restore: bool
    enable_token_auth: bool
    def __init__(self, enable_backup: bool = ..., duration_between_backup: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., backup_retain_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., backup_folder: _Optional[str] = ..., mongodb_service_host: _Optional[str] = ..., auth_modes: _Optional[_Iterable[str]] = ..., enable_restore: bool = ..., enable_token_auth: bool = ...) -> None: ...
