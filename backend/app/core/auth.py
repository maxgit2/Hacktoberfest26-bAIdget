from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth as firebase_auth
from starlette.concurrency import run_in_threadpool

from app.core.errors import AppError


@dataclass(frozen=True, slots=True)
class AuthenticatedUser:
    uid: str
    email: str | None
    display_name: str | None


bearer = HTTPBearer(auto_error=False)


async def current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> AuthenticatedUser:
    if credentials is None:
        raise AppError("unauthenticated", 401, "Authentication required")

    try:
        decoded = await run_in_threadpool(
            firebase_auth.verify_id_token,
            credentials.credentials,
            check_revoked=False,
        )
        uid = decoded.get("uid")
        if not isinstance(uid, str) or not uid:
            raise ValueError("Token has no uid")
    except Exception as exc:
        raise AppError("unauthenticated", 401, "Authentication required") from exc

    email = decoded.get("email")
    display_name = decoded.get("name")
    return AuthenticatedUser(
        uid=uid,
        email=email if isinstance(email, str) else None,
        display_name=display_name if isinstance(display_name, str) else None,
    )
