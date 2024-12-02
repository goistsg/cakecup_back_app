from enum import Enum

class OrderStatus(str, Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    PAID = 'paid'
    CANCELLED = 'cancelled'
    DELIVERED = 'delivered'

class PaymentStatus(str, Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    APPROVED = 'approved'
    DECLINED = 'declined'
    REFUNDED = 'refunded'

class PaymentMethod(str, Enum):
    CREDIT_CARD = 'credit_card'
    PIX = 'pix'
    BANK_SLIP = 'bank_slip' 