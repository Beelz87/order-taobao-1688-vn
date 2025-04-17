from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.consignment_foreign_shipment_code import ConsignmentForeignShipmentCode


class ConsignmentBase(BaseModel):
    user_id: int
    source_store_id: int
    dest_store_id: int
    user_address_id: int
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

    number_of_packages: int
    domestic_shipping_fee: float = 0.0
    product_category_id: Optional[int] = None
    product_name: Optional[str] = None

    foreign_shipment_codes: List[str] = None
    image_base64: Optional[str] = None


# Properties to receive via API on creation
class ConsignmentCreate(ConsignmentBase):
    image_path: Optional[str] = None


# Properties to receive via API on update
class ConsignmentUpdate(ConsignmentBase):
    pass


class ConsignmentInDBBase(BaseModel):
    id: int
    user_id: int
    source_store_id: int
    dest_store_id: int
    user_address_id: int
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

    number_of_packages: int
    domestic_shipping_fee: float = 0.0
    product_category_id: Optional[int] = None
    product_name: Optional[str] = None
    code: str
    image_path: Optional[str] = None

    foreign_shipment_codes: Optional[List[ConsignmentForeignShipmentCode]] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class Consignment(ConsignmentInDBBase):
    pass


# Additional properties stored in DB
class ConsignmentInDB(ConsignmentInDBBase):
    pass
