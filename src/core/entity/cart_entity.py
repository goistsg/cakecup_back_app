from sqlalchemy import Column, ForeignKey, String, Numeric, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import BaseModel

class CartEntity(BaseModel):
    __tablename__ = 'carts'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    total = Column(Numeric(10, 2), default=0.0)
    status = Column(String(50), default='active')
    items = Column(JSON, default=[])
    is_active = Column(Boolean, default=True)

    user = relationship('UserEntity', back_populates='carts')
 