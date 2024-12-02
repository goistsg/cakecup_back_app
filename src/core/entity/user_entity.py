from sqlalchemy import Column, String, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel
from .review_entity import ReviewEntity

class UserEntity(BaseModel):
    __tablename__ = 'users'

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(JSON, nullable=False, default={'type': 'user'}) 

    carts = relationship('CartEntity', back_populates='user')
    orders = relationship('OrderEntity', back_populates='user') 
    reviews = relationship(ReviewEntity, back_populates='user')