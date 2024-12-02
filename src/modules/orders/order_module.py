from nest.core import Module
from src.modules.orders.services.order_service import OrderService
from src.modules.orders.repositories.order_repository import OrderRepository

@Module(
    controllers=[],
    providers=[
        OrderService,
        OrderRepository
    ]
)
class OrderModule:
    pass