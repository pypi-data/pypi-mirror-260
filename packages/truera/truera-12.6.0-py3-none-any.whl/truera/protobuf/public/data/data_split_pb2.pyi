from google.protobuf import timestamp_pb2 as _timestamp_pb2
from truera.protobuf.public.util import split_mode_pb2 as _split_mode_pb2
from truera.protobuf.public.util import time_range_pb2 as _time_range_pb2
from truera.protobuf.public import metadata_message_types_pb2 as _metadata_message_types_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataSplitType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALL_SPLIT: _ClassVar[DataSplitType]
    TRAIN_SPLIT: _ClassVar[DataSplitType]
    TEST_SPLIT: _ClassVar[DataSplitType]
    VALIDATE_SPLIT: _ClassVar[DataSplitType]
    OOT_SPLIT: _ClassVar[DataSplitType]
    PROD_SPLIT: _ClassVar[DataSplitType]
    TIMERANGE_SPLIT: _ClassVar[DataSplitType]
    CUSTOM_SPLIT: _ClassVar[DataSplitType]
    EVAL_DATASET: _ClassVar[DataSplitType]
    EXPERIMENT_DATASET: _ClassVar[DataSplitType]
ALL_SPLIT: DataSplitType
TRAIN_SPLIT: DataSplitType
TEST_SPLIT: DataSplitType
VALIDATE_SPLIT: DataSplitType
OOT_SPLIT: DataSplitType
PROD_SPLIT: DataSplitType
TIMERANGE_SPLIT: DataSplitType
CUSTOM_SPLIT: DataSplitType
EVAL_DATASET: DataSplitType
EXPERIMENT_DATASET: DataSplitType

class DataSplit(_message.Message):
    __slots__ = ("id", "name", "description", "split_type", "dataset_id", "project_id", "preprocessed_locator", "processed_locator", "label_locator", "extra_data_locator", "tags", "created_at", "derived_from", "provenance", "time_range", "unique_id_column_name", "timestamp_column_name", "created_on", "updated_on", "split_mode", "status", "time_window_filter", "prediction_score_types", "options_hashes", "rows_written")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SPLIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PREPROCESSED_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    LABEL_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    EXTRA_DATA_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DERIVED_FROM_FIELD_NUMBER: _ClassVar[int]
    PROVENANCE_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_ON_FIELD_NUMBER: _ClassVar[int]
    UPDATED_ON_FIELD_NUMBER: _ClassVar[int]
    SPLIT_MODE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FILTER_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_SCORE_TYPES_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_HASHES_FIELD_NUMBER: _ClassVar[int]
    ROWS_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    split_type: DataSplitType
    dataset_id: str
    project_id: str
    preprocessed_locator: str
    processed_locator: str
    label_locator: str
    extra_data_locator: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    created_at: _timestamp_pb2.Timestamp
    derived_from: DerivedSplitInfo
    provenance: _metadata_message_types_pb2.DataProvenance
    time_range: _time_range_pb2.TimeRange
    unique_id_column_name: str
    timestamp_column_name: str
    created_on: str
    updated_on: str
    split_mode: _split_mode_pb2.SplitMode
    status: _metadata_message_types_pb2.SplitStatus
    time_window_filter: _metadata_message_types_pb2.TimeWindowFilter
    prediction_score_types: _containers.RepeatedScalarFieldContainer[_qoi_pb2.QuantityOfInterest]
    options_hashes: _containers.RepeatedScalarFieldContainer[str]
    rows_written: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., split_type: _Optional[_Union[DataSplitType, str]] = ..., dataset_id: _Optional[str] = ..., project_id: _Optional[str] = ..., preprocessed_locator: _Optional[str] = ..., processed_locator: _Optional[str] = ..., label_locator: _Optional[str] = ..., extra_data_locator: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., derived_from: _Optional[_Union[DerivedSplitInfo, _Mapping]] = ..., provenance: _Optional[_Union[_metadata_message_types_pb2.DataProvenance, _Mapping]] = ..., time_range: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ..., unique_id_column_name: _Optional[str] = ..., timestamp_column_name: _Optional[str] = ..., created_on: _Optional[str] = ..., updated_on: _Optional[str] = ..., split_mode: _Optional[_Union[_split_mode_pb2.SplitMode, str]] = ..., status: _Optional[_Union[_metadata_message_types_pb2.SplitStatus, str]] = ..., time_window_filter: _Optional[_Union[_metadata_message_types_pb2.TimeWindowFilter, _Mapping]] = ..., prediction_score_types: _Optional[_Iterable[_Union[_qoi_pb2.QuantityOfInterest, str]]] = ..., options_hashes: _Optional[_Iterable[str]] = ..., rows_written: _Optional[int] = ...) -> None: ...

class DerivedSplitInfo(_message.Message):
    __slots__ = ("parent_id", "segmentation_id", "segment_index")
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENTATION_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    parent_id: str
    segmentation_id: str
    segment_index: str
    def __init__(self, parent_id: _Optional[str] = ..., segmentation_id: _Optional[str] = ..., segment_index: _Optional[str] = ...) -> None: ...
