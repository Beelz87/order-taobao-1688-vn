from datetime import datetime

from pydantic import BaseModel

from app.constants.deposit import DepositType, DepositStatus


class DepositBillBase(BaseModel):
    user_id: int
    user_fullname: str
    amount: float
    deposit_type: int = DepositType.CASH
    note: str
    status: int = DepositStatus.PENDING.value

class DepositBillCreate(DepositBillBase):
    pass

class DepositBillUpdate(BaseModel):
    deposit_type: int = DepositType.CASH
    note: str
    status: int = DepositStatus.PENDING.value

class DepositBillInDBBase(DepositBillBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Additional properties to return via API
class DepositBill(DepositBillInDBBase):
    pass

# Additional properties stored in DB
class DepositBillInDB(DepositBillInDBBase):
    pass