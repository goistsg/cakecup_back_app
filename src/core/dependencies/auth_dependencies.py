from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.modules.user.services.auth_service import AuthService
from src.core.models.user_model import User
from typing import Annotated
from nest.core import Injectable

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends()]
) -> User:
    try:
        return await auth_service.get_current_user(token)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Não foi possível autenticar",
            headers={"WWW-Authenticate": "Bearer"},
        )
