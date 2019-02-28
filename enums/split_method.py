from enum import Enum

class SplitMethod(Enum):
    DEFAULT = 0
    MOM = 1
    JEROSLOW = 2
    FIRST_AVAILABLE = 3
    pMOM = 4
    OWN_HEURISTIC = 5
