from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.user import User
from models.menu import MenuItem
from models.order import Order
from utils.id_generator import set_db_client

async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.food_ordering

    # ست کردن client مشترک برای id_generator
    set_db_client(client, "food_ordering")

    # init کردن counters فقط اگه وجود نداشتن
    counters = db.counters
    for name in ["user_id", "menu_item_id", "order_id"]:
        await counters.update_one(
            {"_id": name},
            {"$setOnInsert": {"seq": 0}},
            upsert=True
        )

    await init_beanie(
        database=db,
        document_models=[User, MenuItem, Order]
    )