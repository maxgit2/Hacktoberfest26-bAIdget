from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import firebase_admin
from fastapi import FastAPI, Request
from google.cloud.firestore import AsyncClient

from app.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(
            options={"projectId": settings.google_cloud_project}
        )

    app.state.firestore = AsyncClient(project=settings.google_cloud_project)
    try:
        yield
    finally:
        app.state.firestore.close()  # sync in google-cloud-firestore AsyncClient


def get_firestore_client(request: Request) -> AsyncClient:
    return request.app.state.firestore
