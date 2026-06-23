from pydantic import BaseModel

class MenuCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    is_available: bool = True

class MenuUpdate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    is_available: bool