import datetime
from collections import OrderedDict
from datetime import timedelta
from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class CachedItem(BaseModel):
    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )
    value: Any


class LRUCache:
    def __init__(self, capacity: int, expiration_time: timedelta):
        self.capacity: int = capacity
        self.expiration_time: timedelta = expiration_time
        self.cache: OrderedDict = OrderedDict()

    def get(self, key) -> Optional[CachedItem]:
        try:
            item = self.cache.pop(key)
            if datetime.utcnow() - item.timestamp > self.expiration_time:
                return None

            self.cache[key] = item
            return item.value
        except KeyError:
            return None

    def set(self, key, value) -> None:
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = CachedItem(value=value)

    def clear(self):
        self.cache.clear()
