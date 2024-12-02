from src.modules.product.repositories.product_repository import ProductRepository
from src.core.models.product_model import Product
from typing import List, Optional

class ProductMemoryRepository(ProductRepository):
    def __init__(self):
        self.products = []

    def find_products(self) -> List[Product]:
        return self.products

    def find_product_by_id(self, product_id: int) -> Optional[Product]:
        return next((p for p in self.products if p.id == product_id), None)

    def create_product(self, product: Product) -> Product:
        self.products.append(product)
        return product
