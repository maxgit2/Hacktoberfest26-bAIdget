from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.auth import AuthenticatedUser, current_user
from app.models.errors import error_responses
from app.models.user import UserResponse
from app.repositories.users import UsersRepository, get_users_repository
from app.services.users import get_or_create_user

router = APIRouter(prefix="/v1", tags=["user"])


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    operation_id="getCurrentUser",
    responses=error_responses("unauthenticated", "internal_error"),
)
async def read_me(
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[UsersRepository, Depends(get_users_repository)],
) -> UserResponse:
    return await get_or_create_user(user, repository)
