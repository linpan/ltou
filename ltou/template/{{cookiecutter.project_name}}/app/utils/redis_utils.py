import aioredis
from app.core.config import settings


async def redis_pool():
    """
    :return:
    """
    redis = await aioredis.from_url(settings.REDIS_URL,
                                    max_connections=8,
                                    encoding="utf8",
                                    decode_responses=True)
    return redis


async def shutdown_redis() -> None:  # pragma: no cover
    """
    Closes redis connection pool.
    """
    await redis_pool().disconnect()
