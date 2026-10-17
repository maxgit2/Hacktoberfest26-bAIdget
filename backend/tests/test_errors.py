from fastapi import Query

from app.core.errors import AppError


def assert_error(response, status, code):
    assert response.status_code == status
    assert response.json()["error"]["code"] == code
    assert set(response.json()["error"]) == {"code", "message", "details"}


async def test_unknown_route(client):
    assert_error(await client.get("/missing"), 404, "not_found")


async def test_invalid_query(client, app):
    @app.get("/v1/validated")
    async def validated(limit: int = Query(ge=1)):
        return {"limit": limit}

    response = await client.get("/v1/validated?limit=bad")

    assert_error(response, 422, "validation_error")
    assert response.json()["error"]["details"]["fields"][0]["field"] == "limit"


async def test_app_error(client, app):
    @app.get("/v1/app-error")
    async def app_error():
        raise AppError("not_found", 404, "Missing", {"resource": "test"})

    response = await client.get("/v1/app-error")

    assert_error(response, 404, "not_found")
    assert response.json()["error"]["details"] == {"resource": "test"}


async def test_unhandled_error(client, app):
    @app.get("/v1/boom")
    async def boom():
        raise RuntimeError("not exposed")

    response = await client.get("/v1/boom")

    assert_error(response, 500, "internal_error")
    assert "not exposed" not in response.text
