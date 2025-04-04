from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import Consignment


class ShipmentBase(BaseModel):
    consignment_id: int
    shipment_status: int
    finance_status: int


# Properties to receive via API on creation
class ShipmentCreate(ShipmentBase):
    pass


# Properties to receive via API on update
class ShipmentUpdate(BaseModel):
    shipment_status: int
    finance_status: int


class ShipmentInDBBase(ShipmentBase):
    id: int
    consignment: Optional[Consignment]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Additional properties to return via API
class Shipment(ShipmentInDBBase):
    pass


# Additional properties stored in DB
class ShipmentInDB(ShipmentInDBBase):
    pass