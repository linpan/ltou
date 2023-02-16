import pytest
from typing import AsyncGenerator

from httpx import AsyncClient
from app.main import app as fastapi_app


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://localhost:8005") as ac:
        yield ac
