from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core.auth import AuthenticatedUser, current_user
from app.core.config import Settings, get_settings
from app.models.errors import error_responses
from app.models.summary import MonthlySummaryResponse, YearlySummaryResponse
from app.repositories.categories import (
    CategoriesRepository,
    get_categories_repository,
)
from app.repositories.expenses import ExpensesRepository, get_expenses_repository
from app.services.summary import monthly_summary, yearly_summary

router = APIRouter(prefix="/v1/summary", tags=["summary"])


@router.get(
    "/monthly",
    response_model=MonthlySummaryResponse,
    status_code=status.HTTP_200_OK,
    operation_id="getMonthlySummary",
    responses=error_responses("unauthenticated", "validation_error", "internal_error"),
)
async def monthly(
    month: Annotated[str, Query(pattern=r"^\d{4}-\d{2}$")],
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    settings: Annotated[Settings, Depends(get_settings)],
    expenses_repository: Annotated[
        ExpensesRepository, Depends(get_expenses_repository)
    ],
    categories_repository: Annotated[
        CategoriesRepository, Depends(get_categories_repository)
    ],
) -> MonthlySummaryResponse:
    return await monthly_summary(
        user.uid,
        month,
        settings,
        expenses_repository,
        categories_repository,
    )


@router.get(
    "/yearly",
    response_model=YearlySummaryResponse,
    status_code=status.HTTP_200_OK,
    operation_id="getYearlySummary",
    responses=error_responses("unauthenticated", "validation_error", "internal_error"),
)
async def yearly(
    year: Annotated[str, Query(pattern=r"^\d{4}$")],
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    settings: Annotated[Settings, Depends(get_settings)],
    expenses_repository: Annotated[
        ExpensesRepository, Depends(get_expenses_repository)
    ],
    categories_repository: Annotated[
        CategoriesRepository, Depends(get_categories_repository)
    ],
) -> YearlySummaryResponse:
    return await yearly_summary(
        user.uid,
        year,
        settings,
        expenses_repository,
        categories_repository,
    )
