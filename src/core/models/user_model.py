from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import datetime
from src.core.entity.user_entity import UserEntity

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Dict = {'type': 'user'}
    is_active: bool = True

class UserCreate(UserBase):
    password: str
    role: Dict = {'type': 'user'}

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[Dict] = None

class User(UserBase):
    id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    @staticmethod
    def from_entity(entity: 'UserEntity') -> 'User':
        return User(
            id=str(entity.id) if entity.id else None,
            name=entity.name,
            email=entity.email, 
            role=entity.role,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )