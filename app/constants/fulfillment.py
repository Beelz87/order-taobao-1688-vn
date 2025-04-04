from enum import Enum


class FulfillmentShippingType(Enum):
    BUS_SHIPMENT = 0
    GHTK = 1
    VT_POST = 2
    URBAN_DELIVERY = 3
    PICKUP_AT_WAREHOUSE = 4


class FulfillmentStatus(Enum):
    WAITING = 0
    SHIPPING = 1
    SHIPPED = 2