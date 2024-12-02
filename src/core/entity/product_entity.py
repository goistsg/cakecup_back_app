from sqlalchemy import Column, String, Numeric, Integer, Boolean, Text, ARRAY
from sqlalchemy.orm import relationship
from .base import BaseModel
from .review_entity import ReviewEntity

class ProductEntity(BaseModel):
    __tablename__ = 'products'

    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    sku = Column(String(100), unique=True)
    is_active = Column(Boolean, default=True)
    image_url = Column(Text)
    
    # Campos específicos para cupcakes
    flavor = Column(String(100), nullable=False)
    frosting_type = Column(String(100))
    decoration_description = Column(Text)
    is_gluten_free = Column(Boolean, default=False)
    is_lactose_free = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    allergens = Column(ARRAY(String))
    ingredients = Column(Text, nullable=False)
    size = Column(String(20), default='regular')
    calories = Column(Integer)

    reviews = relationship(ReviewEntity, back_populates='product')
