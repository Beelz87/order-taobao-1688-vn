from uuid import uuid4

from sqlalchemy import Column, UUID, String, Boolean, Float, Integer

from app.constants.exchange import ExchangeCurrencyCode, ExchangeType
from app.db.base_class import Base


class Exchange(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name = Column(String(255), index=True, nullable=False)
    description = Column(String(255))
    foreign_currency = Column(String(4), default=ExchangeCurrencyCode.CNY)
    local_currency = Column(String(4), default=ExchangeCurrencyCode.VND)
    is_active = Column(Boolean(), default=True)
    exchange_rate = Column(Float())
    type = Column(Integer(), default=ExchangeType.BASIC)