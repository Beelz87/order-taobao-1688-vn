from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy import Column, UUID, ForeignKey, String, Integer, DateTime, Float, Boolean

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

    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )

    shipping_address = Column(String(2056), nullable=False)

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

    image_path = Column(String(255), nullable=True)



