from datetime import datetime, UTC
from uuid import uuid4

from app.db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Account(Base):
    """
    Database model for an account
    """

    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name = Column(String(255), index=True, nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean(), default=True)
    plan_id = Column(UUID(as_uuid=True), index=True, default=None)
    current_subscription_ends = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )

    users = relationship("User", back_populates="account")
