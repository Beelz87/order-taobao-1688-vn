from enum import Enum


class DepositType(Enum):
    CASH = 1
    BANKING = 2


class DepositStatus(Enum):
    PENDING = 1
    APPROVED = 2
    NOT_APPROVED = 3