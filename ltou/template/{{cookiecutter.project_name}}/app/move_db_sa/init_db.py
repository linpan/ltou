import asyncio
from sqlalchemy import MetaData

from app.db.base import Base
# fixme import register model here, your class must  import in models.__init__.py file
from app import models
from app.db.session import async_engine


async def async_main():
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    asyncio.run(async_main())
