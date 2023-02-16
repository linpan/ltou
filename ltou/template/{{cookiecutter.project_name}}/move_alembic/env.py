import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve())) # noqa
from alembic import context

from logging.config import fileConfig
from app.core.config import settings
{%- if cookiecutter.orm == "sa2" %}
from sqlalchemy import engine_from_config, pool
from app.db.base import Base  # noqa
from app import models
from app.core.config import settings  # noqa
{%- endif %}

{%- if cookiecutter.orm == "sqlmodel" %}
from sqlmodel import SQLModel
{%- endif %}
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

{%- if cookiecutter.orm == "sa2" %}
target_metadata = Base.metadata
{%- else %}
target_metadata = SQLModel.metadata
{%- endif %}
# target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url() -> str:
    {%- if cookiecutter.db_info.name == "sqlite" %}
    return settings.SQlite_URI.replace("+aiosqlite", "")
    {%- elif cookiecutter.db_info.name == "postgresql" %}
    return settings.POSTGRES_URL.replace("+asyncpg", "")
    {%- else %}
    return settings.MYSQL_URI
    {%- endif %}
    returnsettings.POSTGRES_URL.replace("+aiosqlite", "")

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
