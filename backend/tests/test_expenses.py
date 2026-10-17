from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.repositories.expenses import ExpensesRepository


def assert_error(response, status, code):
    assert response.status_code == status
    assert response.json()["error"]["code"] == code


async def categories(client, headers):
    response = await client.post(
        "/v1/categories/onboarding",
        headers=headers,
        json={"catalog_ids": ["groceries", "transport"], "custom": []},
    )
    assert response.status_code == 201
    return response.json()["categories"]


def expense_body(category_id, **changes):
    body = {
        "id": str(uuid4()),
        "date": "2026-10-16T12:30:00+02:00",
        "category": category_id,
        "amount": 23.4,
        "currency": "EUR",
        "seller": "Esselunga",
        "title": "Weekly groceries",
        "description": None,
    }
    body.update(changes)
    return body


async def create(client, headers, category_id, **changes):
    return await client.post(
        "/v1/expenses",
        headers=headers,
        json=expense_body(category_id, **changes),
    )


async def test_create_is_idempotent_and_serializes_the_full_expense(client, user_a):
    category = (await categories(client, user_a))[0]
    body = expense_body(category["id"])

    first = await client.post("/v1/expenses", headers=user_a, json=body)
    repeated = await client.post(
        "/v1/expenses", headers=user_a, json={**body, "title": "Ignored retry"}
    )

    assert first.status_code == 201
    assert repeated.status_code == 200
    assert repeated.json() == first.json()
    expense = first.json()
    assert set(expense) == {
        "id",
        "owner",
        "date",
        "seller",
        "title",
        "description",
        "category",
        "type",
        "recurrence",
        "amount",
        "currency",
        "source",
        "scan_details",
        "needs_review",
        "created_at",
        "updated_at",
        "deleted_at",
    }
    assert expense["date"] == "2026-10-16T10:30:00Z"
    assert expense["amount"] == 23.4
    assert expense["type"] == "single"
    assert expense["source"] == "manual"
    assert expense["recurrence"] is expense["scan_details"] is None
    assert expense["needs_review"] is False
    assert expense["deleted_at"] is None


@pytest.mark.parametrize("amount", [0.001, 0, 1000000.01])
async def test_create_rejects_invalid_amounts(client, user_a, amount):
    category = (await categories(client, user_a))[0]
    assert_error(
        await create(client, user_a, category["id"], amount=amount),
        422,
        "validation_error",
    )


async def test_nullable_amount_and_integer_cents_are_exact(client, app, user_a):
    category = (await categories(client, user_a))[0]
    missing = await create(client, user_a, category["id"], amount=None)
    first = await create(client, user_a, category["id"], amount=0.10)
    second = await create(client, user_a, category["id"], amount=0.20)

    assert missing.status_code == 201
    assert missing.json()["amount"] is None
    uid = missing.json()["owner"]
    expense_ids = [first.json()["id"], second.json()["id"]]
    snapshots = [
        await app.state.firestore.collection("users")
        .document(uid)
        .collection("expenses")
        .document(expense_id)
        .get()
        for expense_id in expense_ids
    ]
    assert sum(snapshot.get("amount_cents") for snapshot in snapshots) == 30


async def test_category_must_be_active_on_create_and_update(client, user_a):
    active, archived, *_ = await categories(client, user_a)
    assert (
        await client.delete(f"/v1/categories/{archived['id']}", headers=user_a)
    ).status_code == 204

    assert_error(await create(client, user_a, "cat_missing"), 422, "category_not_found")
    assert_error(
        await create(client, user_a, archived["id"]), 422, "category_not_found"
    )

    expense = await create(client, user_a, active["id"])
    assert_error(
        await client.patch(
            f"/v1/expenses/{expense.json()['id']}",
            headers=user_a,
            json={"category": archived["id"]},
        ),
        422,
        "category_not_found",
    )


async def test_patch_updates_allowed_fields_and_rejects_forbidden_fields(
    client, user_a
):
    first, second, *_ = await categories(client, user_a)
    created = await create(client, user_a, first["id"])
    expense_id = created.json()["id"]

    updated = await client.patch(
        f"/v1/expenses/{expense_id}",
        headers=user_a,
        json={
            "date": "2026-11-01T01:30:00-04:00",
            "seller": None,
            "title": None,
            "description": "Updated",
            "category": second["id"],
            "amount": None,
            "currency": "EUR",
            "needs_review": True,
        },
    )
    assert updated.status_code == 200
    assert updated.json()["date"] == "2026-11-01T05:30:00Z"
    assert updated.json()["seller"] is updated.json()["title"] is None
    assert updated.json()["description"] == "Updated"
    assert updated.json()["category"] == second["id"]
    assert updated.json()["amount"] is None
    assert updated.json()["needs_review"] is True
    assert updated.json()["updated_at"] >= created.json()["updated_at"]

    assert_error(
        await client.patch(
            f"/v1/expenses/{expense_id}",
            headers=user_a,
            json={"type": "recurring"},
        ),
        422,
        "validation_error",
    )


async def test_list_filters_and_repository_range(client, app, user_a):
    first, second, *_ = await categories(client, user_a)
    older = await create(
        client,
        user_a,
        first["id"],
        date="2026-10-01T00:00:00Z",
        amount=None,
    )
    newer = await create(
        client,
        user_a,
        second["id"],
        date="2026-10-20T00:00:00Z",
    )
    await client.patch(
        f"/v1/expenses/{newer.json()['id']}",
        headers=user_a,
        json={"needs_review": True},
    )

    cases = [
        ({"from": "2026-10-10T00:00:00Z"}, {newer.json()["id"]}),
        ({"to": "2026-10-10T00:00:00Z"}, {older.json()["id"]}),
        ({"category": first["id"]}, {older.json()["id"]}),
        ({"type": "single"}, {older.json()["id"], newer.json()["id"]}),
        ({"type": "recurring"}, set()),
        ({"needs_review": "true"}, {newer.json()["id"]}),
    ]
    for params, expected in cases:
        response = await client.get("/v1/expenses", headers=user_a, params=params)
        assert response.status_code == 200
        assert {item["id"] for item in response.json()["items"]} == expected

    repository = ExpensesRepository(app.state.firestore)
    ranged = [
        item
        async for item in repository.list_in_range(
            older.json()["owner"],
            datetime(2026, 10, 10, tzinfo=UTC),
            datetime(2026, 11, 1, tzinfo=UTC),
        )
    ]
    assert [item["id"] for item in ranged] == [newer.json()["id"]]


async def test_pagination_has_no_duplicates_or_gaps(client, user_a):
    category = (await categories(client, user_a))[0]
    ids = [str(uuid4()) for _ in range(5)]
    for expense_id in ids:
        response = await create(
            client,
            user_a,
            category["id"],
            id=expense_id,
            date="2026-10-16T10:00:00Z",
        )
        assert response.status_code == 201

    seen = []
    cursor = None
    page_sizes = []
    while True:
        params = {"limit": 2}
        if cursor is not None:
            params["cursor"] = cursor
        response = await client.get("/v1/expenses", headers=user_a, params=params)
        assert response.status_code == 200
        page = response.json()
        page_sizes.append(len(page["items"]))
        seen.extend(item["id"] for item in page["items"])
        cursor = page["next_cursor"]
        if cursor is None:
            break

    assert page_sizes == [2, 2, 1]
    assert seen == sorted(ids, reverse=True)
    assert len(seen) == len(set(seen)) == 5
    assert_error(
        await client.get(
            "/v1/expenses", headers=user_a, params={"cursor": "not-a-cursor"}
        ),
        422,
        "validation_error",
    )


async def test_soft_delete_hides_expense_and_deleted_id_is_not_recreated(
    client, user_a
):
    category = (await categories(client, user_a))[0]
    body = expense_body(category["id"])
    created = await client.post("/v1/expenses", headers=user_a, json=body)
    expense_id = created.json()["id"]

    assert (
        await client.delete(f"/v1/expenses/{expense_id}", headers=user_a)
    ).status_code == 204
    assert_error(
        await client.get(f"/v1/expenses/{expense_id}", headers=user_a),
        404,
        "not_found",
    )
    listed = await client.get("/v1/expenses", headers=user_a)
    assert listed.json() == {"items": [], "next_cursor": None}
    assert_error(
        await client.post("/v1/expenses", headers=user_a, json=body),
        404,
        "not_found",
    )


async def test_user_cannot_access_another_users_expense(client, user_a, user_b):
    category = (await categories(client, user_a))[0]
    expense = await create(client, user_a, category["id"])
    expense_id = expense.json()["id"]

    assert_error(
        await client.get(f"/v1/expenses/{expense_id}", headers=user_b),
        404,
        "not_found",
    )
    assert_error(
        await client.patch(
            f"/v1/expenses/{expense_id}", headers=user_b, json={"title": "Mine"}
        ),
        404,
        "not_found",
    )
    assert_error(
        await client.delete(f"/v1/expenses/{expense_id}", headers=user_b),
        404,
        "not_found",
    )
    listed = await client.get("/v1/expenses", headers=user_b)
    assert listed.json() == {"items": [], "next_cursor": None}
