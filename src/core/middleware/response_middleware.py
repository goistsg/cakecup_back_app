from nest.core import Injectable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response
from typing import Any
from ..models.api_response import ApiResponse, StatusEnum

@Injectable()
class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Any) -> Any:
        response = await call_next(request)
        
        # Se for uma requisição OPTIONS, retorna a resposta como está
        if request.method == "OPTIONS":
            return response

        # Se já for uma JSONResponse, retorna como está
        if isinstance(response, JSONResponse):
            return response

        # Converte a resposta para nosso formato padrão
        if hasattr(response, 'body'):
            try:
                # Tenta converter o corpo da resposta para dict
                from json import loads
                data = loads(response.body)
            except:
                data = response.body

            api_response = ApiResponse(
                data=data,
                message="Operação realizada com sucesso",
                status=StatusEnum.SUCCESS if response.status_code < 400 else StatusEnum.ERROR
            )

            return JSONResponse(
                content=api_response.dict(),
                status_code=response.status_code
            )

        # Se for qualquer outro tipo de resposta
        return JSONResponse(
            content=ApiResponse(
                data=response,
                message="Operação realizada com sucesso",
                status=StatusEnum.SUCCESS
            ).dict()
        ) 