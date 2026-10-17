from collections.abc import Callable
from datetime import date, datetime
from uuid import uuid4

from fastapi import Request
from google.cloud import firestore
from google.cloud.firestore import AsyncClient
from google.cloud.firestore_v1.base_query import FieldFilter

from app.repositories.client import get_firestore_client


class AlreadyRecurringError(Exception):
    pass


type SyncCandidate = tuple[str, dict[str, object]]
type SyncPlan = tuple[list[SyncCandidate], int, bool]
type SyncPlanner = Callable[[dict[str, object]], SyncPlan]


class RulesRepository:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    def _user(self, uid: str):
        return self.client.collection("users").document(uid)

    def _rules(self, uid: str):
        return self._user(uid).collection("recurring_rules")

    @staticmethod
    def _rule(snapshot) -> dict[str, object]:
        return {"id": snapshot.id, **snapshot.to_dict()}

    async def make_recurring(
        self,
        uid: str,
        expense_id: str,
        frequency: str,
        end_date: date | None,
        now: datetime,
    ) -> tuple[dict[str, object], dict[str, object]] | None:
        expense_reference = self._user(uid).collection("expenses").document(expense_id)
        rule_id = f"rule_{uuid4().hex[:8]}"
        rule_reference = self._rules(uid).document(rule_id)
        transaction = self.client.transaction()

        @firestore.async_transactional
        async def create_in_transaction(transaction):
            expense_snapshot = await expense_reference.get(transaction=transaction)
            if (
                not expense_snapshot.exists
                or expense_snapshot.get("deleted_at") is not None
            ):
                return None
            expense = expense_snapshot.to_dict()
            if expense.get("type") == "recurring":
                raise AlreadyRecurringError

            document = {
                "frequency": frequency,
                "start": expense["date"],
                "anchor_tz": "Europe/Rome",
                "end_date": None if end_date is None else end_date.isoformat(),
                "active": True,
                "next_index": 1,
                "resume_from": None,
                "template": {
                    field: expense[field]
                    for field in (
                        "seller",
                        "title",
                        "description",
                        "category",
                        "amount_cents",
                        "currency",
                    )
                },
                "source_expense_id": expense_id,
                "created_at": now,
                "updated_at": now,
                "deleted_at": None,
            }
            expense_updates = {
                "type": "recurring",
                "recurrence": {"rule_id": rule_id, "index": 0},
                "updated_at": now,
            }
            transaction.create(rule_reference, document)
            transaction.update(expense_reference, expense_updates)
            return (
                {"id": rule_id, **document},
                {"id": expense_id, "owner": uid, **expense, **expense_updates},
            )

        return await create_in_transaction(transaction)

    async def list(self, uid: str) -> list[dict[str, object]]:
        snapshots = (
            await self._rules(uid)
            .where(filter=FieldFilter("deleted_at", "==", None))
            .get()
        )
        return [self._rule(snapshot) for snapshot in snapshots]

    async def get(self, uid: str, rule_id: str) -> dict[str, object] | None:
        snapshot = await self._rules(uid).document(rule_id).get()
        if not snapshot.exists or snapshot.get("deleted_at") is not None:
            return None
        return self._rule(snapshot)

    async def update(
        self,
        uid: str,
        rule_id: str,
        changes: dict[str, object],
        template_changes: dict[str, object],
        now: datetime,
    ) -> dict[str, object] | None:
        reference = self._rules(uid).document(rule_id)
        transaction = self.client.transaction()

        @firestore.async_transactional
        async def update_in_transaction(transaction):
            snapshot = await reference.get(transaction=transaction)
            if not snapshot.exists or snapshot.get("deleted_at") is not None:
                return None
            rule = snapshot.to_dict()
            updates = {**changes, "updated_at": now}
            if template_changes:
                updates["template"] = {**rule["template"], **template_changes}
            if changes.get("active") is True and rule.get("active") is False:
                updates["resume_from"] = now
            transaction.update(reference, updates)
            return {"id": rule_id, **rule, **updates}

        return await update_in_transaction(transaction)

    async def deactivate(self, uid: str, rule_id: str, now: datetime) -> bool:
        reference = self._rules(uid).document(rule_id)
        transaction = self.client.transaction()

        @firestore.async_transactional
        async def deactivate_in_transaction(transaction):
            snapshot = await reference.get(transaction=transaction)
            if not snapshot.exists or snapshot.get("deleted_at") is not None:
                return False
            transaction.update(reference, {"active": False, "updated_at": now})
            return True

        return await deactivate_in_transaction(transaction)

    async def sync_rule(
        self,
        uid: str,
        rule_id: str,
        planner: SyncPlanner,
        now: datetime,
    ) -> tuple[int, bool]:
        rule_reference = self._rules(uid).document(rule_id)
        expenses = self._user(uid).collection("expenses")
        transaction = self.client.transaction()

        @firestore.async_transactional
        async def sync_in_transaction(transaction):
            rule_snapshot = await rule_reference.get(transaction=transaction)
            if (
                not rule_snapshot.exists
                or rule_snapshot.get("deleted_at") is not None
                or not rule_snapshot.get("active")
            ):
                return 0, False

            rule = self._rule(rule_snapshot)
            candidates, next_index, has_more = planner(rule)
            references = [expenses.document(expense_id) for expense_id, _ in candidates]
            existing = {}
            if references:
                # SDK bug: AsyncTransaction.get_all awaits an async generator; call the client directly.
                async for snapshot in self.client.get_all(
                    references, transaction=transaction
                ):
                    existing[snapshot.id] = snapshot.exists

            created = 0
            for (expense_id, document), reference in zip(candidates, references):
                if not existing.get(expense_id, False):
                    transaction.create(reference, document)
                    created += 1
            if next_index != rule["next_index"]:
                transaction.update(
                    rule_reference, {"next_index": next_index, "updated_at": now}
                )
            return created, has_more

        return await sync_in_transaction(transaction)


def get_rules_repository(request: Request) -> RulesRepository:
    return RulesRepository(get_firestore_client(request))
