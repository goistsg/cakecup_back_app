import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from nest.core import Injectable

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

print(f"Database URL configurada: {DATABASE_URL.split('@')[1] if DATABASE_URL else 'None'}")

Base = declarative_base()

SECRET_KEY: str = "sua_chave_secreta_aqui"  # Em produção, use uma chave secreta forte
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

@Injectable()
class AsyncOrmProvider:
    def __init__(self):
        self.engine: AsyncEngine = None
        self.session_factory = None
        self.initialize()
        
    def initialize(self):
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL não está configurada")
            
        print(f"Inicializando conexão com o banco de dados...")
        self.engine = create_async_engine(
            DATABASE_URL,
            echo=False,
            future=True,
            pool_size=5,
            max_overflow=10
        )
        
        self.session_factory = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )
        
        print("AsyncOrmProvider inicializado")

    async def get_session(self) -> AsyncSession:
        if self.session_factory is None:
            raise RuntimeError("AsyncOrmProvider não foi inicializado corretamente")
        return self.session_factory()

