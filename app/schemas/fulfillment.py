from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import Consignment, Shipment


class FulfillmentBase(BaseModel):
    consignment_id: int
    shipment_id: int
    status: int
    shipping_type: int
    customer_name: Optional[str] = None
    customer_phone_number: Optional[str] = None
    customer_address: Optional[str] = None


# Properties to receive via API on creation
class FulfillmentCreate(FulfillmentBase):
    pass


# Properties to receive via API on update
class FulfillmentUpdate(BaseModel):
    status: int
    shipping_type: int


class FulfillmentInDBBase(FulfillmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Additional properties to return via API
class Fulfillment(FulfillmentInDBBase):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    user_id: Optional[int]

    shipment: Shipment = None
    consignment: Consignment = None


# Additional properties stored in DB
class FulfillmentInDB(FulfillmentInDBBase):
    pass