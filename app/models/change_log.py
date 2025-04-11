from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, JSON, DateTime, Index

from app.db.base_class import Base


class ChangeLog(Base):
    __tablename__ = "change_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    object_type = Column(String(100), nullable=False)
    object_id = Column(Integer, index=True, nullable=False)
    action = Column(String(50), nullable=False)
    changes = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))

    __table_args__ = (
        Index("ix_object_type_object_id", "object_type", "object_id"),
        Index("ix_user_id_object_type", "user_id", "object_type")
    )
