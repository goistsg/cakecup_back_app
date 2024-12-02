from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from src.core.entity.product_entity import ProductEntity

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    sku: Optional[str] = None
    is_active: bool = True
    image_url: Optional[str] = None
    flavor: str
    frosting_type: Optional[str] = None
    decoration_description: Optional[str] = None
    is_gluten_free: bool = False
    is_lactose_free: bool = False
    is_vegan: bool = False
    allergens: Optional[List[str]] = None
    ingredients: str
    size: str = 'regular'
    calories: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    sku: Optional[str] = None
    is_active: Optional[bool] = None
    image_url: Optional[str] = None
    flavor: Optional[str] = None
    frosting_type: Optional[str] = None
    decoration_description: Optional[str] = None
    is_gluten_free: Optional[bool] = None
    is_lactose_free: Optional[bool] = None
    is_vegan: Optional[bool] = None
    allergens: Optional[List[str]] = None
    ingredients: Optional[str] = None
    size: Optional[str] = None
    calories: Optional[int] = None

class Product(ProductBase):
    id: UUID
    created_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @staticmethod
    def from_entity(entity: 'ProductEntity') -> 'Product':
        return Product(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            price=entity.price,
            stock_quantity=entity.stock_quantity,
            sku=entity.sku,
            is_active=entity.is_active,
            image_url=entity.image_url,
            flavor=entity.flavor,
            frosting_type=entity.frosting_type,
            decoration_description=entity.decoration_description,
            is_gluten_free=entity.is_gluten_free,
            is_lactose_free=entity.is_lactose_free,
            is_vegan=entity.is_vegan,
            allergens=entity.allergens,
            ingredients=entity.ingredients,
            size=entity.size,
            calories=entity.calories,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
