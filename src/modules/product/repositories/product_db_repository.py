from typing import List, Optional, Dict, Any
from sqlalchemy import select
from src.core.providers.async_orm_provider import AsyncOrmProvider
from src.core.models.product_model import Product, ProductCreate, ProductUpdate
from src.core.entity.product_entity import ProductEntity
from nest.core import Injectable
from uuid import UUID

@Injectable()
class ProductDbRepository:
    def __init__(self, orm_provider: AsyncOrmProvider):
        self.orm_provider = orm_provider

    async def create_product(self, product: ProductCreate, created_by: UUID) -> Product:
        try:
            async with await self.orm_provider.get_session() as session:
                product_entity = ProductEntity(
                    **product.dict(),
                    created_by=created_by
                )
                
                session.add(product_entity)
                await session.commit()
                await session.refresh(product_entity)
                
                return Product.from_entity(product_entity)
                
        except Exception as e:
            print(f"Erro ao criar produto: {str(e)}")
            raise e

    async def find_products(self, filters: Dict[str, Any]) -> List[Product]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(ProductEntity).filter_by(**filters)
                result = await session.execute(query)
                return [Product.from_entity(entity) for entity in result.scalars().all()]
        except Exception as e:
            print(f"Erro ao buscar produtos: {str(e)}")
            raise e

    async def find_product(self, product_id: UUID) -> Optional[Product]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(ProductEntity).filter_by(id=product_id)
                result = await session.execute(query)
                return Product.from_entity(result.scalars().first())
        except Exception as e:
            print(f"Erro ao buscar produto: {str(e)}")
            raise e

    async def update_product(self, product_id: UUID, product_data: ProductUpdate) -> Optional[Product]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(ProductEntity).filter_by(id=product_id)
                result = await session.execute(query)
                product_entity = result.scalars().first()
                if product_entity:
                    product_entity.update(**product_data.model_dump())
                    await session.commit()
                    await session.refresh(product_entity)
                    return Product.from_entity(product_entity)
                return None
        except Exception as e:
            print(f"Erro ao atualizar produto: {str(e)}")
            raise e
        
    async def delete_product(self, product_id: UUID) -> bool:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(ProductEntity).filter_by(id=product_id)
                result = await session.execute(query)
                product_entity = result.scalars().first()
                if product_entity:
                    await session.delete(product_entity)
                    await session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Erro ao deletar produto: {str(e)}")
            raise e
