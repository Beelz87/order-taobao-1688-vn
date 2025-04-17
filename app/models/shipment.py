from datetime import datetime, UTC

from sqlalchemy import Column, UUID, ForeignKey, String, Integer, DateTime, Float, Boolean, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    consignment_id = Column(Integer, ForeignKey("consignments.id"), nullable=False)
    consignment = relationship("Consignment", back_populates="shipments")

    contains_liquid = Column(Boolean(), nullable=False, default=False)
    is_fragile = Column(Boolean(), nullable=False, default=False)
    wooden_packaging_required = Column(Boolean(), nullable=False, default=False)
    insurance_required = Column(Boolean(), nullable=False, default=False)
    item_count_check_required = Column(Boolean(), nullable=False, default=False)

    contains_liquid_fee = Column(Float(), nullable=False, default=0.0)
    is_fragile_fee = Column(Float(), nullable=False, default=0.0)
    wooden_packaging_required_fee = Column(Float(), nullable=False, default=0.0)
    insurance_required_fee = Column(Float(), nullable=False, default=0.0)
    item_count_check_required_fee = Column(Float(), nullable=False, default=0.0)

    shipment_status = Column(Integer(), nullable=False, default=0)
    finance_status = Column(Integer(), nullable=False, default=0)

    note = Column(Text(), nullable=True)
    code = Column(String(128), nullable=False, default="")

    shipping_fee = Column(Float(), nullable=False, default=0.0)

    created_at = Column(DateTime, index=True, default=datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )

    # Relationships
    fulfillment = relationship("Fulfillment", back_populates="shipment")