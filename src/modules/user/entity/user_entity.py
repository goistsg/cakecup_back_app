from sqlalchemy import Column, String, Boolean, JSON, DateTime, UUID
from sqlalchemy.sql import func
from cakecup_back_app.src.core.providers.async_orm_provider import Base
import uuid

class UserEntity(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(JSON, nullable=True)

    created_by = Column(UUID, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())