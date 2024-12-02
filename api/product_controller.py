from nest.core import Controller, Get, Post, Put, Delete, Depends
from typing import List, Optional
from src.core.models.product_model import Product, ProductCreate, ProductUpdate
from src.modules.product.services.product_service import ProductService
from src.core.providers.response_handler import ResponseHandler, ApiResponse
from uuid import UUID
from src.core.models.user_model import User
from src.modules.user.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer
from src.core.decorators.validation import enable_cors

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@Controller("/products", tag=["Cupcakes"])
class ProductController:
    def __init__(self, service: ProductService, auth_service: AuthService, response_handler: ResponseHandler):
        self.service = service
        self.auth_service = auth_service
        self.response_handler = response_handler

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        return await self.auth_service.get_current_user(token)

    @Post(response_model=ApiResponse[Product])
    async def create_product(
        self,
        product: ProductCreate,
        token: str = Depends(oauth2_scheme)
    ) -> ApiResponse[Product]:
        try:
            current_user = await self.auth_service.get_current_user(token)
            created = await self.service.create_product(product, UUID(current_user.id))
            return self.response_handler.wrap_response(
                data=created,
                message="Cupcake criado com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao criar cupcake",
                errors=str(e)
            )
    @Get()
    async def find_products(
        self, 
        is_active: Optional[bool] = True,
        is_gluten_free: Optional[bool] = None,
        is_lactose_free: Optional[bool] = None,
        is_vegan: Optional[bool] = None,
        flavor: Optional[str] = None,
        size: Optional[str] = None
    ) -> ApiResponse[List[Product]]:
        try:
            filters = {
                "is_active": is_active,
                "is_gluten_free": is_gluten_free,
                "is_lactose_free": is_lactose_free,
                "is_vegan": is_vegan,
                "flavor": flavor,
                "size": size
            }
            # Remove None values
            filters = {k: v for k, v in filters.items() if v is not None}
            
            products = await self.service.find_products(filters)
            return self.response_handler.wrap_response(
                data=products,
                message="Cupcakes recuperados com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao buscar cupcakes",
                errors=str(e)
            )

    @Get("/{product_id}")
    async def find_product(self, product_id: UUID) -> ApiResponse[Product]:
        try:
            product = await self.service.find_product(product_id)
            return self.response_handler.wrap_response(
                data=product,
                message="Cupcake encontrado com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao buscar cupcake",
                errors=str(e)
            )

    @Put("/{product_id}")
    async def update_product(self, product_id: UUID, product: ProductUpdate) -> ApiResponse[Product]:
        try:
            updated = await self.service.update_product(product_id, product)
            return self.response_handler.wrap_response(
                data=updated,
                message="Cupcake atualizado com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao atualizar cupcake",
                errors=str(e)
            )

    @Delete("/{product_id}")
    async def delete_product(self, product_id: UUID) -> ApiResponse[bool]:
        try:
            result = await self.service.delete_product(product_id)
            return self.response_handler.wrap_response(
                data=result,
                message="Cupcake removido com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao remover cupcake",
                errors=str(e)
            )

