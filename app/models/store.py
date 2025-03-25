from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy import Column, UUID, String, Boolean, DateTime

from app.db.base_class import Base


class Store(Base):
    """
    Database Model for a store
    """

    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name = Column(String(255), index=True)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )