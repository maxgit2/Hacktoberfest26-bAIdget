from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

from app.core.errors import AppError
from app.core.money import from_cents, to_cents
from app.models.recurring import (
    MakeRecurringRequest,
    MakeRecurringResponse,
    RecurringRuleListResponse,
    RecurringRuleResponse,
    RecurringRuleUpdate,
    RecurringSyncResponse,
)
from app.repositories.categories import CategoriesRepository
from app.repositories.rules import AlreadyRecurringError, RulesRepository, SyncPlan
from app.services.expenses import _expense_response
from app.services.recurrence import occurrence_date, occurrence_id

ROME = ZoneInfo("Europe/Rome")
RULES_PER_SYNC = 20
OCCURRENCES_PER_RULE = 50


def _not_found() -> AppError:
    return AppError("not_found", 404, "Recurring rule not found")


def _rule_response(rule: dict[str, object]) -> RecurringRuleResponse:
    template = rule["template"]
    assert isinstance(template, dict)
    amount_cents = template.get("amount_cents")
    return RecurringRuleResponse.model_validate(
        {
            **rule,
            "template": {
                **template,
                "amount": (
                    None if amount_cents is None else float(from_cents(amount_cents))  # type: ignore[arg-type]
                ),
            },
        }
    )


def _is_due(rule: dict[str, object], now: datetime) -> bool:
    start = rule["start"]
    assert isinstance(start, datetime)
    next_date = occurrence_date(
        start.astimezone(ROME),
        rule["frequency"],  # type: ignore[arg-type]
        int(rule["next_index"]),
    )
    end_date = rule.get("end_date")
    return (
        end_date is None or next_date.date() <= date.fromisoformat(str(end_date))
    ) and (next_date.astimezone(UTC) <= now)


def _plan_occurrences(rule: dict[str, object], now: datetime) -> SyncPlan:
    start = rule["start"]
    template = rule["template"]
    assert isinstance(start, datetime) and isinstance(template, dict)
    start_local = start.astimezone(ROME)
    end_date = (
        None
        if rule.get("end_date") is None
        else date.fromisoformat(str(rule["end_date"]))
    )
    resume_from = rule.get("resume_from")
    index = int(rule["next_index"])
    candidates = []

    for _ in range(OCCURRENCES_PER_RULE):
        local_date = occurrence_date(
            start_local,
            rule["frequency"],
            index,  # type: ignore[arg-type]
        )
        occurrence_utc = local_date.astimezone(UTC)
        if (
            end_date is not None and local_date.date() > end_date
        ) or occurrence_utc > now:
            return candidates, index, False

        current_index = index
        index += 1
        if isinstance(resume_from, datetime) and occurrence_utc < resume_from:
            continue
        expense_id = occurrence_id(str(rule["id"]), current_index)
        candidates.append(
            (
                expense_id,
                {
                    "date": occurrence_utc,
                    "seller": template.get("seller"),
                    "title": template.get("title"),
                    "description": template.get("description"),
                    "category": template["category"],
                    "type": "recurring",
                    "recurrence": {"rule_id": rule["id"], "index": current_index},
                    "amount_cents": template.get("amount_cents"),
                    "currency": template["currency"],
                    "source": "manual",
                    "scan_details": None,
                    "needs_review": False,
                    "created_at": now,
                    "updated_at": now,
                    "deleted_at": None,
                },
            )
        )
    return candidates, index, True


async def make_recurring(
    uid: str,
    expense_id: str,
    request: MakeRecurringRequest,
    repository: RulesRepository,
) -> MakeRecurringResponse:
    now = datetime.now(UTC)
    try:
        result = await repository.make_recurring(
            uid, expense_id, request.frequency, request.end_date, now
        )
    except AlreadyRecurringError as exc:
        raise AppError(
            "already_recurring", 409, "Expense is already recurring"
        ) from exc
    if result is None:
        raise AppError("not_found", 404, "Expense not found")
    rule, expense = result
    created, _ = await repository.sync_rule(
        uid, str(rule["id"]), lambda current: _plan_occurrences(current, now), now
    )
    return MakeRecurringResponse(
        rule=_rule_response(rule),
        expense=_expense_response(expense),
        created_occurrences=created,
    )


async def list_recurring_rules(
    uid: str, repository: RulesRepository
) -> RecurringRuleListResponse:
    rules = await repository.list(uid)
    return RecurringRuleListResponse(items=[_rule_response(rule) for rule in rules])


async def update_recurring_rule(
    uid: str,
    rule_id: str,
    request: RecurringRuleUpdate,
    repository: RulesRepository,
    categories_repository: CategoriesRepository,
) -> RecurringRuleResponse:
    if await repository.get(uid, rule_id) is None:
        raise _not_found()
    changes = request.model_dump(exclude_unset=True)
    template_changes = {
        field: changes.pop(field)
        for field in ("seller", "title", "description", "category")
        if field in changes
    }
    if (
        "category" in template_changes
        and await categories_repository.get_active_category(
            uid, str(template_changes["category"])
        )
        is None
    ):
        raise AppError("category_not_found", 422, "Category not found or archived")
    if "amount" in changes:
        amount = changes.pop("amount")
        template_changes["amount_cents"] = None if amount is None else to_cents(amount)
    if "end_date" in changes and changes["end_date"] is not None:
        changes["end_date"] = changes["end_date"].isoformat()  # type: ignore[union-attr]

    updated = await repository.update(
        uid, rule_id, changes, template_changes, datetime.now(UTC)
    )
    if updated is None:
        raise _not_found()
    return _rule_response(updated)


async def delete_recurring_rule(
    uid: str, rule_id: str, repository: RulesRepository
) -> None:
    if not await repository.deactivate(uid, rule_id, datetime.now(UTC)):
        raise _not_found()


async def sync_recurring_rules(
    uid: str, repository: RulesRepository
) -> RecurringSyncResponse:
    now = datetime.now(UTC)
    active = sorted(
        (rule for rule in await repository.list(uid) if rule.get("active")),
        key=lambda rule: str(rule["id"]),
    )
    due = [rule for rule in active if _is_due(rule, now)]
    due_ids = {rule["id"] for rule in due}
    selected = (due + [rule for rule in active if rule["id"] not in due_ids])[
        :RULES_PER_SYNC
    ]

    created = 0
    has_more = len(active) > RULES_PER_SYNC
    for rule in selected:
        rule_created, rule_has_more = await repository.sync_rule(
            uid,
            str(rule["id"]),
            lambda current, now=now: _plan_occurrences(current, now),
            now,
        )
        created += rule_created
        has_more = has_more or rule_has_more
    return RecurringSyncResponse(
        created=created, rules_processed=len(selected), has_more=has_more
    )
