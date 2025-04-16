from datetime import datetime, UTC

from sqlalchemy import Column, UUID, ForeignKey, String, Integer, DateTime, Float, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Consignment(Base):
    __tablename__ = "consignments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="consignments")

    shipping_name = Column(String(255), nullable=False)
    shipping_phone_number = Column(String(13), nullable=False)
    shipping_address = Column(String(2056), nullable=False)

    source_store_id = Column(
        Integer, ForeignKey("stores.id"), nullable=False, index=True
    )
    dest_store_id = Column(
        Integer, ForeignKey("stores.id"), nullable=False, index=True
    )
    source_store = relationship(
        "Store",
        foreign_keys="Consignment.source_store_id",
        back_populates="source_consignments"
    )
    dest_store = relationship(
        "Store",
        foreign_keys="Consignment.dest_store_id",
        back_populates="dest_consignments"
    )

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

    created_at = Column(DateTime, index=True, default=datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )

    image_path = Column(String(255), nullable=True)
    product_name = Column(String(255), nullable=True)
    product_category_id = Column(
        Integer(), ForeignKey("product_categories.id"), nullable=True
    )
    product_category = relationship("ProductCategory", back_populates="consignments")

    number_of_packages = Column(Integer(), nullable=False, default=1)
    domestic_shipping_fee = Column(Float(), nullable=False, default=0.0)
    code = Column(String(255), nullable=False, index=True)

    shipments = relationship("Shipment", back_populates="consignment")
    foreign_shipment_codes = relationship("ConsignmentForeignShipmentCode", back_populates="consignment")
    fulfillments = relationship("Fulfillment", back_populates="consignment")

