from truera.protobuf.druid import data_schema_pb2 as _data_schema_pb2
from truera.protobuf.druid import ingestion_method_pb2 as _ingestion_method_pb2
from truera.protobuf.druid import tuning_config_pb2 as _tuning_config_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IngestionSpec(_message.Message):
    __slots__ = ("data_schema", "ingestion_method", "general_tuning_config")
    DATA_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    INGESTION_METHOD_FIELD_NUMBER: _ClassVar[int]
    GENERAL_TUNING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    data_schema: _data_schema_pb2.DataSchema
    ingestion_method: _ingestion_method_pb2.IngestionMethod
    general_tuning_config: _tuning_config_pb2.GeneralTuningConfig
    def __init__(self, data_schema: _Optional[_Union[_data_schema_pb2.DataSchema, _Mapping]] = ..., ingestion_method: _Optional[_Union[_ingestion_method_pb2.IngestionMethod, _Mapping]] = ..., general_tuning_config: _Optional[_Union[_tuning_config_pb2.GeneralTuningConfig, _Mapping]] = ...) -> None: ...
