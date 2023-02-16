from tortoise import Tortoise
from app.core.config import settings


async def get_db() -> None:
    await Tortoise.init(
        db_url={%- if cookiecutter.db_info.name == "postgresql"%} settings.POSTGRES_URL,{%- elif cookiecutter.db_info.name == "sqlite"%}settings.SQlite_URI, {%- elif cookiecutter.db_info.name == "mysql" %} settings.MYSQL_URL,{%- else %} "sqlite://db.sqlite3",{%- endif %}
        modules={'models': ['app.models']}
    )
