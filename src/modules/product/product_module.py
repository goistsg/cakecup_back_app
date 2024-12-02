from nest.core import Module
from src.modules.product.services.product_service import ProductService
from src.modules.product.repositories.product_db_repository import ProductDbRepository

@Module(
    controllers=[],
    providers=[
        ProductService,
        ProductDbRepository
    ]
)
class ProductModule:
    pass
