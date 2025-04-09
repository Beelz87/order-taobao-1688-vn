from datetime import datetime, UTC
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship

from app.constants.store import StoreType
from app.db.base_class import Base


class Store(Base):
    """
    Database Model for a store
    """

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(String(255), index=True)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean(), default=True)
    type_store = Column(Integer, default=StoreType.SOURCE.value)
    code = Column(String(255), unique=True, nullable=True)

    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )

    source_consignments = relationship(
        "Consignment",
        back_populates="source_store",
        foreign_keys="Consignment.source_store_id"
    )

    dest_consignments = relationship(
        "Consignment",
        back_populates="dest_store",
        foreign_keys="Consignment.dest_store_id"
    )