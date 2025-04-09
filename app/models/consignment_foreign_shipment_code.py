from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ConsignmentForeignShipmentCode(Base):
    __tablename__ = "consignment_foreign_shipment_codes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    consignment_id = Column(Integer, ForeignKey("consignments.id"), index=True, nullable=False)
    consignment = relationship("Consignment", back_populates="foreign_shipment_codes")
    foreign_shipment_code = Column(String(255), index=True, nullable=False)