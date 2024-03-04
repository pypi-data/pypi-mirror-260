from truera.protobuf.public.common import data_kind_pb2 as _data_kind_pb2
from truera.protobuf.public import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CombinedDataKindDescribed(_message.Message):
    __slots__ = ("base_data_kinds",)
    BASE_DATA_KINDS_FIELD_NUMBER: _ClassVar[int]
    base_data_kinds: _containers.RepeatedScalarFieldContainer[_data_kind_pb2.DataKindDescribed]
    def __init__(self, base_data_kinds: _Optional[_Iterable[_Union[_data_kind_pb2.DataKindDescribed, str]]] = ...) -> None: ...

class DataKindWrapper(_message.Message):
    __slots__ = ("base_data_kind", "combined_data_kind")
    BASE_DATA_KIND_FIELD_NUMBER: _ClassVar[int]
    COMBINED_DATA_KIND_FIELD_NUMBER: _ClassVar[int]
    base_data_kind: _data_kind_pb2.DataKindDescribed
    combined_data_kind: CombinedDataKindDescribed
    def __init__(self, base_data_kind: _Optional[_Union[_data_kind_pb2.DataKindDescribed, str]] = ..., combined_data_kind: _Optional[_Union[CombinedDataKindDescribed, _Mapping]] = ...) -> None: ...

class CombinedPredictionOptions(_message.Message):
    __slots__ = ("base_prediction_options",)
    BASE_PREDICTION_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    base_prediction_options: _containers.RepeatedCompositeFieldContainer[_common_pb2.PredictionOptions]
    def __init__(self, base_prediction_options: _Optional[_Iterable[_Union[_common_pb2.PredictionOptions, _Mapping]]] = ...) -> None: ...

class PredictionOptionsWrapper(_message.Message):
    __slots__ = ("base_prediction_option", "combined_prediction_options")
    BASE_PREDICTION_OPTION_FIELD_NUMBER: _ClassVar[int]
    COMBINED_PREDICTION_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    base_prediction_option: _common_pb2.PredictionOptions
    combined_prediction_options: CombinedPredictionOptions
    def __init__(self, base_prediction_option: _Optional[_Union[_common_pb2.PredictionOptions, _Mapping]] = ..., combined_prediction_options: _Optional[_Union[CombinedPredictionOptions, _Mapping]] = ...) -> None: ...

class DataLocator(_message.Message):
    __slots__ = ("id", "project_id", "data_collection_id", "data_kind", "table", "file_path", "kafka_topic", "druid_table", "prediction_options", "fi_options")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_KIND_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    KAFKA_TOPIC_FIELD_NUMBER: _ClassVar[int]
    DRUID_TABLE_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    FI_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    data_collection_id: str
    data_kind: DataKindWrapper
    table: _common_pb2.TableInfo
    file_path: _common_pb2.LocalFile
    kafka_topic: _common_pb2.KafkaTopic
    druid_table: _common_pb2.DruidTable
    prediction_options: PredictionOptionsWrapper
    fi_options: _common_pb2.FeatureInfluenceOptions
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., data_kind: _Optional[_Union[DataKindWrapper, _Mapping]] = ..., table: _Optional[_Union[_common_pb2.TableInfo, _Mapping]] = ..., file_path: _Optional[_Union[_common_pb2.LocalFile, _Mapping]] = ..., kafka_topic: _Optional[_Union[_common_pb2.KafkaTopic, _Mapping]] = ..., druid_table: _Optional[_Union[_common_pb2.DruidTable, _Mapping]] = ..., prediction_options: _Optional[_Union[PredictionOptionsWrapper, _Mapping]] = ..., fi_options: _Optional[_Union[_common_pb2.FeatureInfluenceOptions, _Mapping]] = ...) -> None: ...
