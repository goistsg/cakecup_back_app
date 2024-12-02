from sqlalchemy import Column, ForeignKey, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.core.entity.base import BaseModel

class ReviewEntity(BaseModel):
    __tablename__ = "reviews"

    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    rating = Column(Numeric(10, 2), nullable=False)
    comment = Column(String)

    product = relationship('ProductEntity', back_populates='reviews', lazy='joined')
    user = relationship('UserEntity', back_populates='reviews', lazy='joined')
