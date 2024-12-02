from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from nest.core import Injectable
from typing import Callable, List, Union

@Injectable()
class CorsMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        allow_origins: Union[List[str], str] = "*",
        allow_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers: List[str] = ["Content-Type", "Authorization", "X-Requested-With"],
        allow_credentials: bool = True
    ):
        super().__init__(app)
        self.allow_origins = allow_origins
        self.allow_methods = ", ".join(allow_methods)
        self.allow_headers = ", ".join(allow_headers)
        self.allow_credentials = "true" if allow_credentials else "false"

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Se for uma requisição OPTIONS (preflight), retorna resposta imediatamente
        if request.method == "OPTIONS":
            return Response(
                status_code=200,
                headers={
                    "Access-Control-Allow-Origin": "*" if self.allow_origins == "*" else ", ".join(self.allow_origins),
                    "Access-Control-Allow-Credentials": self.allow_credentials,
                    "Access-Control-Allow-Methods": self.allow_methods,
                    "Access-Control-Allow-Headers": self.allow_headers,
                }
            )

        # Processa a requisição normalmente
        response = await call_next(request)

        # Adiciona os headers CORS à resposta
        response.headers["Access-Control-Allow-Origin"] = "*" if self.allow_origins == "*" else ", ".join(self.allow_origins)
        response.headers["Access-Control-Allow-Credentials"] = self.allow_credentials
        response.headers["Access-Control-Allow-Methods"] = self.allow_methods
        response.headers["Access-Control-Allow-Headers"] = self.allow_headers

        return response
