from functools import wraps
from typing import Type, Optional, Any, List, Union
from pydantic import BaseModel, ValidationError
from fastapi import HTTPException, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse

security = HTTPBearer()

def validate_request_body(model: Type[BaseModel]):
    """
    Decorator para validar o corpo da requisição usando um modelo Pydantic
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                if 'request_body' in kwargs:
                    validated_data = model(**kwargs['request_body'])
                    kwargs['request_body'] = validated_data
                return await func(*args, **kwargs)
            except ValidationError as e:
                raise HTTPException(
                    status_code=422,
                    detail=e.errors()
                )
        return wrapper
    return decorator

def require_auth(func):
    """
    Decorator para verificar autenticação
    """
    @wraps(func)
    async def wrapper(*args, token: HTTPAuthorizationCredentials = Depends(security), **kwargs):
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Não autorizado"
            )
        # Aqui você pode adicionar sua lógica de verificação do token
        return await func(*args, **kwargs)
    return wrapper

def has_permission(permission: str):
    """
    Decorator para verificar permissões do usuário
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, token: HTTPAuthorizationCredentials = Depends(security), **kwargs):
            # Aqui você pode adicionar sua lógica de verificação de permissões
            # Por exemplo, decodificar o token e verificar as permissões do usuário
            return await func(*args, **kwargs)
        return wrapper
    return decorator

class CurrentUser:
    """
    Dependency para obter o usuário atual
    """
    def __init__(self, token: HTTPAuthorizationCredentials = Depends(security)):
        self.token = token

    async def __call__(self) -> Optional[Any]:
        # Aqui você pode implementar a lógica para obter o usuário atual
        # Por exemplo, decodificar o token e buscar o usuário no banco
        pass

def enable_cors(
    origins: Union[List[str], str] = "*",
    methods: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
):
    """
    Decorator para adicionar headers CORS às respostas
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            response = await func(*args, **kwargs)
            
            # Prepara os headers CORS
            cors_headers = {
                "Access-Control-Allow-Origin": origins if isinstance(origins, str) else ", ".join(origins),
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": ", ".join(methods),
                "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With"
            }
            
            # Se já for uma Response do FastAPI
            if isinstance(response, Response):
                for key, value in cors_headers.items():
                    response.headers[key] = value
                return response
                
            # Se for um dict ou outro objeto, converte para JSONResponse
            return JSONResponse(
                content=response if isinstance(response, dict) else response.dict(),
                headers=cors_headers
            )
        return wrapper
    return decorator

# Exemplo de uso combinado dos decorators
def secure_endpoint(
    request_model: Optional[Type[BaseModel]] = None,
    permission: Optional[str] = None,
    cors_origins: Union[List[str], str] = "*"
):
    """
    Decorator composto que combina validação, autenticação e CORS
    """
    def decorator(func):
        @wraps(func)
        @enable_cors(origins=cors_origins)
        @require_auth
        @validate_request_body(request_model) if request_model else lambda x: x
        @has_permission(permission) if permission else lambda x: x
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator 