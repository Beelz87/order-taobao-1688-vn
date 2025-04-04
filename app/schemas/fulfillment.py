from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import Consignment


class FulfillmentBase(BaseModel):
    consignment_id: int
    shipment_id: int
    status: int
    shipping_type: int


# Properties to receive via API on creation
class FulfillmentCreate(FulfillmentBase):
    customer_name: str
    customer_phone_number: str
    customer_address: str


# Properties to receive via API on update
class FulfillmentUpdate(BaseModel):
    status: int
    shipping_type: int


class FulfillmentInDBBase(FulfillmentBase):
    id: int
    consignment: Optional[Consignment]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Additional properties to return via API
class Fulfillment(FulfillmentInDBBase):
    customer_name: str
    customer_phone_number: str
    customer_address: str


# Additional properties stored in DB
class FulfillmentInDB(FulfillmentInDBBase):
    pass