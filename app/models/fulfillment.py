from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Fulfillment(Base):
    __tablename__ = "fulfillments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    consignment_id = Column(Integer(), ForeignKey("consignments.id"), nullable=False)
    shipment_id = Column(Integer(), ForeignKey("shipments.id"), nullable=False)

    customer_name = Column(String(255), nullable=False)
    customer_phone_number = Column(String(32), nullable=False)
    customer_address = Column(String(2056), nullable=False)

    status = Column(Integer(), nullable=False)
    shipping_type = Column(Integer(), nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )
