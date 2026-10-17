from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query, Response, status

from app.core.auth import AuthenticatedUser, current_user
from app.models.expense import (
    ExpenseCreate,
    ExpenseListResponse,
    ExpenseResponse,
    ExpenseUpdate,
)
from app.repositories.categories import (
    CategoriesRepository,
    get_categories_repository,
)
from app.repositories.expenses import ExpensesRepository, get_expenses_repository
from app.services.expenses import (
    create_expense,
    delete_expense,
    get_expense,
    list_expenses,
    update_expense,
)

router = APIRouter(prefix="/v1/expenses", tags=["expenses"])


@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="createExpense",
)
async def create(
    request: ExpenseCreate,
    response: Response,
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[ExpensesRepository, Depends(get_expenses_repository)],
    categories_repository: Annotated[
        CategoriesRepository, Depends(get_categories_repository)
    ],
) -> ExpenseResponse:
    expense, created = await create_expense(
        user.uid, request, repository, categories_repository
    )
    response.status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return expense


@router.get("", response_model=ExpenseListResponse, operation_id="listExpenses")
async def list_(
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[ExpensesRepository, Depends(get_expenses_repository)],
    from_: Annotated[datetime | None, Query(alias="from")] = None,
    to: datetime | None = None,
    category: str | None = None,
    type_: Annotated[Literal["single", "recurring"] | None, Query(alias="type")] = None,
    needs_review: bool | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    cursor: str | None = None,
) -> ExpenseListResponse:
    return await list_expenses(
        user.uid,
        repository,
        from_=from_,
        to=to,
        category=category,
        type_=type_,
        needs_review=needs_review,
        limit=limit,
        cursor=cursor,
    )


@router.get("/{expense_id}", response_model=ExpenseResponse, operation_id="getExpense")
async def get(
    expense_id: str,
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[ExpensesRepository, Depends(get_expenses_repository)],
) -> ExpenseResponse:
    return await get_expense(user.uid, expense_id, repository)


@router.patch(
    "/{expense_id}", response_model=ExpenseResponse, operation_id="updateExpense"
)
async def update(
    expense_id: str,
    request: ExpenseUpdate,
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[ExpensesRepository, Depends(get_expenses_repository)],
    categories_repository: Annotated[
        CategoriesRepository, Depends(get_categories_repository)
    ],
) -> ExpenseResponse:
    return await update_expense(
        user.uid, expense_id, request, repository, categories_repository
    )


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="deleteExpense",
)
async def delete(
    expense_id: str,
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[ExpensesRepository, Depends(get_expenses_repository)],
) -> Response:
    await delete_expense(user.uid, expense_id, repository)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
