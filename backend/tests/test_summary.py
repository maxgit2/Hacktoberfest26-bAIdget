from datetime import UTC, datetime
from uuid import uuid4

import pytest


async def categories(client, headers):
    response = await client.post(
        "/v1/categories/onboarding",
        headers=headers,
        json={"catalog_ids": ["groceries", "transport"], "custom": []},
    )
    assert response.status_code == 201
    return response.json()["categories"]


async def create_expense(client, headers, category_id, date, amount):
    response = await client.post(
        "/v1/expenses",
        headers=headers,
        json={
            "id": str(uuid4()),
            "date": date,
            "category": category_id,
            "amount": amount,
            "currency": "EUR",
        },
    )
    assert response.status_code == 201
    return response.json()


@pytest.mark.parametrize(
    ("month", "from_utc", "to_utc"),
    [
        ("2026-03", "2026-02-28T23:00:00Z", "2026-03-31T22:00:00Z"),
        ("2026-10", "2026-09-30T22:00:00Z", "2026-10-31T23:00:00Z"),
    ],
)
async def test_monthly_uses_rome_dst_boundaries(
    client, user_a, month, from_utc, to_utc
):
    response = await client.get(
        "/v1/summary/monthly", headers=user_a, params={"month": month}
    )

    assert response.status_code == 200
    assert response.json() == {
        "period": {"type": "month", "value": month, "from": from_utc, "to": to_utc},
        "currency": "EUR",
        "total": 0.0,
        "count": 0,
        "uncounted": 0,
        "by_category": [],
    }


async def test_monthly_aggregates_exact_cents_and_excludes_null_amounts(client, user_a):
    groceries, transport, *_ = await categories(client, user_a)
    await create_expense(
        client, user_a, groceries["id"], "2026-10-31T23:30:00+01:00", 10.10
    )
    await create_expense(
        client, user_a, groceries["id"], "2026-10-15T12:00:00+02:00", 0.20
    )
    await create_expense(
        client, user_a, transport["id"], "2026-10-16T12:00:00+02:00", 5
    )
    await create_expense(
        client, user_a, transport["id"], "2026-10-17T12:00:00+02:00", None
    )
    await create_expense(
        client, user_a, groceries["id"], "2026-11-01T00:00:00+01:00", 99
    )

    response = await client.get(
        "/v1/summary/monthly", headers=user_a, params={"month": "2026-10"}
    )

    assert response.status_code == 200
    summary = response.json()
    assert summary["total"] == 15.3
    assert summary["count"] == 3
    assert summary["uncounted"] == 1
    assert summary["by_category"] == [
        {
            "category": groceries["id"],
            "name": "Groceries",
            "total": 10.3,
            "count": 2,
            "percentage": 67.3,
        },
        {
            "category": transport["id"],
            "name": "Transport",
            "total": 5.0,
            "count": 1,
            "percentage": 32.7,
        },
    ]


async def test_archived_category_name_is_included(client, app, user_a):
    category = (await categories(client, user_a))[0]
    expense = await create_expense(
        client, user_a, category["id"], "2026-10-10T12:00:00+02:00", 12.34
    )
    await (
        app.state.firestore.collection("users")
        .document(expense["owner"])
        .collection("categories")
        .document(category["id"])
        .update({"archived_at": datetime.now(UTC)})
    )

    response = await client.get(
        "/v1/summary/monthly", headers=user_a, params={"month": "2026-10"}
    )

    assert response.status_code == 200
    assert response.json()["by_category"][0]["name"] == "Groceries"


async def test_yearly_always_returns_twelve_months(client, user_a):
    category = (await categories(client, user_a))[0]
    await create_expense(
        client, user_a, category["id"], "2026-03-20T12:00:00+01:00", 7.25
    )

    response = await client.get(
        "/v1/summary/yearly", headers=user_a, params={"year": "2026"}
    )

    assert response.status_code == 200
    summary = response.json()
    assert len(summary["by_month"]) == 12
    assert [item["month"] for item in summary["by_month"]] == [
        f"2026-{month:02d}" for month in range(1, 13)
    ]
    assert summary["by_month"][2] == {
        "month": "2026-03",
        "total": 7.25,
        "count": 1,
    }
    assert all(
        item == {"month": item["month"], "total": 0.0, "count": 0}
        for index, item in enumerate(summary["by_month"])
        if index != 2
    )


@pytest.mark.parametrize(
    ("path", "params"),
    [
        ("/v1/summary/monthly", {"month": "2026-13"}),
        ("/v1/summary/monthly", {"month": "October"}),
        ("/v1/summary/yearly", {"year": "0000"}),
        ("/v1/summary/yearly", {"year": "26"}),
    ],
)
async def test_invalid_period_is_validation_error(client, user_a, path, params):
    response = await client.get(path, headers=user_a, params=params)

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


async def test_other_user_sees_no_expenses(client, user_a, user_b):
    category = (await categories(client, user_a))[0]
    await create_expense(
        client, user_a, category["id"], "2026-10-10T12:00:00+02:00", 42
    )

    monthly = await client.get(
        "/v1/summary/monthly", headers=user_b, params={"month": "2026-10"}
    )
    yearly = await client.get(
        "/v1/summary/yearly", headers=user_b, params={"year": "2026"}
    )

    assert monthly.status_code == yearly.status_code == 200
    assert monthly.json()["total"] == yearly.json()["total"] == 0.0
    assert monthly.json()["count"] == yearly.json()["count"] == 0
    assert monthly.json()["by_category"] == yearly.json()["by_category"] == []
