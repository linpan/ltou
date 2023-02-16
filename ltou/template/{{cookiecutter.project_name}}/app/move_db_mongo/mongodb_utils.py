from typing import NoReturn

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.logging import logger
from .mongodb import db


async def connect_to_mongo() -> NoReturn:
    logger.info("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db.database_name = settings.MONGODB_URI
    logger.info("Connected to Mongo...")


async def close_mongo_connection() -> NoReturn:
    logger.info("Closing MongoDB connection...")
    db.client.close()
    logger.info("Closed MongoDB connection...")