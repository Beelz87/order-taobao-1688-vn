from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from app.schemas.user_address import UserAddress
from app.schemas.user_finance import UserFinance
from app.schemas.user_role import UserRole


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    account_id: Optional[int] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    user_code: Optional[str] = None
    is_user_code_edited: Optional[bool] = False


# Properties to receive via API on update
class UserUpdate(UserBase):
    user_code: Optional[str] = None

    class Config:
        from_attributes = True


class UserInDBBase(UserBase):
    id: int
    user_role: Optional[UserRole]
    user_addresses: Optional[List[UserAddress]] = None
    user_finance: Optional[UserFinance] = None
    user_code: Optional[str] = None
    is_user_code_edited: Optional[bool] = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
