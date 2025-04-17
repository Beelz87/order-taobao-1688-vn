from datetime import datetime, UTC

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserFinance(Base):
    __tablename__ = "user_finances"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="user_finance", uselist=False)

    balance = Column(Float, nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.now(UTC))
    updated_at = Column(DateTime, index=True, default=datetime.now(UTC), onupdate=datetime.now(UTC))