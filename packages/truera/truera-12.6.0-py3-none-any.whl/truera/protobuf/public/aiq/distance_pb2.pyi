from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class DistanceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_DISTANCE_TYPE: _ClassVar[DistanceType]
    CATEGORICAL_WASSERSTEIN_ORDERED: _ClassVar[DistanceType]
    CATEGORICAL_WASSERSTEIN_UNORDERED: _ClassVar[DistanceType]
    TOTAL_VARIATION_DISTANCE: _ClassVar[DistanceType]
    CATEGORICAL_JENSEN_SHANNON_DISTANCE: _ClassVar[DistanceType]
    CHI_SQUARE_TEST: _ClassVar[DistanceType]
    CATEGORICAL_POPULATION_STABILITY_INDEX: _ClassVar[DistanceType]
    L1: _ClassVar[DistanceType]
    L2: _ClassVar[DistanceType]
    LInfinity: _ClassVar[DistanceType]
    NUMERICAL_WASSERSTEIN: _ClassVar[DistanceType]
    DIFFERENCE_OF_MEAN: _ClassVar[DistanceType]
    NUMERICAL_JENSEN_SHANNON_DISTANCE: _ClassVar[DistanceType]
    ENERGY_DISTANCE: _ClassVar[DistanceType]
    KOLMOGOROV_SMIRNOV_STATISTIC: _ClassVar[DistanceType]
    NUMERICAL_POPULATION_STABILITY_INDEX: _ClassVar[DistanceType]
UNKNOWN_DISTANCE_TYPE: DistanceType
CATEGORICAL_WASSERSTEIN_ORDERED: DistanceType
CATEGORICAL_WASSERSTEIN_UNORDERED: DistanceType
TOTAL_VARIATION_DISTANCE: DistanceType
CATEGORICAL_JENSEN_SHANNON_DISTANCE: DistanceType
CHI_SQUARE_TEST: DistanceType
CATEGORICAL_POPULATION_STABILITY_INDEX: DistanceType
L1: DistanceType
L2: DistanceType
LInfinity: DistanceType
NUMERICAL_WASSERSTEIN: DistanceType
DIFFERENCE_OF_MEAN: DistanceType
NUMERICAL_JENSEN_SHANNON_DISTANCE: DistanceType
ENERGY_DISTANCE: DistanceType
KOLMOGOROV_SMIRNOV_STATISTIC: DistanceType
NUMERICAL_POPULATION_STABILITY_INDEX: DistanceType
