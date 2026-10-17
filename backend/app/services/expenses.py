import base64
import binascii
import json
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.core.errors import AppError
from app.core.money import from_cents, to_cents
from app.core.time import parse_datetime, to_z
from app.models.expense import (
    ExpenseCreate,
    ExpenseListResponse,
    ExpenseResponse,
    ExpenseUpdate,
)
from app.repositories.categories import CategoriesRepository
from app.repositories.expenses import ExpensesRepository


def _not_found() -> AppError:
    return AppError("not_found", 404, "Expense not found")


def _category_not_found() -> AppError:
    return AppError("category_not_found", 422, "Category not found or archived")


def _expense_response(expense: dict[str, object]) -> ExpenseResponse:
    recurrence = expense.get("recurrence")
    return ExpenseResponse.model_validate(
        {
            **expense,
            "recurrence": (
                {"rule_id": recurrence["rule_id"]}
                if isinstance(recurrence, dict)
                else None
            ),
            "amount": (
                None
                if expense.get("amount_cents") is None
                else float(from_cents(expense["amount_cents"]))  # type: ignore[arg-type]
            ),
        }
    )


async def _validate_category(
    uid: str, category_id: str, repository: CategoriesRepository
) -> None:
    if await repository.get_active_category(uid, category_id) is None:
        raise _category_not_found()


def _cursor_error() -> AppError:
    return AppError(
        "validation_error",
        422,
        "Invalid pagination cursor",
        {"fields": [{"field": "cursor", "message": "Invalid cursor"}]},
    )


def _decode_cursor(cursor: str | None) -> tuple[datetime, str] | None:
    if cursor is None:
        return None
    try:
        decoded = json.loads(
            base64.b64decode(cursor, altchars=b"-_", validate=True).decode("utf-8")
        )
        if set(decoded) != {"date", "id"} or not isinstance(decoded["id"], str):
            raise ValueError
        UUID(decoded["id"])
        return parse_datetime(decoded["date"]), decoded["id"]
    except (
        binascii.Error,
        UnicodeDecodeError,
        json.JSONDecodeError,
        TypeError,
        ValueError,
    ):
        raise _cursor_error() from None


def _encode_cursor(expense: dict[str, object]) -> str:
    payload = json.dumps(
        {"date": to_z(expense["date"]), "id": expense["id"]},  # type: ignore[arg-type]
        separators=(",", ":"),
    ).encode()
    return base64.urlsafe_b64encode(payload).decode()


async def create_expense(
    uid: str,
    request: ExpenseCreate,
    repository: ExpensesRepository,
    categories_repository: CategoriesRepository,
) -> tuple[ExpenseResponse, bool]:
    await _validate_category(uid, request.category, categories_repository)
    now = datetime.now(UTC)
    expense = {
        "id": str(request.id or uuid4()),
        "date": request.date,
        "seller": request.seller,
        "title": request.title,
        "description": request.description,
        "category": request.category,
        "type": "single",
        "recurrence": None,
        "amount_cents": None if request.amount is None else to_cents(request.amount),
        "currency": request.currency,
        "source": "manual",
        "scan_details": None,
        "needs_review": False,
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }
    stored, created = await repository.create_idempotent(uid, expense)
    if not created and stored.get("deleted_at") is not None:
        raise _not_found()
    return _expense_response(stored), created


async def get_expense(
    uid: str, expense_id: str, repository: ExpensesRepository
) -> ExpenseResponse:
    expense = await repository.get(uid, expense_id)
    if expense is None:
        raise _not_found()
    return _expense_response(expense)


async def list_expenses(
    uid: str,
    repository: ExpensesRepository,
    *,
    from_: datetime | None,
    to: datetime | None,
    category: str | None,
    type_: str | None,
    needs_review: bool | None,
    limit: int,
    cursor: str | None,
) -> ExpenseListResponse:
    filters: dict[str, object] = {}
    for field, value in (("from", from_), ("to", to)):
        if value is not None:
            try:
                filters[field] = parse_datetime(value)
            except ValueError:
                raise AppError(
                    "validation_error",
                    422,
                    "Datetime filters must include a UTC offset",
                    {"fields": [{"field": field, "message": "UTC offset required"}]},
                ) from None
    if category is not None:
        filters["category"] = category
    if type_ is not None:
        filters["type"] = type_
    if needs_review is not None:
        filters["needs_review"] = needs_review

    expenses, has_more = await repository.list(
        uid, filters, limit, _decode_cursor(cursor)
    )
    return ExpenseListResponse(
        items=[_expense_response(expense) for expense in expenses],
        next_cursor=_encode_cursor(expenses[-1]) if has_more else None,
    )


async def update_expense(
    uid: str,
    expense_id: str,
    request: ExpenseUpdate,
    repository: ExpensesRepository,
    categories_repository: CategoriesRepository,
) -> ExpenseResponse:
    changes = request.model_dump(exclude_unset=True)
    if "category" in changes:
        if await repository.get(uid, expense_id) is None:
            raise _not_found()
        await _validate_category(uid, changes["category"], categories_repository)
    if "amount" in changes:
        amount = changes.pop("amount")
        changes["amount_cents"] = None if amount is None else to_cents(amount)
    updated = await repository.update(uid, expense_id, changes)
    if updated is None:
        raise _not_found()
    return _expense_response(updated)


async def delete_expense(
    uid: str, expense_id: str, repository: ExpensesRepository
) -> None:
    if not await repository.soft_delete(uid, expense_id):
        raise _not_found()
