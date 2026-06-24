from pydantic import BaseModel
from typing import List

class OrderItemRequest(BaseModel):
    menu_item_id: str
    quantity: int

class CreateOrderSchema(BaseModel):
    items: List[OrderItemRequest]

class StatusSchema(BaseModel):
    status: str