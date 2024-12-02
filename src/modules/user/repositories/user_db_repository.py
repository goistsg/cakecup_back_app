from typing import List, Optional
from sqlalchemy import select
from src.core.providers.async_orm_provider import AsyncOrmProvider
from src.core.models.user_model import User, UserCreate, UserUpdate
from src.core.entity.user_entity import UserEntity
from nest.core import Injectable
from uuid import UUID

@Injectable()
class UserDbRepository:
    def __init__(self, orm_provider: AsyncOrmProvider):
        self.orm_provider = orm_provider

    async def create_user(self, user: UserCreate, password_hash: str) -> User:
        try:
            async with await self.orm_provider.get_session() as session:
                user_entity = UserEntity(
                    name=user.name,
                    email=user.email,
                    is_active=user.is_active,
                    role=user.role,
                    password_hash=password_hash
                )
                session.add(user_entity)
                await session.commit()
                await session.refresh(user_entity)
                
                return User.from_entity(user_entity)
                
        except Exception as e:
            print(f"Erro ao criar usuário: {str(e)}")
            raise e
    
    async def get_users(self) -> List[User]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(UserEntity)
                result = await session.execute(query)
                return [User.from_entity(user) for user in result.scalars().all()]
        except Exception as e:
            print(f"Erro ao buscar usuários: {str(e)}")
            return []
        
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(UserEntity).filter_by(id=user_id)
                result = await session.execute(query)
                return User.from_entity(result.scalars().first())
        except Exception as e:
            print(f"Erro ao buscar usuário: {str(e)}")
            raise e
        
    async def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(UserEntity).filter_by(email=email)
                result = await session.execute(query)
                user = result.scalars().first()
                
                if user:
                    await session.refresh(user)
                
                return user
        except Exception as e:
            print(f"Erro ao buscar usuário: {str(e)}")
            return None
        
    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(UserEntity).filter_by(id=user_id)
                result = await session.execute(query)
                user_entity = result.scalars().first()
                if user_entity:
                    for key, value in user_data.dict().items():
                        if value is not None:
                            setattr(user_entity, key, value)
                    await session.commit()
                    await session.refresh(user_entity)
                    return User.from_entity(user_entity)
                return None
        except Exception as e:
            print(f"Erro ao atualizar usuário: {str(e)}")
            raise e

    async def delete_user(self, user_id: UUID) -> bool:
        try:
            async with await self.orm_provider.get_session() as session:
                query = select(UserEntity).filter_by(id=user_id)
                result = await session.execute(query)
                user_entity = result.scalars().first()
                if user_entity:
                    await session.delete(user_entity)
                    await session.commit()
                    return True
                return False    
        except Exception as e:
            print(f"Erro ao deletar usuário: {str(e)}")
            raise e 
