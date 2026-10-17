import math
from datetime import UTC, datetime, timedelta

from fastapi import Request
from google.cloud import firestore
from google.cloud.firestore import AsyncClient

from app.repositories.client import get_firestore_client


class RateLimitExceeded(Exception):
    def __init__(self, retry_after: int) -> None:
        self.retry_after = retry_after


class ScanRateLimitRepository:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    async def consume(self, uid: str, limit: int) -> None:
        now = datetime.now(UTC)
        window_start = now.replace(minute=0, second=0, microsecond=0)
        retry_after = max(
            1, math.ceil(((window_start + timedelta(hours=1)) - now).total_seconds())
        )
        reference = (
            self.client.collection("users")
            .document(uid)
            .collection("meta")
            .document("scan_rate")
        )
        transaction = self.client.transaction()

        @firestore.async_transactional
        async def consume_in_transaction(transaction):
            snapshot = await reference.get(transaction=transaction)
            count = (
                snapshot.get("count")
                if snapshot.exists and snapshot.get("window_start") == window_start
                else 0
            )
            if count >= limit:
                raise RateLimitExceeded(retry_after)
            transaction.set(
                reference,
                {"window_start": window_start, "count": count + 1},
            )

        await consume_in_transaction(transaction)


def get_scan_rate_limit_repository(request: Request) -> ScanRateLimitRepository:
    return ScanRateLimitRepository(get_firestore_client(request))
