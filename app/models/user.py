from datetime import datetime, UTC
from app.db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Integer
from sqlalchemy.orm import relationship


class User(Base):
    """
    Database Model for an application user
    """

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(255), index=True)
    user_code = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone_number = Column(String(13), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_user_code_edited = Column(Boolean(), default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )

    account_id = Column(
        Integer(), ForeignKey("accounts.id"), nullable=False
    )

    user_role = relationship("UserRole", back_populates="user", uselist=False)
    account = relationship("Account", back_populates="users")
    consignments = relationship("Consignment", back_populates="user")
    deposit_bills = relationship("DepositBill", back_populates="user")
    addresses = relationship("UserAddress", back_populates="user")
