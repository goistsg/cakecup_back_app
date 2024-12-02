from nest.core import Controller, Post
from src.core.models.user_model import UserCreate
from src.core.models.auth_model import LoginRequest
from src.modules.user.services.auth_service import AuthService
from src.core.providers.response_handler import ResponseHandler, ApiResponse

@Controller("/auth", tag=["Autenticação"])
class AuthController:
    def __init__(self, service: AuthService, response_handler: ResponseHandler):
        self.service = service
        self.response_handler = response_handler

    @Post("/login")
    async def login(self, credentials: LoginRequest) -> ApiResponse:
        try:
            token = await self.service.authenticate_user(credentials.email, credentials.password)
            return self.response_handler.wrap_response(
                data=token,
                message="Login realizado com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao realizar login",
                errors=str(e)
            )

    @Post("/register")
    async def register(self, user: UserCreate) -> ApiResponse:
        try:
            print(user)
            created = await self.service.register_user(user)
            print('created')
            print(created)
            return self.response_handler.wrap_response(
                data=created,
                message="Usuário registrado com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao registrar usuário",
                errors=str(e)
            ) 