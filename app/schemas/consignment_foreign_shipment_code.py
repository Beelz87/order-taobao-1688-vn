from datetime import datetime, UTC
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class ConsignmentForeignShipmentCodeBase(BaseModel):
    consignment_id: int
    foreign_shipment_code: str

class ConsignmentForeignShipmentCodeCreate(ConsignmentForeignShipmentCodeBase):
    pass

class ConsignmentForeignShipmentCodeUpdate(ConsignmentForeignShipmentCodeBase):
    pass

class ConsignmentForeignShipmentCodeInDBBase(ConsignmentForeignShipmentCodeBase):
    id: int

    class Config:
        from_attributes = True

class ConsignmentForeignShipmentCode(ConsignmentForeignShipmentCodeInDBBase):
    pass

class ConsignmentForeignShipmentCodeInDB(ConsignmentForeignShipmentCodeInDBBase):
    pass
