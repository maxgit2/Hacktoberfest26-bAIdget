from app.core.auth import AuthenticatedUser
from app.models.user import UserResponse
from app.repositories.users import UsersRepository


async def get_or_create_user(
    user: AuthenticatedUser, repository: UsersRepository
) -> UserResponse:
    profile = await repository.get_or_create(user)
    return UserResponse.model_validate({"uid": user.uid, **profile})
