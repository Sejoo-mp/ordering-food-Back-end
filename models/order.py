from beanie import Document
from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class OrderItem(BaseModel):
    menu_item_id: int
    quantity: int
    price: float

class Order(Document):
    id: int
    user_id: int
    items: List[OrderItem]
    total_price: float
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "orders"
        use_state_management = True