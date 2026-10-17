import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ROME = ZoneInfo("Europe/Rome")


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


async def create_expense(client, headers, category_id, date):
    response = await client.post(
        "/v1/expenses",
        headers=headers,
        json={
            "date": date.isoformat(),
            "category": category_id,
            "amount": 12.99,
            "currency": "EUR",
            "seller": "Netflix",
            "title": "Netflix",
        },
    )
    assert response.status_code == 201
    return response.json()


async def make_recurring(
    client, headers, expense_id, frequency="weekly", end_date=None
):
    body = {"frequency": frequency}
    if end_date is not None:
        body["end_date"] = end_date.isoformat()
    return await client.post(
        f"/v1/expenses/{expense_id}/make-recurring", headers=headers, json=body
    )


async def raw_expenses(app, uid):
    return await (
        app.state.firestore.collection("users")
        .document(uid)
        .collection("expenses")
        .get()
    )


def rule_reference(app, uid, rule_id):
    return (
        app.state.firestore.collection("users")
        .document(uid)
        .collection("recurring_rules")
        .document(rule_id)
    )


async def test_make_recurring_shape_and_sync_is_idempotent(client, app, user_a):
    category = (await categories(client, user_a))[0]
    expense = await create_expense(
        client, user_a, category["id"], datetime.now(ROME) - timedelta(days=22)
    )

    response = await make_recurring(client, user_a, expense["id"])

    assert response.status_code == 201
    result = response.json()
    assert result["created_occurrences"] == 3
    assert result["expense"]["type"] == "recurring"
    assert result["expense"]["recurrence"] == {"rule_id": result["rule"]["id"]}
    assert result["rule"]["template"] == {
        "seller": "Netflix",
        "title": "Netflix",
        "description": None,
        "category": category["id"],
        "amount": 12.99,
        "currency": "EUR",
    }
    assert set(result["rule"]) == {
        "id",
        "frequency",
        "start",
        "end_date",
        "active",
        "template",
    }

    raw = await raw_expenses(app, expense["owner"])
    occurrences = [item for item in raw if item.get("type") == "recurring"]
    assert len(occurrences) == 4
    assert {item.get("source") for item in occurrences} == {"manual"}
    assert {item.get("needs_review") for item in occurrences} == {False}
    assert {item.get("scan_details") for item in occurrences} == {None}
    assert {item.get("deleted_at") for item in occurrences} == {None}
    assert {item.get("recurrence")["index"] for item in occurrences} == {0, 1, 2, 3}
    listed = (await client.get("/v1/expenses", headers=user_a)).json()["items"]
    assert all(set(item["recurrence"]) == {"rule_id"} for item in listed)

    first_sync = await client.post("/v1/recurring-rules/sync", headers=user_a)
    second_sync = await client.post("/v1/recurring-rules/sync", headers=user_a)
    assert first_sync.json() == {
        "created": 0,
        "rules_processed": 1,
        "has_more": False,
    }
    assert second_sync.json()["created"] == 0
    assert_error(
        await make_recurring(client, user_a, expense["id"]),
        409,
        "already_recurring",
    )


async def test_soft_deleted_occurrence_is_never_recreated(client, app, user_a):
    category = (await categories(client, user_a))[0]
    expense = await create_expense(
        client, user_a, category["id"], datetime.now(ROME) - timedelta(days=15)
    )
    made = (await make_recurring(client, user_a, expense["id"])).json()
    rule_id = made["rule"]["id"]
    snapshots = await raw_expenses(app, expense["owner"])
    occurrence = next(
        item for item in snapshots if item.get("recurrence")["index"] == 1
    )

    assert (
        await client.delete(f"/v1/expenses/{occurrence.id}", headers=user_a)
    ).status_code == 204
    await rule_reference(app, expense["owner"], rule_id).update({"next_index": 1})

    synced = await client.post("/v1/recurring-rules/sync", headers=user_a)

    assert synced.status_code == 200
    assert synced.json()["created"] == 0
    assert_error(
        await client.get(f"/v1/expenses/{occurrence.id}", headers=user_a),
        404,
        "not_found",
    )
    assert (await occurrence.reference.get()).get("deleted_at") is not None


async def test_reactivation_skips_the_paused_period(client, app, user_a):
    category = (await categories(client, user_a))[0]
    expense = await create_expense(
        client, user_a, category["id"], datetime.now(ROME) - timedelta(days=100)
    )
    made = (
        await make_recurring(client, user_a, expense["id"], frequency="monthly")
    ).json()
    rule_id = made["rule"]["id"]
    uid = expense["owner"]

    paused = await client.patch(
        f"/v1/recurring-rules/{rule_id}", headers=user_a, json={"active": False}
    )
    assert paused.status_code == 200
    for snapshot in await raw_expenses(app, uid):
        if snapshot.get("recurrence")["index"] > 0:
            await snapshot.reference.delete()
    await rule_reference(app, uid, rule_id).update({"next_index": 1})

    resumed = await client.patch(
        f"/v1/recurring-rules/{rule_id}", headers=user_a, json={"active": True}
    )
    synced = await client.post("/v1/recurring-rules/sync", headers=user_a)

    assert resumed.status_code == 200
    assert synced.json()["created"] == 0
    assert len(await raw_expenses(app, uid)) == 1
    stored_rule = await rule_reference(app, uid, rule_id).get()
    assert stored_rule.get("next_index") > 1
    assert stored_rule.get("resume_from") is not None


async def test_patch_delete_and_category_validation(client, app, user_a):
    first, archived, *_ = await categories(client, user_a)
    assert (
        await client.delete(f"/v1/categories/{archived['id']}", headers=user_a)
    ).status_code == 204
    expense = await create_expense(client, user_a, first["id"], datetime.now(ROME))
    made = (await make_recurring(client, user_a, expense["id"])).json()
    rule_id = made["rule"]["id"]

    assert_error(
        await client.patch(
            f"/v1/recurring-rules/{rule_id}",
            headers=user_a,
            json={"category": archived["id"]},
        ),
        422,
        "category_not_found",
    )
    assert_error(
        await client.patch(
            f"/v1/recurring-rules/{rule_id}",
            headers=user_a,
            json={"frequency": "yearly"},
        ),
        422,
        "validation_error",
    )
    patched = await client.patch(
        f"/v1/recurring-rules/{rule_id}",
        headers=user_a,
        json={"seller": None, "title": "Streaming", "amount": None},
    )
    assert patched.status_code == 200
    assert patched.json()["template"]["seller"] is None
    assert patched.json()["template"]["title"] == "Streaming"
    assert patched.json()["template"]["amount"] is None
    source = await client.get(f"/v1/expenses/{expense['id']}", headers=user_a)
    assert source.json()["title"] == "Netflix"

    assert (
        await client.delete(f"/v1/recurring-rules/{rule_id}", headers=user_a)
    ).status_code == 204
    listed = await client.get("/v1/recurring-rules", headers=user_a)
    assert listed.json()["items"][0]["active"] is False
    assert len(await raw_expenses(app, expense["owner"])) == 1


async def test_end_date_caps_occurrences_and_active_rule_blocks_category_delete(
    client, user_a
):
    category = (await categories(client, user_a))[0]
    start = datetime.now(ROME) - timedelta(days=30)
    expense = await create_expense(client, user_a, category["id"], start)
    made = await make_recurring(
        client, user_a, expense["id"], end_date=start.date() + timedelta(days=14)
    )

    assert made.status_code == 201
    assert made.json()["created_occurrences"] == 2
    expenses = (await client.get("/v1/expenses", headers=user_a)).json()["items"]
    assert all(
        datetime.fromisoformat(item["date"]).astimezone(ROME).date()
        <= start.date() + timedelta(days=14)
        for item in expenses
    )
    for item in expenses:
        assert (
            await client.delete(f"/v1/expenses/{item['id']}", headers=user_a)
        ).status_code == 204
    assert_error(
        await client.delete(f"/v1/categories/{category['id']}", headers=user_a),
        409,
        "category_in_use",
    )


async def test_sync_caps_occurrences_and_rules(client, app, user_a):
    category = (await categories(client, user_a))[0]
    old_expense = await create_expense(
        client, user_a, category["id"], datetime.now(ROME) - timedelta(weeks=120)
    )
    made = await make_recurring(client, user_a, old_expense["id"])
    assert made.json()["created_occurrences"] == 50

    synced = await client.post("/v1/recurring-rules/sync", headers=user_a)
    assert synced.json()["created"] == 50
    assert synced.json()["has_more"] is True

    future_expense = await create_expense(
        client, user_a, category["id"], datetime.now(ROME) + timedelta(days=1)
    )
    future = (await make_recurring(client, user_a, future_expense["id"])).json()
    uid = future_expense["owner"]
    source_rule = await rule_reference(app, uid, future["rule"]["id"]).get()
    rule_document = source_rule.to_dict()
    rules = (
        app.state.firestore.collection("users")
        .document(uid)
        .collection("recurring_rules")
    )
    for index in range(20):
        await rules.document(f"rule_cap_{index:02}").set(rule_document)

    capped = await client.post("/v1/recurring-rules/sync", headers=user_a)
    assert capped.status_code == 200
    assert capped.json()["rules_processed"] == 20
    assert capped.json()["has_more"] is True


async def test_concurrent_sync_has_no_duplicates(client, app, user_a):
    category = (await categories(client, user_a))[0]
    expense = await create_expense(
        client, user_a, category["id"], datetime.now(ROME) - timedelta(days=29)
    )
    made = (await make_recurring(client, user_a, expense["id"])).json()
    expected = made["created_occurrences"]
    uid = expense["owner"]
    for snapshot in await raw_expenses(app, uid):
        if snapshot.get("recurrence")["index"] > 0:
            await snapshot.reference.delete()
    await rule_reference(app, uid, made["rule"]["id"]).update({"next_index": 1})

    responses = await asyncio.gather(
        *(client.post("/v1/recurring-rules/sync", headers=user_a) for _ in range(3))
    )

    assert all(response.status_code == 200 for response in responses)
    assert sum(response.json()["created"] for response in responses) == expected
    snapshots = await raw_expenses(app, uid)
    assert len(snapshots) == expected + 1
    assert len({snapshot.id for snapshot in snapshots}) == expected + 1


async def test_other_user_cannot_touch_rules_or_sync_expenses(
    client, app, user_a, user_b
):
    category = (await categories(client, user_a))[0]
    expense = await create_expense(
        client, user_a, category["id"], datetime.now(ROME) - timedelta(days=8)
    )
    made = (await make_recurring(client, user_a, expense["id"])).json()
    rule_id = made["rule"]["id"]
    before = len(await raw_expenses(app, expense["owner"]))

    assert (await client.get("/v1/recurring-rules", headers=user_b)).json() == {
        "items": []
    }
    assert_error(
        await client.patch(
            f"/v1/recurring-rules/{rule_id}",
            headers=user_b,
            json={"active": False},
        ),
        404,
        "not_found",
    )
    assert_error(
        await client.delete(f"/v1/recurring-rules/{rule_id}", headers=user_b),
        404,
        "not_found",
    )
    assert_error(await make_recurring(client, user_b, expense["id"]), 404, "not_found")
    synced = await client.post("/v1/recurring-rules/sync", headers=user_b)
    assert synced.json() == {"created": 0, "rules_processed": 0, "has_more": False}
    assert len(await raw_expenses(app, expense["owner"])) == before


async def test_deleted_expense_cannot_be_made_recurring(client, user_a):
    category = (await categories(client, user_a))[0]
    expense = await create_expense(client, user_a, category["id"], datetime.now(ROME))
    assert (
        await client.delete(f"/v1/expenses/{expense['id']}", headers=user_a)
    ).status_code == 204

    assert_error(await make_recurring(client, user_a, expense["id"]), 404, "not_found")
