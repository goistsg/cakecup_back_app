from uuid import uuid4
from sqlalchemy import Column, ForeignKey, Numeric, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import BaseModel
from .enums import OrderStatus
from .user_entity import UserEntity

class OrderEntity(BaseModel):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'public'}

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.id"), nullable=False)
    items = Column(JSON, nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    status = Column(
        Enum(OrderStatus, name='order_status', create_type=False),
        nullable=False,
        default=OrderStatus.PENDING
    )

    user = relationship('UserEntity', back_populates='orders')
    payment = relationship(
        "PaymentEntity",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan"
    )
