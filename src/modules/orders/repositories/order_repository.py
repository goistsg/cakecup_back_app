from nest.core import Injectable
from sqlalchemy import select
from src.core.providers.async_orm_provider import AsyncOrmProvider
from src.core.entity.order_entity import OrderEntity
from src.core.entity.enums import OrderStatus
from typing import List, Optional
from uuid import UUID

@Injectable()
class OrderRepository:
    def __init__(self, orm_provider: AsyncOrmProvider):
        self.orm_provider = orm_provider

    async def create_order(self, order_data: dict) -> OrderEntity:
        async with await self.orm_provider.get_session() as session:
            try:
                order = OrderEntity(
                    user_id=order_data["user_id"],
                    items=order_data["items"],
                    total=order_data["total"],
                    cart_id=order_data["cart_id"],
                    created_by=order_data["created_by"],
                    status=OrderStatus.PENDING
                )
                
                session.add(order)
                await session.commit()
                await session.refresh(order)
                
                print(f"Order created: {order.__dict__}")  # Debug
                return order
                
            except Exception as e:
                await session.rollback()
                print(f"Error creating order: {str(e)}")  # Debug
                raise

    async def get_orders_by_user_id(self, user_id: UUID) -> List[OrderEntity]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(OrderEntity).where(OrderEntity.user_id == user_id)
                result = await session.execute(query)
                return result.scalars().all()
        except Exception as e:
            print(f"Erro ao buscar pedidos: {str(e)}")
            raise e 