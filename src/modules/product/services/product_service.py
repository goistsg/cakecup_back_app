from uuid import UUID
from nest.core import Injectable
from typing import List, Dict, Any, Optional
from src.core.models.product_model import Product, ProductCreate, ProductUpdate
from src.modules.product.repositories.product_db_repository import ProductDbRepository

@Injectable()
class ProductService:
    def __init__(self, repository: ProductDbRepository):
        self.repository = repository

    async def create_product(self, product: ProductCreate, created_by: UUID) -> Product:
        try:
            return await self.repository.create_product(product, created_by)
        except Exception as e:
            raise Exception(f"Erro ao criar cupcake: {str(e)}")

    async def find_products(self, filters: Dict[str, Any]) -> List[Product]:
        try:
            return await self.repository.find_products(filters)
        except Exception as e:
            raise Exception(f"Erro ao buscar cupcakes: {str(e)}")

    async def find_product(self, product_id: UUID) -> Optional[Product]:
        try:
            product = await self.repository.find_product(product_id)
            if not product:
                raise Exception("Cupcake não encontrado")
            return product
        except Exception as e:
            raise Exception(f"Erro ao buscar cupcake: {str(e)}")

    async def update_product(self, product_id: UUID, product_data: ProductUpdate) -> Product:
        try:
            updated_product = await self.repository.update_product(product_id, product_data)
            if not updated_product:
                raise Exception("Cupcake não encontrado")
            return updated_product
        except Exception as e:
            raise Exception(f"Erro ao atualizar cupcake: {str(e)}")

    async def delete_product(self, product_id: UUID) -> bool:
        try:
            return await self.repository.delete_product(product_id)
        except Exception as e:
            raise Exception(f"Erro ao deletar cupcake: {str(e)}")
