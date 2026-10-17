from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Response, UploadFile, status
from fastapi.responses import JSONResponse
from pydantic import UUID4

from app.core.auth import AuthenticatedUser, current_user
from app.core.config import Settings, get_settings
from app.models.expense import ExpenseResponse
from app.repositories.categories import (
    CategoriesRepository,
    get_categories_repository,
)
from app.repositories.expenses import ExpensesRepository, get_expenses_repository
from app.repositories.rate_limit import (
    RateLimitExceeded,
    ScanRateLimitRepository,
    get_scan_rate_limit_repository,
)
from app.services.scan import scan_expense

router = APIRouter(prefix="/v1/expenses", tags=["expenses"])


@router.post(
    "/scan",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="scanExpense",
)
async def scan(
    response: Response,
    image: Annotated[UploadFile, File()],
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    expenses: Annotated[ExpensesRepository, Depends(get_expenses_repository)],
    categories: Annotated[CategoriesRepository, Depends(get_categories_repository)],
    rate_limit: Annotated[
        ScanRateLimitRepository, Depends(get_scan_rate_limit_repository)
    ],
    settings: Annotated[Settings, Depends(get_settings)],
    id: Annotated[UUID4 | None, Form()] = None,
) -> ExpenseResponse | JSONResponse:
    try:
        expense, created = await scan_expense(
            user.uid,
            image,
            id,
            expenses,
            categories,
            rate_limit,
            settings,
        )
    except RateLimitExceeded as exc:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            headers={"Retry-After": str(exc.retry_after)},
            content={
                "error": {
                    "code": "rate_limited",
                    "message": "Too many scans",
                    "details": {},
                }
            },
        )
    response.status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return expense
