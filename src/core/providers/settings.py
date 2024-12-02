from functools import lru_cache
from nest.core import Injectable

@Injectable()
class Settings():
    SECRET_KEY: str = "sua_chave_secreta_aqui"  # Altere para uma chave segura em produção
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()