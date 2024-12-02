from nest.core import Injectable
from typing import List, Optional
from abc import abstractmethod
from src.core.models.product_model import Product
from src.core.providers.async_orm_provider import AsyncOrmProvider

@Injectable()
class ProductRepository():
    def __init__(self, orm_provider: AsyncOrmProvider):
        self.orm_provider = orm_provider
        print("ProductRepository inicializado com ORM provider")

    @abstractmethod
    def find_products(self) -> List[Product]:
        pass

    @abstractmethod
    def obter_produto(self, produto_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def create_product(self, produto: Product) -> Product:
        pass

    @abstractmethod
    def delete_product(self, produto: Product) -> Product:
        pass
    
    @abstractmethod
    def update_product(self, produto: Product) -> Product:
        pass
