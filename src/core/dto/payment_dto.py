from pydantic import BaseModel, UUID4
from typing import Optional, Dict
from datetime import datetime
from src.core.entity.payment_entity import PaymentStatus, PaymentMethod

class CreatePaymentDTO(BaseModel):
    order_id: UUID4
    amount: float
    payment_method: PaymentMethod
    payment_details: Dict

class PaymentResponseDTO(BaseModel):
    id: UUID4
    order_id: UUID4
    amount: float
    payment_method: PaymentMethod
    status: PaymentStatus
    payment_details: Optional[Dict]
    created_at: datetime
    updated_at: datetime 