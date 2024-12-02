from nest.core import Module
# from src.modules.payments.services.payment_gateway_service import PaymentGatewayService
from src.modules.payments.services.payment_service import PaymentService
from src.modules.payments.repositories.payment_repository import PaymentRepository

@Module(
    controllers=[],
    providers=[
        # PaymentGatewayService,
        PaymentService,
        PaymentRepository
    ]
)
class PaymentModule:
    pass