from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime
from src.core.entity.order_entity import OrderStatus

class OrderItemDTO(BaseModel):
    id: str
    name: str
    quantity: int
    price: float

class CreateOrderDTO(BaseModel):
    user_id: UUID4
    cart_id: UUID4

class OrderResponseDTO(BaseModel):
    id: UUID4
    user_id: UUID4
    items: List[OrderItemDTO]
    total: float
    status: OrderStatus
    payment_id: Optional[UUID4]
    created_at: datetime
    updated_at: datetime 