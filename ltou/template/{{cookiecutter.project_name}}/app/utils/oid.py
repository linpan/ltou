from typing import List, NoReturn

from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from pydantic import BaseModel, BaseConfig
from pymongo.cursor import Cursor

from app.core.config import settings

tz = settings.TIME_ZONE


class PydanticObjectId:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId 🍰")

    @classmethod
    def __modify_schema__(cls, field_schema) -> NoReturn:
        field_schema.update(type="string")


class MongoModel(BaseModel):

    @classmethod
    def from_dict(cls, data: dict) -> "MongoModel":
        """We must convert _id into "id". """
        if not data:
            return data
        id = data.pop('_id', None)
        return cls(**dict(data, id=id))

    def to_mongo(self, **kwargs):
        """ save to mongo"""
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)

        parsed = self.dict(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )
        if "updated_at" in parsed:
            parsed["updated_at"] = datetime.now(tz=tz)

        # Mongo uses `_id` as default key. We should stick to that as well.
        if '_id' not in parsed and 'id' in parsed:
            parsed['_id'] = parsed.pop('id')

        return parsed

    @classmethod
    async def iter_to_list(cls, cursor_: Cursor) -> List['MongoModel']:
        docs = []
        async for doc in cursor_:
            _id = doc.pop('_id', None)
            docs.append(cls(**dict(doc, id=_id)))

        return docs

    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }
