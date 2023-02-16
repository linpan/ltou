import datetime
from pathlib import Path
from typing import Optional
import pytz
from pydantic import BaseSettings, HttpUrl, validator,ValidationError

{%- if cookiecutter.db_info.name == "mongodb" %},MongoDsn {%- endif %}
{%- if cookiecutter.db_info.name == "postgresql" %},PostgresDsn {%- endif %}
{%- if cookiecutter.enable_redis == "True" %}, RedisDsn {%- endif %}
{%- if cookiecutter.enable_kafka == "True" %}, KafkaDsn {%- endif %}
{%- if cookiecutter.enable_rmq == "True" %}, AmqpDsn {%- endif %}

from pytz.exceptions import UnknownTimeZoneError


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    PROJECT_DIR: Path = Path(__file__).parent.parent.parent
    PROJECT_NAME: str = "{{cookiecutter.project_name}}"

    ENVIRONMENT: str = "dev"
    project_version: str = "0.1"

    USE_CORRELATION_ID: bool = True

    TIME_ZONE: datetime.tzinfo = pytz.timezone("UTC")

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "logs/{{cookiecutter.project_name}}.log"

    {%- if cookiecutter.db_info.name == "postgresql" %}
    # postgres database
    POSTGRES_URL: PostgresDsn = "postgresql+asyncpg://hiro:rcts2020@localhost:5432/mock"
    {%- endif %}

    {%- if cookiecutter.db_info.name == "mongodb" %}
    # MONGODB Database
    MONGODB_URI: MongoDsn = "mongodb://localhost:27017/"
    MONGODB_DB_NAME: str = "dev"
    {%- endif %}

    {%- if cookiecutter.db_info.name == "sqlite" %}
    # SQlite Database SQLITE_SYNC_URL_PREFIX or SQLITE_SYNC_URL_PREFIX
    SQlite_URI: str = "sqlite+aiosqlite:///db.sqlite3:?mode=memory&cache=shared&uri=true"
    {%- endif %}

    {%- if cookiecutter.db_info.name == "mysql" %}
    # MySQL Database
    MYSQL_URI: str = "mysql://username:password@server/db"
    {%- endif %}

    {%- if cookiecutter.enable_redis == "True" %}
    # Redis Database
    REDIS_URL: RedisDsn = "redis://localhost:6379/0"
    {%- endif %}

    {% if cookiecutter.enable_kafka == "True" %}
    # Kafka Database
    KAFKA_BROKER: KafkaDsn = "kafka://localhost:9092"
    {%- endif %}
    {%- if cookiecutter.enable_rmq == "True" %}
    # RabbitMQ Queue
    RABBIT_URI: AmqpDsn = "amqp://guest:guest@rabbitmq:5672//"
    {%- endif %}

    {%- if cookiecutter.enable_sentry == "True" %}
    # warning in production must be disabled
    # Sentry
    SENTRY_DSN: Optional[HttpUrl] = None
    {%- endif %}

    REDOC_URL: Optional[str] = "/redoc" if DEBUG else None
    DOCS_URL: Optional[str] = "/docs"  if DEBUG else None

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    SECRET_KEY: str = "hidden secret key"

    @validator("TIME_ZONE", always=True)
    def valid_timezone(cls, v):
        try:
            if isinstance(v, str):
                return pytz.timezone(v)
        except (ValueError, ValidationError, UnknownTimeZoneError):
            return pytz.timezone("UTC")


    class Config:
            env_file = f".env"
            # Place your .env file under this path
            # env_file = "short/.env"
            env_prefix = "dev_"


settings = Settings()

