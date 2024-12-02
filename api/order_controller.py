from nest.core import Controller, Post, Get, Injectable, Depends
# from nest.core.decorators import UseGuards
# from src.shared.guards import AuthGuard
from src.modules.orders.services.order_service import OrderService
from src.modules.user.services.auth_service import AuthService
from src.core.dto.order_dto import CreateOrderDTO, OrderResponseDTO
from src.core.providers.response_handler import ResponseHandler, ApiResponse
from src.core.models.user_model import User
from typing import List
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# @UseGuards(AuthGuard)
@Controller('orders', tag=["Pedidos"])
class OrderController:
    def __init__(self, order_service: OrderService, auth_service: AuthService, response_handler: ResponseHandler):
        self.order_service = order_service
        self.auth_service = auth_service
        self.response_handler = response_handler

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        return await self.auth_service.get_current_user(token)
    
    @Post("/cart/{cart_id}")
    async def create_order(
        self,
        cart_id: UUID,
        token: str = Depends(oauth2_scheme)
    ) -> ApiResponse[OrderResponseDTO]:
        try:
            current_user = await self.get_current_user(token)
            order = await self.order_service.create_order(cart_id, UUID(current_user.id))
            return self.response_handler.wrap_response(
                data=order,
                message="Pedido criado com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao criar pedido",
                errors=str(e)
            )

    @Get()
    async def get_user_orders(self, user_id: UUID) -> List[OrderResponseDTO]:
        return await self.order_service.get_user_orders(user_id)

    @Get(':id')
    async def get_order(self, id: UUID) -> OrderResponseDTO:
        return await self.order_service.get_order_by_id(id) 