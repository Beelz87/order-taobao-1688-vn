from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy import Column, UUID, ForeignKey, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ShippingOrder(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    shipping_name = Column(String(255), nullable=False)
    shipping_phone_number = Column(String(13), nullable=False)

    send_store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id"))
    receive_store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id"))

    shipping_status = Column(Integer(), nullable=False)
    store_status = Column(Integer(), nullable=False)

    weight = Column(Float(), nullable=False)
    height = Column(Float(), nullable=False)
    wide = Column(Float(), nullable=False)
    length = Column(Float(), nullable=False)

    weight_packaged = Column(Float(), nullable=False)
    height_packaged = Column(Float(), nullable=False)
    wide_packaged = Column(Float(), nullable=False)
    length_packaged = Column(Float(), nullable=False)

    wood_packaged_fee = Column(Float(), nullable=False)

    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )


