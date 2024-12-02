from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from src.core.entity.cart_entity import CartEntity
from enum import Enum

class CartStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    ABANDONED = "abandoned"

class CartBase(BaseModel):
    user_id: UUID
    total: float = 0.0
    status: str = "active"
    items: List[dict] = []
    
class CartCreate(CartBase):
    pass

class CartUpdate(BaseModel):
    user_id: Optional[UUID] = None
    total: Optional[float] = None
    status: Optional[str] = None
    items: Optional[List[dict]] = None

class Cart(CartBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: 'CartEntity') -> 'Cart':
        return Cart(
            id=entity.id,
            user_id=entity.user_id,
            total=entity.total,
            status=entity.status,
            items=entity.items,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        ) 