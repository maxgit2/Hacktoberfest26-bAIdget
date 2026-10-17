import asyncio


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
