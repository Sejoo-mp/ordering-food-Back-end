from pydantic import BaseModel
from typing import List
from models.order import OrderStatus

class OrderItemRequest(BaseModel):
    menu_item_id: int
    quantity: int

class CreateOrderSchema(BaseModel):
    items: List[OrderItemRequest]

class StatusSchema(BaseModel):
    status: OrderStatus