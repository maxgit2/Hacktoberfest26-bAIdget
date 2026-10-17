import pytest
from firebase_admin import auth as firebase_auth

from app.core import auth as auth_module


def assert_unauthenticated(response):
    assert response.status_code == 401
    assert response.json() == {
        "error": {
            "code": "unauthenticated",
            "message": "Authentication required",
            "details": {},
        }
    }


@pytest.mark.parametrize(
    "headers",
    [
        None,
        {"Authorization": "Bearer"},
        {"Authorization": "Bearer not-a-token"},
    ],
    ids=["missing", "malformed", "invalid"],
)
async def test_authentication_failures(client, headers):
    response = await client.get("/v1/me", headers=headers)

    assert_unauthenticated(response)


async def test_expired_token_is_unauthenticated(client, monkeypatch):
    def expired(*_args, **_kwargs):
        raise firebase_auth.ExpiredIdTokenError("Token expired", None)

    monkeypatch.setattr(auth_module.firebase_auth, "verify_id_token", expired)

    response = await client.get(
        "/v1/me", headers={"Authorization": "Bearer expired-token"}
    )

    assert_unauthenticated(response)
