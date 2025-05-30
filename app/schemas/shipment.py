from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import Consignment


class ShipmentBase(BaseModel):
    consignment_id: int
    shipment_status: int
    finance_status: int

    contains_liquid: bool = False
    is_fragile: bool = False
    wooden_packaging_required: bool = False
    insurance_required: bool = False
    item_count_check_required: bool = False

    contains_liquid_fee: float = 0.0
    is_fragile_fee: float = 0.0
    wooden_packaging_required_fee: float = 0.0
    insurance_required_fee: float = 0.0
    item_count_check_required_fee: float = 0.0

    domestic_shipping_fee: float = 0.0

    weight: float = 0.0
    height: float = 0.0
    wide: float = 0.0
    length: float = 0.0

    weight_packaged: float = 0.0
    height_packaged: float = 0.0
    wide_packaged: float = 0.0
    length_packaged: float = 0.0

    code: str
    note: Optional[str] = None


# Properties to receive via API on creation
class ShipmentCreate(ShipmentBase):
    user_id: Optional[int] = None
    pass


# Properties to receive via API on update
class ShipmentUpdate(BaseModel):
    shipment_status: int
    finance_status: int

    contains_liquid: bool = False
    is_fragile: bool = False
    wooden_packaging_required: bool = False
    insurance_required: bool = False
    item_count_check_required: bool = False

    contains_liquid_fee: float = 0.0
    is_fragile_fee: float = 0.0
    wooden_packaging_required_fee: float = 0.0
    insurance_required_fee: float = 0.0
    item_count_check_required_fee: float = 0.0

    weight: float = 0.0
    height: float = 0.0
    wide: float = 0.0
    length: float = 0.0

    weight_packaged: float = 0.0
    height_packaged: float = 0.0
    wide_packaged: float = 0.0
    length_packaged: float = 0.0

    domestic_shipping_fee: float = 0.0


class ShipmentInDBBase(ShipmentBase):
    id: int
    user_id: Optional[int]
    consignment: Optional[Consignment]
    created_at: datetime
    updated_at: datetime

    weight: float
    height: float
    wide: float
    length: float
    weight_packaged: float
    height_packaged: float
    wide_packaged: float
    length_packaged: float

    class Config:
        from_attributes = True


# Additional properties to return via API
class Shipment(ShipmentInDBBase):
    pass


# Additional properties stored in DB
class ShipmentInDB(ShipmentInDBBase):
    pass