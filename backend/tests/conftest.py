import os
from uuid import uuid4

import httpx
import pytest

os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "demo-baidget")

from app.main import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture(autouse=True)
async def clear_firestore():
    host = os.environ.get("FIRESTORE_EMULATOR_HOST")
    if host is None:
        yield
        return

    project = os.environ["GOOGLE_CLOUD_PROJECT"]
    url = f"http://{host}/emulator/v1/projects/{project}/databases/(default)/documents"
    async with httpx.AsyncClient() as emulator:
        response = await emulator.delete(url)
        response.raise_for_status()
    yield


@pytest.fixture
async def client(app):
    transport = httpx.ASGITransport(app=app, raise_app_exceptions=False)
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(transport=transport, base_url="http://test") as test_client,
    ):
        yield test_client


async def _create_user(label: str) -> dict[str, str]:
    host = os.environ["FIREBASE_AUTH_EMULATOR_HOST"]
    url = f"http://{host}/identitytoolkit.googleapis.com/v1/accounts:signUp?key=fake"
    payload = {
        "email": f"{label}-{uuid4().hex}@example.test",
        "password": "test-password-123",
        "returnSecureToken": True,
    }
    async with httpx.AsyncClient() as emulator:
        response = await emulator.post(url, json=payload)
        response.raise_for_status()
    return {"Authorization": f"Bearer {response.json()['idToken']}"}


@pytest.fixture
async def user_a():
    return await _create_user("user-a")


@pytest.fixture
async def user_b():
    return await _create_user("user-b")
