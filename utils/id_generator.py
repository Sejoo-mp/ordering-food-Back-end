from motor.motor_asyncio import AsyncIOMotorClient

_client = None
_db = None

def set_db_client(client: AsyncIOMotorClient, db_name: str):
    global _client, _db
    _client = client
    _db = client[db_name]

async def get_next_id(collection_name: str) -> int:
    result = await _db.counters.find_one_and_update(
        {"_id": collection_name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    return result["seq"]