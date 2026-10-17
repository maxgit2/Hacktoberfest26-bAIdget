from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.core.auth import AuthenticatedUser, current_user
from app.models.recurring import (
    MakeRecurringRequest,
    MakeRecurringResponse,
    RecurringRuleListResponse,
    RecurringRuleResponse,
    RecurringRuleUpdate,
    RecurringSyncResponse,
)
from app.repositories.categories import CategoriesRepository, get_categories_repository
from app.repositories.rules import RulesRepository, get_rules_repository
from app.services.recurring import (
    delete_recurring_rule,
    list_recurring_rules,
    make_recurring,
    sync_recurring_rules,
    update_recurring_rule,
)

router = APIRouter(tags=["recurring"])


@router.post(
    "/v1/expenses/{expense_id}/make-recurring",
    response_model=MakeRecurringResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="makeExpenseRecurring",
)
async def create(
    expense_id: str,
    request: MakeRecurringRequest,
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[RulesRepository, Depends(get_rules_repository)],
) -> MakeRecurringResponse:
    return await make_recurring(user.uid, expense_id, request, repository)


@router.get(
    "/v1/recurring-rules",
    response_model=RecurringRuleListResponse,
    operation_id="listRecurringRules",
)
async def list_(
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[RulesRepository, Depends(get_rules_repository)],
) -> RecurringRuleListResponse:
    return await list_recurring_rules(user.uid, repository)


@router.patch(
    "/v1/recurring-rules/{rule_id}",
    response_model=RecurringRuleResponse,
    operation_id="updateRecurringRule",
)
async def update(
    rule_id: str,
    request: RecurringRuleUpdate,
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[RulesRepository, Depends(get_rules_repository)],
    categories_repository: Annotated[
        CategoriesRepository, Depends(get_categories_repository)
    ],
) -> RecurringRuleResponse:
    return await update_recurring_rule(
        user.uid, rule_id, request, repository, categories_repository
    )


@router.delete(
    "/v1/recurring-rules/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="deleteRecurringRule",
)
async def delete(
    rule_id: str,
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[RulesRepository, Depends(get_rules_repository)],
) -> Response:
    await delete_recurring_rule(user.uid, rule_id, repository)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/v1/recurring-rules/sync",
    response_model=RecurringSyncResponse,
    operation_id="syncRecurringRules",
)
async def sync(
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    repository: Annotated[RulesRepository, Depends(get_rules_repository)],
) -> RecurringSyncResponse:
    return await sync_recurring_rules(user.uid, repository)
