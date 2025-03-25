from datetime import datetime

from pydantic import BaseModel, UUID4


class ShippingOrderBase(BaseModel):
    user_id: UUID4
    send_store_id: UUID4
    receive_store_id: UUID4
    shipping_name: str
    shipping_address: str
    shipping_phone_number: str
    shipping_status: int
    store_status: int
    weight: float
    height: float
    wide: float
    length: float
    weight_packaged: float
    height_packaged: float
    wide_packaged: float
    length_packaged: float
    wood_packaged_fee: float
    created_at: datetime
    updated_at: datetime


# Properties to receive via API on creation
class ShippingOrderCreate(ShippingOrderBase):
    pass


# Properties to receive via API on update
class ShippingOrderUpdate(ShippingOrderBase):
    pass


class ShippingOrderInDBBase(ShippingOrderBase):
    id: UUID4
    send_store_id: UUID4
    receive_store_id: UUID4
    shipping_name: str
    shipping_address: str
    shipping_phone_number: str
    shipping_status: int
    store_status: int
    weight: float
    height: float
    wide: float
    length: float
    weight_packaged: float
    height_packaged: float
    wide_packaged: float
    length_packaged: float
    wood_packaged_fee: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Additional properties to return via API
class ShippingOrder(ShippingOrderInDBBase):
    pass


# Additional properties stored in DB
class ShippingOrderInDB(ShippingOrderInDBBase):
    pass