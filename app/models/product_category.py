from sqlalchemy import Column, UUID, String, Integer, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    category_parent_id = Column(Integer(), nullable=True, default=0)
    level = Column(Integer(), nullable=False, default=0)
    is_active = Column(Boolean(), nullable=False, default=True)

    consignments = relationship("Consignment", back_populates="product_category")
