import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def clear_database():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.food_ordering

    collections = await db.list_collection_names()
    
    for collection in collections:
        await db[collection].drop()
        print(f"✅ Collection '{collection}' dropped")

    print("\n🗑️ Database cleared successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(clear_database())