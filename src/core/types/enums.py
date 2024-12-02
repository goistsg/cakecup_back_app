from enum import Enum

class OrderStatus(Enum):
    PENDING = 'pending'
    PROCESSING = 'processing',
    PAID = 'paid',
    CANCELLED = 'cancelled',
    DELIVERED = 'delivered'

class PaymentStatus(Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    APPROVED = 'approved'
    DECLINED = 'declined'
    REFUNDED = 'refunded'
    CANCELLED = 'cancelled'

class PaymentMethod(Enum):
    CREDIT_CARD = 'credit_card'
    PIX = 'pix'
    BANK_SLIP = 'bank_slip'
