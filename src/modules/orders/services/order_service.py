from nest.core import Injectable
from src.modules.orders.repositories.order_repository import OrderRepository
from src.core.dto.order_dto import OrderResponseDTO
from src.modules.cart.services.cart_service import CartService
from src.modules.payments.services.payment_service import PaymentService
from typing import List
from uuid import UUID
from fastapi import HTTPException

@Injectable()
class OrderService:
    def __init__(
        self, 
        order_repository: OrderRepository,
        cart_service: CartService,
        payment_service: PaymentService
    ):
        self.order_repository = order_repository
        self.cart_service = cart_service
        self.payment_service = payment_service

    async def create_order(self, cart_id: UUID, user_id: UUID) -> OrderResponseDTO:
        try:
            # Buscar carrinho
            cart = await self.cart_service.get_active_cart(user_id)
            if not cart:
                raise HTTPException(status_code=404, detail="Carrinho não encontrado")
            
            if cart.id != cart_id:
                raise HTTPException(status_code=404, detail="Carrinho não está de acordo com o ID informado")

            if not cart.items:
                raise HTTPException(status_code=400, detail="Carrinho está vazio")

            print(f"Carrinho: {cart}")

            order = await self.order_repository.create_order({
                "user_id": user_id,
                "cart_id": cart.id,
                "items": cart.items,
                "total": cart.total,
                "created_by": user_id
            })

            # Fechar o carrinho
            await self.cart_service.close_cart(cart.id)

            print(f"Pedido criado: {order}")
            print(f"User ID: {user_id}")
            print(f"Cart ID: {cart_id}")

            return order

        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Erro ao criar pedido: {str(e)}"
            )

    async def get_user_orders(self, user_id: UUID) -> List[OrderResponseDTO]:
        return await self.order_repository.get_orders_by_user_id(user_id)

    async def get_order_by_id(self, order_id: UUID) -> OrderResponseDTO:
        return await self.order_repository.get_order_by_id(order_id) 