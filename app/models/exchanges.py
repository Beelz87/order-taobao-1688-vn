from sqlalchemy import Column, String, Boolean, Float, Integer

from app.constants.exchange import ExchangeCurrencyCode, ExchangeType
from app.db.base_class import Base


class Exchange(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    description = Column(String(255))
    foreign_currency = Column(String(4), default=ExchangeCurrencyCode.CNY)
    local_currency = Column(String(4), default=ExchangeCurrencyCode.VND)
    is_active = Column(Boolean(), default=True)
    exchange_rate = Column(Float())
    type = Column(Integer(), default=ExchangeType.BASIC)