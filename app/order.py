from pydantic import BaseModel, Field


class Order(BaseModel):
    cart_value: int = Field(..., ge=0)
    delivery_distance: int = Field(..., ge=0)
    number_of_items: int = Field(..., ge=0)
    time: str
