from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserAddress(Base):
    """
    Database Model for a user_addresses table.
    """
    __tablename__ = "user_addresses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(13), nullable=False)
    address = Column(String(2056), nullable=False)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="user_addresses")