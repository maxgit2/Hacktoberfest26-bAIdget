from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.core.auth import AuthenticatedUser, current_user
from app.models.category import (
    CatalogResponse,
    CategoryCreate,
    CategoryListResponse,
    CategoryResponse,
    CategoryUpdate,
    OnboardingRequest,
    OnboardingResponse,
)
from app.models.errors import error_responses
from app.repositories.categories import (
    CategoriesRepository,
    get_categories_repository,
)
from app.repositories.users import UsersRepository, get_users_repository
from app.services.catalog import get_catalog
from app.services.categories import (
    create_category,
    delete_category,
    list_categories,
    onboard_categories,
    update_category,
)

router = APIRouter(prefix="/v1/categories", tags=["categories"])


@router.get(
    "/catalog",
    response_model=CatalogResponse,
    status_code=status.HTTP_200_OK,
    operation_id="getCategoryCatalog",
    responses=error_responses("unauthenticated", "internal_error"),
)
async def category_catalog(
    _user: Annotated[AuthenticatedUser, Depends(current_user)],
) -> CatalogResponse:
    return get_catalog()


@router.post(
    "/onboarding",
    response_model=OnboardingResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="onboardCategories",
    responses=error_responses(
        "unauthenticated",
        "already_onboarded",
        "category_name_taken",
        "validation_error",
        "min_categories",
        "max_categories",
        "internal_error",
    ),
)
async def onboarding(
    request: OnboardingRequest,
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[CategoriesRepository, Depends(get_categories_repository)],
    users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
) -> OnboardingResponse:
    return await onboard_categories(user, request, repository, users_repository)


@router.get(
    "",
    response_model=CategoryListResponse,
    status_code=status.HTTP_200_OK,
    operation_id="listCategories",
    responses=error_responses("unauthenticated", "internal_error"),
)
async def categories(
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[CategoriesRepository, Depends(get_categories_repository)],
) -> CategoryListResponse:
    return await list_categories(user.uid, repository)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="createCategory",
    responses=error_responses(
        "unauthenticated",
        "category_name_taken",
        "validation_error",
        "max_categories",
        "internal_error",
    ),
)
async def create(
    request: CategoryCreate,
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[CategoriesRepository, Depends(get_categories_repository)],
) -> CategoryResponse:
    return await create_category(user.uid, request, repository)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    operation_id="updateCategory",
    responses=error_responses(
        "unauthenticated",
        "not_found",
        "category_name_taken",
        "validation_error",
        "internal_error",
    ),
)
async def update(
    category_id: str,
    request: CategoryUpdate,
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[CategoriesRepository, Depends(get_categories_repository)],
) -> CategoryResponse:
    return await update_category(user.uid, category_id, request, repository)


@router.delete(
    "/{category_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="deleteCategory",
    responses=error_responses(
        "unauthenticated",
        "not_found",
        "category_in_use",
        "cannot_modify_other",
        "validation_error",
        "internal_error",
    ),
)
async def delete(
    category_id: str,
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[CategoriesRepository, Depends(get_categories_repository)],
) -> Response:
    await delete_category(user.uid, category_id, repository)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
