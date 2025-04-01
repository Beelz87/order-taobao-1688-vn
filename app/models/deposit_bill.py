from datetime import datetime, UTC

from sqlalchemy import Column, Integer, Float, Text, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class DepositBill(Base):
    __tablename__ = "deposit_bills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_fullname = Column(String(255))
    amount = Column(Float)
    deposit_type = Column(Integer)
    note = Column(Text)
    created_at = Column(DateTime, index=True, default=datetime.now(UTC))

    user = relationship("User", back_populates="deposit_bills")