from beanie import Document
from datetime import datetime
from typing import Optional

class User(Document):
    id: int
    name: str
    email: str
    password: str
    role: str = "user"
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "users"

    class Config:
        populate_by_name = True