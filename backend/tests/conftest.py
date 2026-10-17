import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "demo-baidget")

from app.main import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
