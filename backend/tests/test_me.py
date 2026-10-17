import asyncio

import pytest
from google.api_core.exceptions import Aborted
from google.cloud.firestore_v1.async_transaction import _AsyncTransactional

from app.core.auth import AuthenticatedUser
from app.repositories import users as users_repository


async def test_me_recovers_after_transaction_contention(client, user_a, monkeypatch):
    original_run = _AsyncTransactional.__call__
    transaction_rounds = 0

    async def contended_run(self, transaction, *args, **kwargs):
        nonlocal transaction_rounds
        transaction_rounds += 1
        if transaction_rounds == 1:
            # Match the SDK's exhaustion error without leaving emulator locks.
            raise ValueError(
                "Failed to commit transaction in 5 attempts."
            ) from Aborted("Synthetic transaction contention")
        return await original_run(self, transaction, *args, **kwargs)

    monkeypatch.setattr(_AsyncTransactional, "__call__", contended_run)

    response = await client.get("/v1/me", headers=user_a)

    assert response.status_code == 200
    assert transaction_rounds == 2


async def test_profile_does_not_retry_unrelated_value_error(app, client, monkeypatch):
    original_error = ValueError("Synthetic non-contention failure")
    commit_calls = 0

    async def invalid_commit(_transaction):
        nonlocal commit_calls
        commit_calls += 1
        raise original_error

    monkeypatch.setattr(
        users_repository.firestore.AsyncTransaction, "_commit", invalid_commit
    )
    repository = users_repository.UsersRepository(app.state.firestore)
    user = AuthenticatedUser("synthetic-user", None, None)

    with pytest.raises(ValueError) as failure:
        await repository.get_or_create(user)

    assert failure.value is original_error
    assert commit_calls == 1


async def test_me_creates_profile_once(client, app, user_a):
    first_response = await client.get("/v1/me", headers=user_a)
    assert first_response.status_code == 200
    profile = first_response.json()

    reference = app.state.firestore.collection("users").document(profile["uid"])
    first_document = await reference.get()
    first_created_at = first_document.get("created_at")

    second_response = await client.get("/v1/me", headers=user_a)
    second_document = await reference.get()

    assert second_response.status_code == 200
    assert second_response.json() == profile
    assert second_document.get("created_at") == first_created_at
    assert first_document.to_dict() == second_document.to_dict()
    assert profile == {
        "uid": profile["uid"],
        "email": profile["email"],
        "display_name": None,
        "onboarding_completed": False,
    }


async def test_concurrent_first_calls_create_one_profile(client, app, user_a):
    responses = await asyncio.gather(
        *(client.get("/v1/me", headers=user_a) for _ in range(5))
    )

    assert {response.status_code for response in responses} == {200}
    assert len({response.json()["uid"] for response in responses}) == 1
    documents = [
        document async for document in app.state.firestore.collection("users").stream()
    ]
    assert len(documents) == 1


async def test_users_get_separate_profiles(client, app, user_a, user_b):
    response_a, response_b = await asyncio.gather(
        client.get("/v1/me", headers=user_a),
        client.get("/v1/me", headers=user_b),
    )

    assert response_a.status_code == response_b.status_code == 200
    assert response_a.json()["uid"] != response_b.json()["uid"]
    assert response_a.json()["email"] != response_b.json()["email"]
    documents = [
        document async for document in app.state.firestore.collection("users").stream()
    ]
    assert {document.id for document in documents} == {
        response_a.json()["uid"],
        response_b.json()["uid"],
    }
