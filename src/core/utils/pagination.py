from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel
from fastapi import Query

T = TypeVar('T')

class PaginationParams(BaseModel):
    page: int = Query(default=1, ge=1, description="Número da página")
    per_page: int = Query(default=10, ge=1, le=100, description="Itens por página")
    
class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool

class FilterParams(BaseModel):
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "asc"
    search: Optional[str] = None
    
    @property
    def sort_direction(self) -> bool:
        return self.sort_order.lower() == "asc"

def paginate(items: List[T], params: PaginationParams) -> PaginatedResponse[T]:
    start = (params.page - 1) * params.per_page
    end = start + params.per_page
    
    total = len(items)
    items_page = items[start:end]
    total_pages = (total + params.per_page - 1) // params.per_page
    
    return PaginatedResponse(
        items=items_page,
        total=total,
        page=params.page,
        per_page=params.per_page,
        pages=total_pages,
        has_next=params.page < total_pages,
        has_prev=params.page > 1
    ) 