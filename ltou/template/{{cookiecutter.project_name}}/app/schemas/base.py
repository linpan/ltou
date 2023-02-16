#  username: constr(min_length=3, regex="^[a-zA-Z0-9_-]+$")
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, validator
from app.core.config import settings

tz = settings.TIME_ZONE


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now(tz=tz)
