from uuid import uuid4
from sqlalchemy import Column, ForeignKey, Numeric, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import BaseModel
from .enums import PaymentStatus, PaymentMethod
from .order_entity import OrderEntity

class PaymentEntity(BaseModel):
    __tablename__ = 'payments'
    __table_args__ = {'schema': 'public'}

    order_id = Column(
        UUID(as_uuid=True), 
        ForeignKey('public.orders.id', ondelete='CASCADE'), 
        nullable=False,
        unique=True  # Garante que um pagamento pertence a apenas um pedido
    )
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    payment_details = Column(JSON, nullable=True)

    # Relacionamento
    order = relationship(
        "OrderEntity",
        back_populates="payment",
        single_parent=True  # Garante que um pagamento tem apenas um pedido
    ) 