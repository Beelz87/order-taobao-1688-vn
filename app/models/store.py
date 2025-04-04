from datetime import datetime, UTC
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Store(Base):
    """
    Database Model for a store
    """

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(String(255), index=True)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )

    consignments = relationship("Consignment", back_populates="store")