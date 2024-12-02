from nest.core import Injectable
from typing import List, Optional
from abc import abstractmethod
from src.core.models.cart_model import Cart
from cakecup_back_app.src.core.providers.async_orm_provider import AsyncOrmProvider
from uuid import UUID

@Injectable()
class CartRepository():
    def __init__(self, orm_provider: AsyncOrmProvider):
        self.orm_provider = orm_provider
        print("UserRepository inicializado com ORM provider")

    @abstractmethod
    def create_cart(self, cart: Cart) -> Cart:
        pass
    
    @abstractmethod
    def get_cart_by_id(self, cart_id: UUID) -> Optional[Cart]:
        pass
    
    @abstractmethod
    def add_item(self, cart_id: UUID, item: dict) -> Cart:
        pass
    
    @abstractmethod
    def remove_item(self, cart_id: UUID, item_id: UUID) -> bool:
        pass
    
    @abstractmethod
    def update_item_quantity(self, cart_id: UUID, item_id: UUID, quantity: int) -> Cart:
        pass
    
    @abstractmethod
    def get_cart_by_user_id(self, user_id: UUID) -> Optional[Cart]:
        pass
    
    @abstractmethod
    def clear_cart(self, cart_id: UUID) -> bool:
        pass
