from datetime import UTC, datetime
from uuid import uuid4

from fastapi import Request
from google.cloud import firestore
from google.cloud.firestore import AsyncClient
from google.cloud.firestore_v1.base_query import FieldFilter

from app.repositories.client import get_firestore_client


class AlreadyOnboardedError(Exception):
    pass


class CategoryLimitError(Exception):
    pass


class CategoryNameTakenError(Exception):
    pass


class CannotModifyOtherError(Exception):
    pass


class CategoryInUseError(Exception):
    pass


class CategoriesRepository:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    def _categories(self, uid: str):
        return self.client.collection("users").document(uid).collection("categories")

    def _active_query(self, uid: str):
        return self._categories(uid).where(
            filter=FieldFilter("archived_at", "==", None)
        )

    @staticmethod
    def _category(snapshot) -> dict[str, object]:
        return {"id": snapshot.id, **snapshot.to_dict()}

    async def list_active(self, uid: str) -> list[dict[str, object]]:
        snapshots = await self._active_query(uid).get()
        return [self._category(snapshot) for snapshot in snapshots]

    async def get_active_category(
        self, uid: str, category_id: str
    ) -> dict[str, object] | None:
        snapshot = await self._categories(uid).document(category_id).get()
        if not snapshot.exists or snapshot.get("archived_at") is not None:
            return None
        return self._category(snapshot)

    async def onboard(
        self, uid: str, categories: list[dict[str, object]]
    ) -> list[dict[str, object]]:
        user_reference = self.client.collection("users").document(uid)
        transaction = self.client.transaction()

        @firestore.async_transactional
        async def onboard_in_transaction(transaction):
            user = await user_reference.get(transaction=transaction)
            existing = await self._active_query(uid).get(transaction=transaction)
            if user.exists and user.get("onboarding_completed"):
                raise AlreadyOnboardedError
            if len(existing) + len(categories) > 30:
                raise CategoryLimitError

            existing_keys = {snapshot.get("name_key") for snapshot in existing}
            if existing_keys.intersection(
                category["name_key"] for category in categories
            ):
                raise CategoryNameTakenError

            now = datetime.now(UTC)
            created = []
            for category in categories:
                category_id = f"cat_{uuid4().hex[:8]}"
                document = {
                    **category,
                    "archived_at": None,
                    "created_at": now,
                    "updated_at": now,
                }
                transaction.set(self._categories(uid).document(category_id), document)
                created.append({"id": category_id, **document})

            transaction.set(
                user_reference,
                {"onboarding_completed": True, "updated_at": now},
                merge=True,
            )
            return [self._category(snapshot) for snapshot in existing] + created

        return await onboard_in_transaction(transaction)

    async def create(self, uid: str, category: dict[str, object]) -> dict[str, object]:
        transaction = self.client.transaction()

        @firestore.async_transactional
        async def create_in_transaction(transaction):
            existing = await self._active_query(uid).get(transaction=transaction)
            if len(existing) >= 30:
                raise CategoryLimitError
            if any(
                snapshot.get("name_key") == category["name_key"]
                for snapshot in existing
            ):
                raise CategoryNameTakenError

            now = datetime.now(UTC)
            category_id = f"cat_{uuid4().hex[:8]}"
            document = {
                **category,
                "archived_at": None,
                "created_at": now,
                "updated_at": now,
            }
            transaction.set(self._categories(uid).document(category_id), document)
            return {"id": category_id, **document}

        return await create_in_transaction(transaction)

    async def update(
        self, uid: str, category_id: str, changes: dict[str, object]
    ) -> dict[str, object] | None:
        reference = self._categories(uid).document(category_id)
        transaction = self.client.transaction()

        @firestore.async_transactional
        async def update_in_transaction(transaction):
            snapshot = await reference.get(transaction=transaction)
            if not snapshot.exists or snapshot.get("archived_at") is not None:
                return None

            if "name_key" in changes:
                existing = await self._active_query(uid).get(transaction=transaction)
                if any(
                    other.id != category_id
                    and other.get("name_key") == changes["name_key"]
                    for other in existing
                ):
                    raise CategoryNameTakenError

            updates = {**changes, "updated_at": datetime.now(UTC)}
            transaction.update(reference, updates)
            return {"id": category_id, **snapshot.to_dict(), **updates}

        return await update_in_transaction(transaction)

    def _usage_queries(self, uid: str, category_id: str):
        user = self.client.collection("users").document(uid)
        expenses = (
            user.collection("expenses")
            .where(filter=FieldFilter("deleted_at", "==", None))
            .where(filter=FieldFilter("category", "==", category_id))
            .limit(1)
        )
        rules = (
            user.collection("recurring_rules")
            .where(filter=FieldFilter("active", "==", True))
            .where(filter=FieldFilter("template.category", "==", category_id))
            .limit(1)
        )
        return expenses, rules

    async def is_category_in_use(self, uid: str, category_id: str) -> bool:
        for query in self._usage_queries(uid, category_id):
            if await query.get():
                return True
        return False

    async def archive(self, uid: str, category_id: str) -> bool:
        reference = self._categories(uid).document(category_id)
        transaction = self.client.transaction()

        @firestore.async_transactional
        async def archive_in_transaction(transaction):
            snapshot = await reference.get(transaction=transaction)
            if not snapshot.exists or snapshot.get("archived_at") is not None:
                return False
            if snapshot.get("is_other"):
                raise CannotModifyOtherError

            for query in self._usage_queries(uid, category_id):
                if await query.get(transaction=transaction):
                    raise CategoryInUseError

            now = datetime.now(UTC)
            transaction.update(reference, {"archived_at": now, "updated_at": now})
            return True

        return await archive_in_transaction(transaction)


def get_categories_repository(request: Request) -> CategoriesRepository:
    return CategoriesRepository(get_firestore_client(request))
