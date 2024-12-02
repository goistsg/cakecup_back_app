from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException
from jose import JWTError, jwt
from src.core.providers.security import verify_password
from src.modules.user.repositories.user_db_repository import UserDbRepository
from src.core.models.auth_model import TokenData
from src.core.models.user_model import User, UserCreate
from src.modules.user.services.user_service import UserService
from nest.core import Injectable
from src.core.models.auth_model import TokenResponse

@Injectable()
class AuthService:
    def __init__(self, repository: UserDbRepository, user_service: UserService):
        self.repository = repository
        self.user_service = user_service
        self.SECRET_KEY = "sua_chave_secreta_aqui"  # Altere para uma chave segura em produção
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

    async def authenticate_user(self, email: str, password: str) -> TokenResponse:
        try:
            user_entity = await self.repository.get_user_by_email(email)
            
            if not user_entity:
                return None
            
            if verify_password(password, user_entity.password_hash):
                user = User.from_entity(user_entity)
                access_token = self.create_access_token(
                    data={"sub": str(user.id)},
                    expires_delta=timedelta(minutes=30)
                )
                return TokenResponse(
                    access_token=access_token,
                    token_type="bearer",
                    user=user
                )
            
            return None
        except Exception as e:
            print(f"Erro na autenticação: {str(e)}")
            raise HTTPException(
                status_code=401, 
                detail="Erro na autenticação do usuário"
            )

    def register_user(self, user: UserCreate) -> User:
        return self.user_service.create_user(user)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            token_data = TokenData(user_id=user_id)
        except JWTError:
            raise credentials_exception
            
        user = await self.repository.get_user_by_id(token_data.user_id)
        if user is None:
            raise credentials_exception
            
        return User.from_entity(user)
