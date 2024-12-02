from nest.core import Injectable
from sqlalchemy import select, update
from src.core.providers.async_orm_provider import AsyncOrmProvider
from src.core.entity.payment_entity import PaymentEntity, PaymentStatus
from typing import Optional, List
from uuid import UUID
from datetime import datetime

@Injectable()
class PaymentRepository:
    def __init__(self, orm_provider: AsyncOrmProvider):
        self.orm_provider = orm_provider

    async def create_payment(self, payment_data: dict) -> PaymentEntity:
        try:
            async with await self.orm_provider.get_session() as session:
                payment = PaymentEntity(**payment_data)
                session.add(payment)
                await session.commit()
                await session.refresh(payment)
                return payment
        except Exception as e:
            print(f"Erro ao criar pagamento: {str(e)}")
            raise e

    async def get_payment_by_id(self, payment_id: UUID) -> Optional[PaymentEntity]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(PaymentEntity).where(PaymentEntity.id == payment_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except Exception as e:
            print(f"Erro ao buscar pagamento: {str(e)}")
            raise e

    async def get_payment_by_order_id(self, order_id: UUID) -> Optional[PaymentEntity]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(PaymentEntity).where(PaymentEntity.order_id == order_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except Exception as e:
            print(f"Erro ao buscar pagamento pelo pedido: {str(e)}")
            raise e

    async def update_payment_status(
        self, 
        payment_id: UUID, 
        status: PaymentStatus,
        payment_details: dict = None
    ) -> Optional[PaymentEntity]:
        try:
            async with await self.orm_provider.get_session() as session:
                update_data = {
                    "status": status,
                    "updated_at": datetime.utcnow()
                }
                
                if payment_details:
                    update_data["payment_details"] = payment_details

                query = (
                    update(PaymentEntity)
                    .where(PaymentEntity.id == payment_id)
                    .values(**update_data)
                    .returning(PaymentEntity)
                )
                
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one()
        except Exception as e:
            print(f"Erro ao atualizar status do pagamento: {str(e)}")
            raise e

    async def get_payments_by_user_id(self, user_id: UUID) -> List[PaymentEntity]:
        try:
            async with await self.orm_provider.get_session() as session:
                # Aqui fazemos um join com orders para pegar os pagamentos do usuário
                query = (
                    select(PaymentEntity)
                    .join(PaymentEntity.order)
                    .where(PaymentEntity.order.has(user_id=user_id))
                )
                result = await session.execute(query)
                return result.scalars().all()
        except Exception as e:
            print(f"Erro ao buscar pagamentos do usuário: {str(e)}")
            raise e

    async def get_pending_payments(self) -> List[PaymentEntity]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(PaymentEntity).where(
                    PaymentEntity.status == PaymentStatus.PENDING
                )
                result = await session.execute(query)
                return result.scalars().all()
        except Exception as e:
            print(f"Erro ao buscar pagamentos pendentes: {str(e)}")
            raise e