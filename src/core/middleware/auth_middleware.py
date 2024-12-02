from nest.core import Injectable
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from src.modules.user.services.auth_service import AuthService
from typing import Callable, Awaitable

@Injectable()
class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def before(self, request: Request) -> None:
        # Ignora rotas públicas
        if self._is_public_route(request.url.path):
            return

        try:
            # Obtém o token do header
            authorization: str = request.headers.get("Authorization")
            print(f"Authorization header: {authorization}")  # Debug

            if not authorization or not authorization.startswith("Bearer "):
                raise HTTPException(
                    status_code=401,
                    detail="Token não fornecido",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            token = authorization.replace("Bearer ", "")
            
            # Valida o token e obtém o usuário
            user = await self.auth_service.get_current_user(token)
            print(f"User from auth service: {user}")  # Debug
            
            # Adiciona o usuário ao request state
            request.state.user = user
            print(f"User added to state: {request.state.user}")  # Debug

        except Exception as e:
            print(f"Error in middleware: {str(e)}")  # Debug
            raise HTTPException(
                status_code=401,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

    def _is_public_route(self, path: str) -> bool:
        public_routes = [
            "/auth/login",
            "/auth/register",
            "/docs",
            "/openapi.json",
            "/redoc"
        ]
        return any(path.startswith(route) for route in public_routes) 