from datetime import datetime

from pydantic import BaseModel


class StoreBase(BaseModel):
    name: str
    description: str
    is_active: bool
    type_store: int
    code: str
    base_fee: float


# Properties to receive via API on creation
class StoreCreate(StoreBase):
    pass


# Properties to receive via API on update
class StoreUpdate(StoreBase):
    pass


class StoreInDBBase(StoreBase):
    id: int
    name: str
    description: str
    is_active: bool
    type_store: int
    code: str
    base_fee: float

    class Config:
        from_attributes = True


# Additional properties to return via API
class Store(StoreInDBBase):
    pass


# Additional properties stored in DB
class StoreInDB(StoreInDBBase):
    pass
