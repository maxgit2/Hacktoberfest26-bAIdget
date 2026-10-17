from collections.abc import AsyncIterator
from datetime import UTC, datetime

from fastapi import Request
from google.cloud import firestore
from google.cloud.firestore import AsyncClient
from google.cloud.firestore_v1.base_query import FieldFilter

from app.repositories.client import get_firestore_client


class ExpensesRepository:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    def _expenses(self, uid: str):
        return self.client.collection("users").document(uid).collection("expenses")

    @staticmethod
    def _expense(uid: str, snapshot) -> dict[str, object]:
        return {"id": snapshot.id, "owner": uid, **snapshot.to_dict()}

    async def create_idempotent(
        self, uid: str, expense_dict: dict[str, object]
    ) -> tuple[dict[str, object], bool]:
        expense_id = str(expense_dict["id"])
        reference = self._expenses(uid).document(expense_id)
        document = {
            key: value
            for key, value in expense_dict.items()
            if key not in {"id", "owner"}
        }
        transaction = self.client.transaction()

        @firestore.async_transactional
        async def create_in_transaction(transaction):
            snapshot = await reference.get(transaction=transaction)
            if snapshot.exists:
                return self._expense(uid, snapshot), False
            transaction.create(reference, document)
            return {"id": expense_id, "owner": uid, **document}, True

        return await create_in_transaction(transaction)

    async def get(self, uid: str, expense_id: str) -> dict[str, object] | None:
        snapshot = await self._expenses(uid).document(expense_id).get()
        if not snapshot.exists or snapshot.get("deleted_at") is not None:
            return None
        return self._expense(uid, snapshot)

    async def list(
        self,
        uid: str,
        filters: dict[str, object],
        limit: int,
        cursor: tuple[datetime, str] | None,
    ) -> tuple[list[dict[str, object]], bool]:
        query = self._expenses(uid).where(filter=FieldFilter("deleted_at", "==", None))
        for field in ("category", "type", "needs_review"):
            if field in filters:
                query = query.where(filter=FieldFilter(field, "==", filters[field]))
        if "from" in filters:
            query = query.where(filter=FieldFilter("date", ">=", filters["from"]))
        if "to" in filters:
            query = query.where(filter=FieldFilter("date", "<", filters["to"]))

        query = query.order_by("date", direction=firestore.Query.DESCENDING).order_by(
            "__name__", direction=firestore.Query.DESCENDING
        )
        if cursor is not None:
            query = query.start_after({"date": cursor[0], "__name__": cursor[1]})
        snapshots = await query.limit(limit + 1).get()
        return (
            [self._expense(uid, snapshot) for snapshot in snapshots[:limit]],
            len(snapshots) > limit,
        )

    async def update(
        self, uid: str, expense_id: str, changes: dict[str, object]
    ) -> dict[str, object] | None:
        reference = self._expenses(uid).document(expense_id)
        transaction = self.client.transaction()

        @firestore.async_transactional
        async def update_in_transaction(transaction):
            snapshot = await reference.get(transaction=transaction)
            if not snapshot.exists or snapshot.get("deleted_at") is not None:
                return None
            updates = {**changes, "updated_at": datetime.now(UTC)}
            transaction.update(reference, updates)
            return {**self._expense(uid, snapshot), **updates}

        return await update_in_transaction(transaction)

    async def soft_delete(self, uid: str, expense_id: str) -> bool:
        reference = self._expenses(uid).document(expense_id)
        transaction = self.client.transaction()

        @firestore.async_transactional
        async def delete_in_transaction(transaction):
            snapshot = await reference.get(transaction=transaction)
            if not snapshot.exists or snapshot.get("deleted_at") is not None:
                return False
            now = datetime.now(UTC)
            transaction.update(reference, {"deleted_at": now, "updated_at": now})
            return True

        return await delete_in_transaction(transaction)

    async def list_in_range(
        self, uid: str, from_utc: datetime, to_utc: datetime
    ) -> AsyncIterator[dict[str, object]]:
        query = (
            self._expenses(uid)
            .where(filter=FieldFilter("deleted_at", "==", None))
            .where(filter=FieldFilter("date", ">=", from_utc))
            .where(filter=FieldFilter("date", "<", to_utc))
            .order_by("date", direction=firestore.Query.DESCENDING)
        )
        async for snapshot in query.stream():
            yield self._expense(uid, snapshot)


def get_expenses_repository(request: Request) -> ExpensesRepository:
    return ExpensesRepository(get_firestore_client(request))
