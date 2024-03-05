from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InputFormatProtobufType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INPUT_FORMAT_PROTOBUF_TYPE_UNSPECIFIED: _ClassVar[InputFormatProtobufType]
    INPUT_FORMAT_PROTOBUF_TYPE_ROW: _ClassVar[InputFormatProtobufType]
    INPUT_FORMAT_PROTOBUF_TYPE_SCHEMA_MISMATCH: _ClassVar[InputFormatProtobufType]
    INPUT_FORMAT_PROTOBUF_TYPE_JOINED_PREDICTION_LABEL: _ClassVar[InputFormatProtobufType]
    INPUT_FORMAT_PROTOBUF_TYPE_SCHEMA_EMBEDDED_ROW: _ClassVar[InputFormatProtobufType]
    INPUT_FORMAT_PROTOBUF_METRIC: _ClassVar[InputFormatProtobufType]
INPUT_FORMAT_PROTOBUF_TYPE_UNSPECIFIED: InputFormatProtobufType
INPUT_FORMAT_PROTOBUF_TYPE_ROW: InputFormatProtobufType
INPUT_FORMAT_PROTOBUF_TYPE_SCHEMA_MISMATCH: InputFormatProtobufType
INPUT_FORMAT_PROTOBUF_TYPE_JOINED_PREDICTION_LABEL: InputFormatProtobufType
INPUT_FORMAT_PROTOBUF_TYPE_SCHEMA_EMBEDDED_ROW: InputFormatProtobufType
INPUT_FORMAT_PROTOBUF_METRIC: InputFormatProtobufType

class IngestionMethod(_message.Message):
    __slots__ = ("kafka_config",)
    KAFKA_CONFIG_FIELD_NUMBER: _ClassVar[int]
    kafka_config: KafkaConfig
    def __init__(self, kafka_config: _Optional[_Union[KafkaConfig, _Mapping]] = ...) -> None: ...

class KafkaConfig(_message.Message):
    __slots__ = ("io_config", "tuning_config")
    IO_CONFIG_FIELD_NUMBER: _ClassVar[int]
    TUNING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    io_config: KafkaIoConfig
    tuning_config: KafkaTuningConfig
    def __init__(self, io_config: _Optional[_Union[KafkaIoConfig, _Mapping]] = ..., tuning_config: _Optional[_Union[KafkaTuningConfig, _Mapping]] = ...) -> None: ...

class KafkaIoConfig(_message.Message):
    __slots__ = ("topic", "consumer_properties", "input_format", "use_earliest_offset", "task_duration")
    class InputFormat(_message.Message):
        __slots__ = ("protobuf_type", "column_list")
        PROTOBUF_TYPE_FIELD_NUMBER: _ClassVar[int]
        COLUMN_LIST_FIELD_NUMBER: _ClassVar[int]
        protobuf_type: InputFormatProtobufType
        column_list: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, protobuf_type: _Optional[_Union[InputFormatProtobufType, str]] = ..., column_list: _Optional[_Iterable[str]] = ...) -> None: ...
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    INPUT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    USE_EARLIEST_OFFSET_FIELD_NUMBER: _ClassVar[int]
    TASK_DURATION_FIELD_NUMBER: _ClassVar[int]
    topic: str
    consumer_properties: ConsumerProperties
    input_format: KafkaIoConfig.InputFormat
    use_earliest_offset: bool
    task_duration: str
    def __init__(self, topic: _Optional[str] = ..., consumer_properties: _Optional[_Union[ConsumerProperties, _Mapping]] = ..., input_format: _Optional[_Union[KafkaIoConfig.InputFormat, _Mapping]] = ..., use_earliest_offset: bool = ..., task_duration: _Optional[str] = ...) -> None: ...

class ConsumerProperties(_message.Message):
    __slots__ = ("bootstrap_servers",)
    class BootstrapServer(_message.Message):
        __slots__ = ("host", "port")
        HOST_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        host: str
        port: int
        def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...
    BOOTSTRAP_SERVERS_FIELD_NUMBER: _ClassVar[int]
    bootstrap_servers: _containers.RepeatedCompositeFieldContainer[ConsumerProperties.BootstrapServer]
    def __init__(self, bootstrap_servers: _Optional[_Iterable[_Union[ConsumerProperties.BootstrapServer, _Mapping]]] = ...) -> None: ...

class KafkaTuningConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
