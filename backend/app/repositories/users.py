from datetime import UTC, datetime

from fastapi import Request
from google.cloud import firestore
from google.cloud.firestore import AsyncClient

from app.core.auth import AuthenticatedUser
from app.repositories.client import get_firestore_client


class UsersRepository:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    async def get_or_create(self, user: AuthenticatedUser) -> dict[str, object]:
        reference = self.client.collection("users").document(user.uid)
        transaction = self.client.transaction()

        @firestore.async_transactional
        async def get_or_create_in_transaction(transaction):
            snapshot = await reference.get(transaction=transaction)
            if snapshot.exists:
                return snapshot.to_dict()

            now = datetime.now(UTC)
            profile = {
                "email": user.email,
                "display_name": user.display_name,
                "onboarding_completed": False,
                "created_at": now,
                "updated_at": now,
            }
            transaction.set(reference, profile)
            return profile

        return await get_or_create_in_transaction(transaction)


def get_users_repository(request: Request) -> UsersRepository:
    return UsersRepository(get_firestore_client(request))
