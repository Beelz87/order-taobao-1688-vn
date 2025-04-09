from enum import Enum


class StoreType(str, Enum):
    SOURCE = 0
    DESTINATION = 1