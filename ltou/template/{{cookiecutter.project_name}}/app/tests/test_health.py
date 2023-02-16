import pytest

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.anyio


async def test_health(client):
    """
    Test health endpoint.
    """
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"messaged": "odk"}