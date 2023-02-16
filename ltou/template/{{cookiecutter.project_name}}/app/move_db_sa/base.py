from sqlalchemy import Column, DateTime, func
from sqlalchemy import Column, Integer, UUID, text, BigInteger
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from app.core.config import settings

from sqlalchemy import MetaData
tz = settings.TIME_ZONE

NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=NAMING_CONVENTION, {%- if cookiecutter.db_info.name == "postgresql" %} schema="default" {%- endif %} )


@as_declarative(metadata=metadata)
class Base:
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # id = Column(Integer, primary_key=True)
    # id = Column(BigInteger, primary_key=True)
    id = Column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    # public uuid in url instead of id( Integer)
    # from sqlalchemy.dialects.postgresql import UUID, INT4RANGE, NUMRANGE, JSON
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False,server_default=text("gen_random_uuid()"))
