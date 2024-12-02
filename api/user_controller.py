from nest.core import Controller, Get, Patch, Delete
from typing import List
from src.core.models.user_model import User, UserUpdate
from src.modules.user.services.user_service import UserService
from src.core.providers.response_handler import ResponseHandler, ApiResponse
from uuid import UUID

@Controller("/users", tag=["Usuários"])
class UserController:
    def __init__(self, service: UserService, response_handler: ResponseHandler):
        self.service = service
        self.response_handler = response_handler

    @Get()
    async def find_users(self) -> ApiResponse[List[User]]:
        try:
            users = await self.service.find_users()
            return self.response_handler.wrap_response(
                data=users,
                message="Usuários recuperados com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao buscar usuários",
                errors=str(e)
            )

    @Get("/{user_id}")
    async def find_user(self, user_id: UUID) -> ApiResponse[User]:
        try:
            user = await self.service.find_user(user_id)
            return self.response_handler.wrap_response(
                data=user,
                message="Usuário encontrado com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao buscar usuário",
                errors=str(e)
            )

    @Patch("/{user_id}")
    async def update_user(self, user_id: UUID, user: UserUpdate) -> ApiResponse[User]:
        try:
            updated = await self.service.update_user(user_id, user)
            return self.response_handler.wrap_response(
                data=updated,
                message="Usuário atualizado com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao atualizar usuário",
                errors=str(e)
            )

    @Delete("/{user_id}")
    async def delete_user(self, user_id: UUID) -> ApiResponse[bool]:
        try:
            result = await self.service.delete_user(user_id)
            return self.response_handler.wrap_response(
                data=result,
                message="Usuário removido com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao remover usuário",
                errors=str(e)
            )
