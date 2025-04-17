from datetime import datetime, UTC

from sqlalchemy import Column, Integer, Float, Text, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.constants.deposit import DepositStatus
from app.db.base_class import Base


class DepositBill(Base):
    __tablename__ = "deposit_bills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_fullname = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    deposit_type = Column(Integer, nullable=False)
    note = Column(Text, nullable=True)
    status = Column(Integer, default=DepositStatus.PENDING.value)
    created_at = Column(DateTime, index=True, default=datetime.now(UTC))
    updated_at = Column(DateTime, index=True, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    user = relationship("User", back_populates="deposit_bills")