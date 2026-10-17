from app.core.auth import AuthenticatedUser
from app.core.errors import AppError
from app.models.category import (
    CategoryCreate,
    CategoryListResponse,
    CategoryResponse,
    CategoryUpdate,
    OnboardingRequest,
    OnboardingResponse,
)
from app.repositories.categories import (
    AlreadyOnboardedError,
    CannotModifyOtherError,
    CategoriesRepository,
    CategoryInUseError,
    CategoryLimitError,
    CategoryNameTakenError,
)
from app.repositories.users import UsersRepository
from app.services.catalog import CATALOG_BY_ID
from app.services.users import get_or_create_user


def _name_key(name: str) -> str:
    return name.casefold()


def _category_response(category: dict[str, object]) -> CategoryResponse:
    return CategoryResponse.model_validate(category)


def _name_taken() -> AppError:
    return AppError(
        "category_name_taken", 409, "An active category already has this name"
    )


def _max_categories() -> AppError:
    return AppError("max_categories", 422, "A maximum of 30 categories is allowed")


async def onboard_categories(
    user: AuthenticatedUser,
    request: OnboardingRequest,
    repository: CategoriesRepository,
    users_repository: UsersRepository,
) -> OnboardingResponse:
    selected = []
    for catalog_id in request.catalog_ids:
        item = CATALOG_BY_ID.get(catalog_id)
        if item is None:
            raise AppError(
                "validation_error",
                422,
                "Unknown catalog category",
                {"fields": [{"field": "catalog_ids", "message": catalog_id}]},
            )
        selected.append(
            {
                "name": item.name,
                "name_key": _name_key(item.name),
                "icon": item.icon,
                "color": None,
                "catalog_id": item.id,
                "is_other": False,
            }
        )

    selected.extend(
        {
            **category.model_dump(),
            "name_key": _name_key(category.name),
            "catalog_id": None,
            "is_other": False,
        }
        for category in request.custom
    )
    if len(selected) < 2:
        raise AppError("min_categories", 422, "Choose at least two categories")

    selected.append(
        {
            "name": "Other",
            "name_key": "other",
            "icon": None,
            "color": None,
            "catalog_id": None,
            "is_other": True,
        }
    )
    if len(selected) > 30:
        raise _max_categories()
    if len({_name_key(str(category["name"])) for category in selected}) != len(
        selected
    ):
        raise _name_taken()

    await get_or_create_user(user, users_repository)
    try:
        categories = await repository.onboard(user.uid, selected)
    except AlreadyOnboardedError as exc:
        raise AppError(
            "already_onboarded", 409, "Onboarding is already complete"
        ) from exc
    except CategoryLimitError as exc:
        raise _max_categories() from exc
    except CategoryNameTakenError as exc:
        raise _name_taken() from exc
    return OnboardingResponse(
        categories=[_category_response(category) for category in categories]
    )


async def list_categories(
    uid: str, repository: CategoriesRepository
) -> CategoryListResponse:
    categories = await repository.list_active(uid)
    return CategoryListResponse(
        items=[_category_response(category) for category in categories]
    )


async def create_category(
    uid: str, request: CategoryCreate, repository: CategoriesRepository
) -> CategoryResponse:
    category = {
        **request.model_dump(),
        "name_key": _name_key(request.name),
        "catalog_id": None,
        "is_other": False,
    }
    try:
        created = await repository.create(uid, category)
    except CategoryLimitError as exc:
        raise _max_categories() from exc
    except CategoryNameTakenError as exc:
        raise _name_taken() from exc
    return _category_response(created)


async def update_category(
    uid: str,
    category_id: str,
    request: CategoryUpdate,
    repository: CategoriesRepository,
) -> CategoryResponse:
    changes = request.model_dump(exclude_unset=True)
    if "name" in changes:
        changes["name_key"] = _name_key(str(changes["name"]))
    try:
        updated = await repository.update(uid, category_id, changes)
    except CategoryNameTakenError as exc:
        raise _name_taken() from exc
    if updated is None:
        raise AppError("not_found", 404, "Category not found")
    return _category_response(updated)


async def delete_category(
    uid: str, category_id: str, repository: CategoriesRepository
) -> None:
    try:
        archived = await repository.archive(uid, category_id)
    except CannotModifyOtherError as exc:
        raise AppError(
            "cannot_modify_other", 409, "The Other category cannot be deleted"
        ) from exc
    except CategoryInUseError as exc:
        raise AppError(
            "category_in_use", 409, "The category is currently in use"
        ) from exc
    if not archived:
        raise AppError("not_found", 404, "Category not found")
