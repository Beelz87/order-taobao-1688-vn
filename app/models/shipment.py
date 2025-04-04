from datetime import datetime, UTC

from sqlalchemy import Column, UUID, ForeignKey, String, Integer, DateTime, Float, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    consignment_id = Column(Integer, ForeignKey("consignments.id"), nullable=False)
    consignment = relationship("Consignment", back_populates="shipment")

    shipment_status = Column(Integer(), nullable=False, default=0)
    finance_status = Column(Integer(), nullable=False, default=0)
    created_at = Column(DateTime, index=True, default=datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )
