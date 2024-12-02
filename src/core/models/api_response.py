from typing import TypeVar, Generic, Optional, List, Union
from pydantic import BaseModel
from enum import Enum

T = TypeVar('T')

class StatusEnum(str, Enum):
    SUCCESS = "success"
    ERROR = "error"

class ApiResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    message: str = "Operação realizada com sucesso"
    errors: List[str] = []
    status: StatusEnum = StatusEnum.SUCCESS

    @classmethod
    def success(cls, data: T, message: str = "Operação realizada com sucesso") -> "ApiResponse[T]":
        return cls(
            data=data,
            message=message,
            status=StatusEnum.SUCCESS
        )

    @classmethod
    def error(cls, message: str, errors: Union[List[str], str] = []) -> "ApiResponse[T]":
        if isinstance(errors, str):
            errors = [errors]
        return cls(
            message=message,
            errors=errors,
            status=StatusEnum.ERROR
        ) 