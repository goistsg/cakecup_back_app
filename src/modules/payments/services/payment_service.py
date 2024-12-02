from nest.core import Injectable
from src.modules.payments.repositories.payment_repository import PaymentRepository
from src.core.dto.payment_dto import CreatePaymentDTO, PaymentResponseDTO
from src.core.entity.payment_entity import PaymentStatus
from uuid import UUID

@Injectable()
class PaymentService:
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    async def create_payment(self, data: CreatePaymentDTO) -> PaymentResponseDTO:
        payment = await self.payment_repository.create_payment(data.dict())
        return PaymentResponseDTO.from_orm(payment)

    async def process_payment(self, payment_id: UUID) -> PaymentResponseDTO:
        # Aqui você implementaria a lógica de processamento
        # Por enquanto, apenas atualizamos o status
        payment = await self.payment_repository.update_payment_status(
            payment_id,
            PaymentStatus.APPROVED
        )
        return PaymentResponseDTO.from_orm(payment) 