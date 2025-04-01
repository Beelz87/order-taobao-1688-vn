from datetime import datetime

from pydantic import BaseModel

from app.constants.deposit import DepositType


class DepositBillBase(BaseModel):
    user_id: int
    user_fullname: str
    amount: float
    deposit_type: int = DepositType.CASH
    note: str
    created_at: datetime

class DepositBillCreate(DepositBillBase):
    pass

class DepositBillUpdate(BaseModel):
    pass

class DepositBillInDBBase(DepositBillBase):
    id: int

    class Config:
        from_attributes = True

# Additional properties to return via API
class DepositBill(DepositBillInDBBase):
    pass

# Additional properties stored in DB
class DepositBillInDB(DepositBillInDBBase):
    pass