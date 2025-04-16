from typing import List

from pydantic import BaseModel


class UserAddressBase(BaseModel):
    name: str
    phone_number: str
    address: str
    is_active: bool = True


class UserAddressCreate(UserAddressBase):
    pass


class UserAddressUpdate(UserAddressBase):
    pass


class UserAddressInDBBase(UserAddressBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class UserAddress(UserAddressInDBBase):
    pass


# Additional properties stored in DB
class UserAddressInDB(UserAddressInDBBase):
    pass