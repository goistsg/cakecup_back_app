from nest.core import Injectable
from typing import List, Optional
from abc import abstractmethod
from src.core.models.user_model import User
from cakecup_back_app.src.core.providers.async_orm_provider import AsyncOrmProvider
from uuid import UUID

@Injectable()
class UserRepository():
    def __init__(self, orm_provider: AsyncOrmProvider):
        self.orm_provider = orm_provider
        print("UserRepository inicializado com ORM provider")

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_users(self) -> List[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def update_user(self, user: User) -> Optional[User]:
        pass
