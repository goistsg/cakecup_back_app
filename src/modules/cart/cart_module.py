from nest.core import Module
from src.modules.cart.services.cart_service import CartService
from src.modules.cart.repositories.cart_db_repository import CartDbRepository

@Module(
    controllers=[],
    providers=[
        CartService,
        CartDbRepository
    ]
)
class CartModule:
    pass
