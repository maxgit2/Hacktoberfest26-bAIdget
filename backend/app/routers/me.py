from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.auth import AuthenticatedUser, current_user
from app.models.user import UserResponse
from app.repositories.users import UsersRepository, get_users_repository
from app.services.users import get_or_create_user

router = APIRouter(prefix="/v1", tags=["user"])


@router.get("/me", response_model=UserResponse)
async def read_me(
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[UsersRepository, Depends(get_users_repository)],
) -> UserResponse:
    return await get_or_create_user(user, repository)
