from pydantic import BaseModel


class ExchangeBase(BaseModel):
    name: str
    description: str
    foreign_currency: str
    local_currency: str
    is_active: bool
    exchange_rate: float
    type: int


class ExchangeCreate(ExchangeBase):
    pass

class ExchangeUpdate(BaseModel):
    pass

class ExchangeInDBBase(ExchangeBase):
    id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class Exchange(ExchangeInDBBase):
    pass


# Additional properties stored in DB
class ExchangeInDB(ExchangeInDBBase):
    pass
