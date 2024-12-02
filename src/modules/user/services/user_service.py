from nest.core import Injectable
from typing import Optional, List
from uuid import UUID
from fastapi import HTTPException
from src.modules.user.repositories.user_db_repository import UserDbRepository
from src.core.models.user_model import User, UserCreate, UserUpdate
from src.core.providers.security import get_password_hash
from pydantic import EmailStr

@Injectable()
class UserService:
    def __init__(self, repository: UserDbRepository):
        self.repository = repository

    async def create_user(self, user_data: UserCreate) -> User:
        try:
            existing_user = await self.repository.get_user_by_email(user_data.email)
            if existing_user is not None:
                raise HTTPException(status_code=400, detail="Email já cadastrado")

            password_hash = get_password_hash(user_data.password)

            user_entity = await self.repository.create_user(user_data, password_hash)
            return User.from_entity(user_entity)
        except Exception as e:
            print(f"Erro detalhado: {str(e)}")  # Debug
            raise HTTPException(status_code=400, detail=f"Erro ao criar usuário: {str(e)}")
        
    async def find_users(self) -> List[User]:
        users_entity = await self.repository.get_users()
        return [User.from_entity(user) for user in users_entity]

    async def find_user(self, user_id: UUID) -> Optional[User]:
        user_entity = await self.repository.get_user_by_id(user_id)
        if not user_entity:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return User.from_entity(user_entity)

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> User:
        try:
            if user_data.password:
                user_data.password = get_password_hash(user_data.password)

            user_entity = await self.repository.update_user(user_id, user_data)
            if not user_entity:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            return User.from_entity(user_entity)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao atualizar usuário: {str(e)}") 
        
    async def delete_user(self, user_id: UUID) -> bool:
        return await self.repository.delete_user(user_id)
    
    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        user_entity = await self.repository.get_user_by_email(email)
        if not user_entity:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return User.from_entity(user_entity)
    
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        user_entity = await self.repository.get_user_by_id(user_id)
        if not user_entity:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return User.from_entity(user_entity)
