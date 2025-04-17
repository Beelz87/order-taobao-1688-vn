from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserFinanceBase(BaseModel):
    user_id: Optional[int]
    balance: float


class UserFinanceCreate(UserFinanceBase):
    pass


class UserFinanceUpdate(BaseModel):
    balance: float


class UserFinanceInDBBase(UserFinanceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserFinance(UserFinanceInDBBase):
    pass


class UserFinanceInDB(UserFinanceInDBBase):
    pass