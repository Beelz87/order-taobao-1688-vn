from enum import Enum


class ShipmentStatus(Enum):
    FOREIGN_SHIPPING = 0
    FOREIGN_STORE_RECEIVED = 1
    VN_RECEIVED = 2
    VN_SHIPPING = 3
    VN_COMPLETED = 4


class ShipmentFinanceStatus(Enum):
    NOT_APPROVED = 0
    approved = 1