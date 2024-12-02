from nest.core import Controller, Get, Patch, Delete, Post, Depends
from typing import List, Dict
from src.core.models.cart_model import Cart, CartUpdate
from src.modules.cart.services.cart_service import CartService
from src.core.providers.response_handler import ResponseHandler, ApiResponse
from src.core.dependencies.auth_dependencies import get_current_user
from src.core.models.user_model import User
from uuid import UUID
from fastapi import Body
from fastapi.security import OAuth2PasswordBearer
from src.modules.user.services.auth_service import AuthService
from fastapi import Depends, Body
from typing import List
from nest.core import Controller, Get, Post, Delete
from src.core.models.cart_model import Cart
from src.core.dto.cart_dto import AddItemDTO
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@Controller("/carts", tag=["Carrinho"])
class CartController:
    """Controlador para operações do carrinho de compras"""

    def __init__(self, service: CartService, auth_service: AuthService, response_handler: ResponseHandler):
        self.service = service
        self.auth_service = auth_service
        self.response_handler = response_handler

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        return await self.auth_service.get_current_user(token)

    @Get()
    async def get_cart(
        self,
        token: str = Depends(oauth2_scheme)
    ) -> ApiResponse[Cart]:
        """
        Busca o carrinho ativo do usuário
        
        Args:
            token: Token de autenticação
            
        Returns:
            Carrinho ativo do usuário
            
        Raises:
            404: Carrinho não encontrado
            401: Não autorizado
        """
        try:
            current_user = await self.get_current_user(token)
            cart = await self.service.get_active_cart(UUID(current_user.id))
            return self.response_handler.wrap_response(
                data=cart,
                message="Carrinho encontrado com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao buscar carrinho",
                errors=str(e)
            )

    @Post("/{cart_id}/items")
    async def add_item(
        self,
        cart_id: UUID,
        item: AddItemDTO = Body(..., 
            example={
                "product_id": "uuid-do-produto",
                "quantity": 1
            }
        ),
        token: str = Depends(oauth2_scheme)
    ) -> ApiResponse[Cart]:
        """
        Adiciona um item ao carrinho
        
        Args:
            cart_id: ID do carrinho
            item: Dados do item a ser adicionado
            token: Token de autenticação
            
        Returns:
            Carrinho atualizado
            
        Raises:
            404: Carrinho não encontrado
            400: Dados inválidos
            401: Não autorizado
        """
        try:
            current_user = await self.get_current_user(token)
            updated = await self.service.add_item_to_cart(cart_id, item, UUID(current_user.id))
            return self.response_handler.wrap_response(
                data=updated,
                message="Item adicionado ao carrinho com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao adicionar item ao carrinho",
                errors=str(e)
            )

    @Delete("/{cart_id}/product/{product_id}")
    async def remove_item(self, cart_id: UUID, product_id: str, token: str = Depends(oauth2_scheme)) -> ApiResponse[bool]:
        try:
            current_user = await self.get_current_user(token)
            result = await self.service.remove_item_from_cart(cart_id, product_id, UUID(current_user.id))
            return self.response_handler.wrap_response(
                data=result,
                message="Item removido do carrinho com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao remover item do carrinho",
                errors=str(e)
            )
        
    @Patch("/{cart_id}/product/quantity")
    async def update_quantity(
        self,
        cart_id: UUID,
        item_data: Dict = Body(...),
        token: str = Depends(oauth2_scheme)
    ) -> ApiResponse[Cart]:
        try:
            # Extrai os dados do body
            product_id = item_data.get('product_id')
            quantity = item_data.get('quantity')

            # Validações básicas
            if not product_id:
                return self.response_handler.wrap_error(
                    message="ID do produto é obrigatório",
                    errors="product_id não fornecido"
                )
            
            if not quantity or not isinstance(quantity, int) or quantity <= 0:
                return self.response_handler.wrap_error(
                    message="Quantidade inválida",
                    errors="quantity deve ser um número inteiro maior que zero"
                )

            current_user = await self.get_current_user(token)
            updated = await self.service.update_item_quantity(cart_id, product_id, quantity, UUID(current_user.id))
            return self.response_handler.wrap_response(
                data=updated,
                message="Quantidade de item atualizada com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao atualizar quantidade de item",
                errors=str(e)
            )
        
    @Patch("/{cart_id}/clear")
    async def clear_cart(
        self,
        cart_id: UUID,
        token: str = Depends(oauth2_scheme)
    ) -> ApiResponse[Cart]:
        try:
            current_user = await self.get_current_user(token)
            cart = await self.service.clear_cart(cart_id, UUID(current_user.id))
            return self.response_handler.wrap_response(
                data=cart,
                message="Carrinho limpo com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao limpar carrinho",
                errors=str(e)
            )
