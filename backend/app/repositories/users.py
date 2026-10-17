import asyncio
import random
from datetime import UTC, datetime

from fastapi import Request
from google.api_core.exceptions import Aborted
from google.cloud import firestore
from google.cloud.firestore import AsyncClient

from app.core.auth import AuthenticatedUser
from app.repositories.client import get_firestore_client


class UsersRepository:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    async def get_or_create(self, user: AuthenticatedUser) -> dict[str, object]:
        reference = self.client.collection("users").document(user.uid)

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

        try:
            return await get_or_create_in_transaction(self.client.transaction())
        except ValueError as exc:
            if not isinstance(exc.__cause__, Aborted):
                raise

        # The SDK exhausts five commit attempts as ValueError caused by Aborted.
        # Retry that contention once, with jitter: at most ten commit attempts
        # and 250 ms of added delay. RPC deadlines still bound each SDK call.
        await asyncio.sleep(random.uniform(0.05, 0.25))
        return await get_or_create_in_transaction(self.client.transaction())


def get_users_repository(request: Request) -> UsersRepository:
    return UsersRepository(get_firestore_client(request))
