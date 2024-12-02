from pydantic import BaseModel, UUID4

class AddItemDTO(BaseModel):
    product_id: UUID4
    quantity: int