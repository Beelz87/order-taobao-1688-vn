from enum import Enum


class ObjectType(Enum):
    SHIPMENT = 1
    EXCHANGE = 2
    DEPOSIT_BILL = 3


class ActionType(Enum):
    CREATE = 0
    UPDATE = 1
    DELETE = 2