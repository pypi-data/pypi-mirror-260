from google.api import annotations_pb2 as _annotations_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from truera.protobuf.backup import backup_info_pb2 as _backup_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TriggerBackupRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TriggerBackupResponse(_message.Message):
    __slots__ = ("backup",)
    BACKUP_FIELD_NUMBER: _ClassVar[int]
    backup: _backup_info_pb2.BackupInfo
    def __init__(self, backup: _Optional[_Union[_backup_info_pb2.BackupInfo, _Mapping]] = ...) -> None: ...

class TriggerRestoreRequest(_message.Message):
    __slots__ = ("backup_folder_path",)
    BACKUP_FOLDER_PATH_FIELD_NUMBER: _ClassVar[int]
    backup_folder_path: str
    def __init__(self, backup_folder_path: _Optional[str] = ...) -> None: ...

class TriggerRestoreResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListBackupsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListBackupsResponse(_message.Message):
    __slots__ = ("backups",)
    BACKUPS_FIELD_NUMBER: _ClassVar[int]
    backups: _containers.RepeatedCompositeFieldContainer[_backup_info_pb2.BackupInfo]
    def __init__(self, backups: _Optional[_Iterable[_Union[_backup_info_pb2.BackupInfo, _Mapping]]] = ...) -> None: ...

class CleanupStaleBackupsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CleanupStaleBackupsResponse(_message.Message):
    __slots__ = ("cleanup_backups",)
    CLEANUP_BACKUPS_FIELD_NUMBER: _ClassVar[int]
    cleanup_backups: _containers.RepeatedCompositeFieldContainer[_backup_info_pb2.BackupInfo]
    def __init__(self, cleanup_backups: _Optional[_Iterable[_Union[_backup_info_pb2.BackupInfo, _Mapping]]] = ...) -> None: ...
