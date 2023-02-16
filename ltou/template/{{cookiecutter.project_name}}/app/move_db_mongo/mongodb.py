from motor.motor_asyncio import AsyncIOMotorClient


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


# dependencies for fastapi
async def get_database() -> AsyncIOMotorClient:
    return db.client
