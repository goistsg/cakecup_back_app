from nest.core import Injectable
from typing import Any
from ..models.api_response import ApiResponse

@Injectable()
class ResponseHandler:
    def wrap_response(self, data: Any, message: str = "Operação realizada com sucesso") -> ApiResponse:
        return ApiResponse.success(data=data, message=message)

    def wrap_error(self, message: str, errors: Any) -> ApiResponse:
        return ApiResponse.error(message=message, errors=errors) 