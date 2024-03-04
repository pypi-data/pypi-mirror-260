from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NNBackend(_message.Message):
    __slots__ = ()
    class Backend(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[NNBackend.Backend]
        PYTORCH: _ClassVar[NNBackend.Backend]
        TENSORFLOW_V1: _ClassVar[NNBackend.Backend]
        TENSORFLOW_V2: _ClassVar[NNBackend.Backend]
        KERAS: _ClassVar[NNBackend.Backend]
    UNKNOWN: NNBackend.Backend
    PYTORCH: NNBackend.Backend
    TENSORFLOW_V1: NNBackend.Backend
    TENSORFLOW_V2: NNBackend.Backend
    KERAS: NNBackend.Backend
    def __init__(self) -> None: ...

class LayerAnchor(_message.Message):
    __slots__ = ()
    class Anchor(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[LayerAnchor.Anchor]
        IN: _ClassVar[LayerAnchor.Anchor]
        OUT: _ClassVar[LayerAnchor.Anchor]
    INVALID: LayerAnchor.Anchor
    IN: LayerAnchor.Anchor
    OUT: LayerAnchor.Anchor
    def __init__(self) -> None: ...

class RNNAttributionConfig(_message.Message):
    __slots__ = ("nn_backend", "forward_padded", "baseline_split", "n_baseline_records", "input_layer", "input_anchor", "n_time_step_input", "n_features_input", "output_layer", "output_anchor", "n_time_step_output", "n_output_neurons", "internal_layer", "internal_anchor", "n_internal_neurons", "use_training_mode")
    NN_BACKEND_FIELD_NUMBER: _ClassVar[int]
    FORWARD_PADDED_FIELD_NUMBER: _ClassVar[int]
    BASELINE_SPLIT_FIELD_NUMBER: _ClassVar[int]
    N_BASELINE_RECORDS_FIELD_NUMBER: _ClassVar[int]
    INPUT_LAYER_FIELD_NUMBER: _ClassVar[int]
    INPUT_ANCHOR_FIELD_NUMBER: _ClassVar[int]
    N_TIME_STEP_INPUT_FIELD_NUMBER: _ClassVar[int]
    N_FEATURES_INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_LAYER_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ANCHOR_FIELD_NUMBER: _ClassVar[int]
    N_TIME_STEP_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    N_OUTPUT_NEURONS_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_LAYER_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_ANCHOR_FIELD_NUMBER: _ClassVar[int]
    N_INTERNAL_NEURONS_FIELD_NUMBER: _ClassVar[int]
    USE_TRAINING_MODE_FIELD_NUMBER: _ClassVar[int]
    nn_backend: NNBackend.Backend
    forward_padded: bool
    baseline_split: str
    n_baseline_records: int
    input_layer: str
    input_anchor: LayerAnchor.Anchor
    n_time_step_input: int
    n_features_input: int
    output_layer: str
    output_anchor: LayerAnchor.Anchor
    n_time_step_output: int
    n_output_neurons: int
    internal_layer: str
    internal_anchor: LayerAnchor.Anchor
    n_internal_neurons: int
    use_training_mode: bool
    def __init__(self, nn_backend: _Optional[_Union[NNBackend.Backend, str]] = ..., forward_padded: bool = ..., baseline_split: _Optional[str] = ..., n_baseline_records: _Optional[int] = ..., input_layer: _Optional[str] = ..., input_anchor: _Optional[_Union[LayerAnchor.Anchor, str]] = ..., n_time_step_input: _Optional[int] = ..., n_features_input: _Optional[int] = ..., output_layer: _Optional[str] = ..., output_anchor: _Optional[_Union[LayerAnchor.Anchor, str]] = ..., n_time_step_output: _Optional[int] = ..., n_output_neurons: _Optional[int] = ..., internal_layer: _Optional[str] = ..., internal_anchor: _Optional[_Union[LayerAnchor.Anchor, str]] = ..., n_internal_neurons: _Optional[int] = ..., use_training_mode: bool = ...) -> None: ...

class RNNUIConfig(_message.Message):
    __slots__ = ("default_classification_threshold",)
    DEFAULT_CLASSIFICATION_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    default_classification_threshold: float
    def __init__(self, default_classification_threshold: _Optional[float] = ...) -> None: ...

class NLPAttributionConfig(_message.Message):
    __slots__ = ("n_metrics_records", "token_embeddings_layer", "token_embeddings_anchor", "output_layer", "output_anchor", "n_output_neurons", "ref_token", "shuffle_data", "resolution", "rebatch_size", "use_training_mode")
    N_METRICS_RECORDS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_EMBEDDINGS_LAYER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_EMBEDDINGS_ANCHOR_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_LAYER_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ANCHOR_FIELD_NUMBER: _ClassVar[int]
    N_OUTPUT_NEURONS_FIELD_NUMBER: _ClassVar[int]
    REF_TOKEN_FIELD_NUMBER: _ClassVar[int]
    SHUFFLE_DATA_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    REBATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    USE_TRAINING_MODE_FIELD_NUMBER: _ClassVar[int]
    n_metrics_records: int
    token_embeddings_layer: str
    token_embeddings_anchor: LayerAnchor.Anchor
    output_layer: str
    output_anchor: LayerAnchor.Anchor
    n_output_neurons: int
    ref_token: str
    shuffle_data: bool
    resolution: int
    rebatch_size: int
    use_training_mode: bool
    def __init__(self, n_metrics_records: _Optional[int] = ..., token_embeddings_layer: _Optional[str] = ..., token_embeddings_anchor: _Optional[_Union[LayerAnchor.Anchor, str]] = ..., output_layer: _Optional[str] = ..., output_anchor: _Optional[_Union[LayerAnchor.Anchor, str]] = ..., n_output_neurons: _Optional[int] = ..., ref_token: _Optional[str] = ..., shuffle_data: bool = ..., resolution: _Optional[int] = ..., rebatch_size: _Optional[int] = ..., use_training_mode: bool = ...) -> None: ...
