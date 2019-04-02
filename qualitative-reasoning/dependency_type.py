from enum import Enum

class DependencyType(Enum):
    Default = 0
    PositiveInfluence = 1
    NegativeInfluence = 2
    PositiveProportionality = 3
    NegativeProportionality = 4