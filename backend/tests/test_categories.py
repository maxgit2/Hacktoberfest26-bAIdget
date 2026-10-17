from app.repositories.categories import CategoriesRepository


async def onboard(client, headers, **body):
    return await client.post(
        "/v1/categories/onboarding",
        headers=headers,
        json=body or {"catalog_ids": ["groceries", "transport"], "custom": []},
    )


def assert_error(response, status, code):
    assert response.status_code == status
    assert response.json()["error"]["code"] == code


async def test_catalog_shape(client, user_a):
    response = await client.get("/v1/categories/catalog", headers=user_a)

    assert response.status_code == 200
    catalog = response.json()
    assert [item["id"] for item in catalog["items"]] == [
        "groceries",
        "dining_out",
        "transport",
        "housing",
        "bills",
        "health",
        "entertainment",
        "shopping",
        "travel",
        "education",
        "subscriptions",
    ]
    assert all(set(item) == {"id", "name", "icon"} for item in catalog["items"])
    assert catalog["presets"] == [
        {
            "id": "essential_4",
            "name": "Essential",
            "catalog_ids": [
                "groceries",
                "transport",
                "housing",
                "entertainment",
            ],
        },
        {
            "id": "complete_6",
            "name": "Complete",
            "catalog_ids": [
                "groceries",
                "transport",
                "housing",
                "entertainment",
                "dining_out",
                "health",
            ],
        },
    ]


async def test_onboarding_creates_categories_and_updates_user(client, app, user_a):
    response = await onboard(
        client,
        user_a,
        catalog_ids=["groceries", "transport"],
        custom=[{"name": "Pets", "icon": "pets", "color": "#FF9800"}],
    )

    assert response.status_code == 201
    categories = response.json()["categories"]
    assert {category["name"] for category in categories} == {
        "Groceries",
        "Transport",
        "Pets",
        "Other",
    }
    assert (
        next(category for category in categories if category["is_other"])["name"]
        == "Other"
    )

    uid = (await client.get("/v1/me", headers=user_a)).json()["uid"]
    user = await app.state.firestore.collection("users").document(uid).get()
    assert user.get("onboarding_completed") is True


async def test_onboarding_rejects_invalid_requests(client, user_a):
    assert_error(
        await onboard(client, user_a, catalog_ids=["groceries"], custom=[]),
        422,
        "min_categories",
    )
    assert_error(
        await onboard(client, user_a, catalog_ids=["missing", "groceries"], custom=[]),
        422,
        "validation_error",
    )

    custom = [{"name": f"Category {index}"} for index in range(30)]
    assert_error(
        await onboard(client, user_a, catalog_ids=[], custom=custom),
        422,
        "max_categories",
    )


async def test_onboarding_is_once_and_names_are_unique(client, user_a):
    duplicate = await onboard(
        client,
        user_a,
        catalog_ids=["groceries"],
        custom=[{"name": "Groceries"}],
    )
    assert_error(duplicate, 409, "category_name_taken")

    assert (await onboard(client, user_a)).status_code == 201
    assert_error(await onboard(client, user_a), 409, "already_onboarded")


async def test_category_crud_and_archived_category_is_hidden(client, app, user_a):
    await onboard(client, user_a)
    created = await client.post(
        "/v1/categories",
        headers=user_a,
        json={"name": "Gym", "icon": "fitness_center", "color": "#2196F3"},
    )
    assert created.status_code == 201
    category = created.json()
    assert category["catalog_id"] is None
    assert category["is_other"] is False

    updated = await client.patch(
        f"/v1/categories/{category['id']}",
        headers=user_a,
        json={"name": "Fitness", "color": None},
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Fitness"
    assert updated.json()["color"] is None

    deleted = await client.delete(f"/v1/categories/{category['id']}", headers=user_a)
    assert deleted.status_code == 204
    listed = await client.get("/v1/categories", headers=user_a)
    assert category["id"] not in {item["id"] for item in listed.json()["items"]}

    uid = (await client.get("/v1/me", headers=user_a)).json()["uid"]
    document = await (
        app.state.firestore.collection("users")
        .document(uid)
        .collection("categories")
        .document(category["id"])
        .get()
    )
    assert document.get("archived_at") is not None


async def test_create_and_rename_enforce_unique_active_names(client, user_a):
    onboarded = await onboard(client, user_a)
    transport = next(
        item
        for item in onboarded.json()["categories"]
        if item["catalog_id"] == "transport"
    )

    assert_error(
        await client.post("/v1/categories", headers=user_a, json={"name": "gRoCeRiEs"}),
        409,
        "category_name_taken",
    )
    assert_error(
        await client.patch(
            f"/v1/categories/{transport['id']}",
            headers=user_a,
            json={"name": "Groceries"},
        ),
        409,
        "category_name_taken",
    )


async def test_other_can_be_renamed_but_not_deleted(client, user_a):
    response = await onboard(client, user_a)
    other = next(
        category for category in response.json()["categories"] if category["is_other"]
    )

    renamed = await client.patch(
        f"/v1/categories/{other['id']}",
        headers=user_a,
        json={"name": "Miscellaneous"},
    )
    assert renamed.status_code == 200
    assert renamed.json()["name"] == "Miscellaneous"
    assert_error(
        await client.delete(f"/v1/categories/{other['id']}", headers=user_a),
        409,
        "cannot_modify_other",
    )


async def test_user_cannot_modify_another_users_category(client, user_a, user_b):
    created = await onboard(client, user_a)
    category_id = created.json()["categories"][0]["id"]

    listed = await client.get("/v1/categories", headers=user_b)
    assert listed.status_code == 200
    assert listed.json() == {"items": []}
    assert_error(
        await client.patch(
            f"/v1/categories/{category_id}",
            headers=user_b,
            json={"name": "Stolen"},
        ),
        404,
        "not_found",
    )
    assert_error(
        await client.delete(f"/v1/categories/{category_id}", headers=user_b),
        404,
        "not_found",
    )


async def test_repository_helpers_find_active_and_used_categories(client, app, user_a):
    response = await onboard(client, user_a)
    category = response.json()["categories"][0]
    uid = (await client.get("/v1/me", headers=user_a)).json()["uid"]
    repository = CategoriesRepository(app.state.firestore)

    assert (await repository.get_active_category(uid, category["id"]))["id"] == (
        category["id"]
    )
    assert await repository.is_category_in_use(uid, category["id"]) is False


async def test_category_with_a_non_deleted_expense_cannot_be_deleted(client, user_a):
    response = await onboard(client, user_a)
    category = response.json()["categories"][0]
    expense = await client.post(
        "/v1/expenses",
        headers=user_a,
        json={
            "date": "2026-10-16T10:30:00Z",
            "category": category["id"],
            "amount": 12.34,
            "currency": "EUR",
        },
    )
    assert expense.status_code == 201

    assert_error(
        await client.delete(f"/v1/categories/{category['id']}", headers=user_a),
        409,
        "category_in_use",
    )

    assert (
        await client.delete(f"/v1/expenses/{expense.json()['id']}", headers=user_a)
    ).status_code == 204
    assert (
        await client.delete(f"/v1/categories/{category['id']}", headers=user_a)
    ).status_code == 204
