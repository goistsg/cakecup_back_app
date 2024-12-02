from nest.core import Module
from src.modules.user.services.user_service import UserService
from src.modules.user.services.auth_service import AuthService
from src.modules.user.repositories.user_db_repository import UserDbRepository

@Module(
    controllers=[],
    providers=[
        UserService,
        AuthService,
        UserDbRepository
    ]
)
class UserModule:
    pass
