from uuid import uuid4

from sqlalchemy import Column, UUID, String, Integer, Boolean

from app.db.base_class import Base


class ProductCategory(Base):
    __tablename__ = "product_categories"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    category_parent_id = Column(UUID(as_uuid=True), nullable=True)
    level = Column(Integer(), nullable=False, default=0)
    is_active = Column(Boolean(), nullable=False, default=True)