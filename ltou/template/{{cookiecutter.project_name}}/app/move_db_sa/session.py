from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# create asyncio engine
async_engine = create_async_engine(url={%- if cookiecutter.db_info.name == "postgresql"%} settings.POSTGRES_URL{%- elif cookiecutter.db_info.name == "sqlite"%}settings.SQlite_URI {%- elif cookiecutter.db_info.name == "mysql" %} settings.MYSQL_URL{%- else %} "sqlite://db.sqlite3"{%- endif %},
                                   echo=True)

async_session = sessionmaker(
    async_engine, class_=AsyncSession,
)


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
