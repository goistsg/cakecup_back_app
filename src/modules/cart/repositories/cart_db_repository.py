from typing import List, Optional
from sqlalchemy import select
from src.core.providers.async_orm_provider import AsyncOrmProvider
from src.core.entity.cart_entity import CartEntity
from nest.core import Injectable
from uuid import UUID
from sqlalchemy import update, func

@Injectable()
class CartDbRepository:
    def __init__(self, orm_provider: AsyncOrmProvider):
        self.orm_provider = orm_provider

    async def create_cart(self, cart: CartEntity) -> CartEntity:
        try:
            async with await self.orm_provider.get_session() as session:
                session.add(cart)
                await session.commit()
                await session.refresh(cart)
                return cart
        except Exception as e:
            print(f"Erro ao criar carrinho: {str(e)}")
            raise e
    
    async def update_cart(self, cart_entity: CartEntity) -> CartEntity:
        async with await self.orm_provider.get_session() as session:
            try:
                # Atualiza diretamente usando uma query UPDATE
                query = update(CartEntity).where(
                    CartEntity.id == cart_entity.id
                ).values(
                    items=cart_entity.items,
                    total=cart_entity.total,
                    updated_at=func.now(),
                    status=cart_entity.status
                ).returning(CartEntity)

                result = await session.execute(query)
                await session.commit()
                
                # Busca o carrinho atualizado
                updated_cart = await self.get_cart_by_id(cart_entity.id)
                return updated_cart

            except Exception as e:
                await session.rollback()
                print(f"Erro no update: {str(e)}")  # Debug
                raise e

    async def close_cart(self, cart_entity: CartEntity) -> CartEntity:
        async with await self.orm_provider.get_session() as session:
            try:
                query = update(CartEntity).where(
                    CartEntity.id == cart_entity.id
                ).values(
                    status=cart_entity.status,
                    is_active=cart_entity.is_active
                ).returning(CartEntity)

                result = await session.execute(query)
                await session.commit()
                
                updated_cart = await self.get_cart_by_id(cart_entity.id)
                return updated_cart

            except Exception as e:
                await session.rollback()
                print(f"Erro no update: {str(e)}")  # Debug
                raise e

    async def get_cart_active_and_by_user_id(self, user_id: UUID) -> Optional[CartEntity]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(CartEntity).where(CartEntity.user_id == user_id, CartEntity.is_active == True)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except Exception as e:
            print(f"Erro ao buscar carrinho: {str(e)}")
            raise e
    
    async def get_cart_by_id(self, cart_id: UUID) -> Optional[CartEntity]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(CartEntity).where(CartEntity.id == cart_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except Exception as e:
            print(f"Erro ao buscar carrinho: {str(e)}")
            raise e
        
    async def get_cart_by_id_and_user_id(self, cart_id: UUID, user_id: UUID) -> Optional[CartEntity]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(CartEntity).where(CartEntity.id == cart_id, CartEntity.user_id == user_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except Exception as e:
            print(f"Erro ao buscar carrinho: {str(e)}")
            raise e
    
    async def add_item(self, cart_id: UUID, item: dict, user_id: UUID) -> CartEntity:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(CartEntity).where(CartEntity.id == cart_id, CartEntity.user_id == user_id)
                result = await session.execute(query)
                cart = result.scalar_one_or_none()
                
                if not cart:
                    raise ValueError("Carrinho não encontrado")
                
                cart.items = cart.items or []
                cart.items.append(item)
                cart.total = sum(item.get('price') * item.get('quantity') for item in cart.items)
                
                await session.commit()
                await session.refresh(cart)
                return cart
        except Exception as e:
            print(f"Erro ao adicionar item: {str(e)}")
            raise e
    
    async def remove_item(self, cart_id: UUID, item_id: str) -> bool:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(CartEntity).where(CartEntity.id == cart_id)
                result = await session.execute(query)
                cart = result.scalar_one_or_none()
                if not cart:
                    return False
                
                item = next((item for item in cart.items if item.get('id') == item_id), None)
                cart.items = [item for item in cart.items if item.get('id') != item_id]

                cart.total = min(cart.total, item.price * item.quantity)
                await session.commit()
                return True
        except Exception as e:
            print(f"Erro ao remover item: {str(e)}")
            raise e
    
    async def update_item_quantity(self, cart_id: UUID, item_id: UUID, quantity: int) -> CartEntity:
        try:
            async with await self.orm_provider.get_session() as session:
                cart = await self.get_cart_by_id(cart_id)
                if not cart:
                    raise ValueError("Carrinho não encontrado")
                
                for item in cart.items:
                    if item.get('id') == str(item_id):
                        item['quantity'] = quantity
                        break
                
                await session.commit()
                await session.refresh(cart)
                return cart
        except Exception as e:
            print(f"Erro ao atualizar quantidade: {str(e)}")
            raise e
    
    async def get_cart_by_user_id(self, user_id: UUID) -> Optional[List[CartEntity]]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(CartEntity).where(CartEntity.user_id == user_id)
                result = await session.execute(query)
                return result.scalars().all()
        except Exception as e:
            print(f"Erro ao buscar carrinho do usuário: {str(e)}")
            raise e
    
    async def clear_cart(self, cart_id: UUID) -> bool:
        try:
            async with await self.orm_provider.get_session() as session:
                cart = await self.get_cart_by_id(cart_id)
                if not cart:
                    return False
                
                cart.items = []
                await session.commit()
                return True
        except Exception as e:
            print(f"Erro ao limpar carrinho: {str(e)}")
            raise e