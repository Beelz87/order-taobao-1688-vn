from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel


class ConsignmentBase(BaseModel):
    user_id: int
    store_id: int
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
    created_at: datetime
    updated_at: datetime

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

    number_of_packages: int
    domestic_shipping_fee: float = 0.0
    product_category_id: int

    foreign_shipping_codes: List[str] = None
    image_base64: str = None


# Properties to receive via API on creation
class ConsignmentCreate(ConsignmentBase):
    image_path: Optional[str] = None


# Properties to receive via API on update
class ConsignmentUpdate(ConsignmentBase):
    pass


class ConsignmentInDBBase(ConsignmentBase):
    id: int
    code: str

    class Config:
        from_attributes = True


# Additional properties to return via API
class Consignment(ConsignmentInDBBase):
    pass


# Additional properties stored in DB
class ConsignmentInDB(ConsignmentInDBBase):
    pass
