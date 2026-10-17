from datetime import UTC, datetime
from typing import Protocol
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from app.core.config import Settings
from app.core.errors import AppError
from app.core.money import from_cents, parse_amount, to_cents
from app.imaging.image import UnsupportedImageTypeError, prepare_image
from app.llm import gemini
from app.llm.schema import ExtractionItem, ExtractionModel
from app.models.expense import ExpenseResponse
from app.repositories.categories import CategoriesRepository
from app.repositories.expenses import ExpensesRepository
from app.repositories.rate_limit import ScanRateLimitRepository
from app.services.expenses import _expense_response


class ImageStream(Protocol):
    async def read(self, size: int = -1) -> bytes: ...


async def _read_image(image: ImageStream, maximum: int) -> bytes:
    content = bytearray()
    while chunk := await image.read(64 * 1024):
        if len(content) + len(chunk) > maximum:
            raise AppError("image_too_large", 413, "Image exceeds the size limit")
        content.extend(chunk)
    return bytes(content)


def _text(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _cents(value: str | None) -> tuple[int | None, bool]:
    if value is None:
        return None, False
    try:
        return to_cents(parse_amount(value)), False
    except ValueError:
        return None, True


def _quantity(value: str | None) -> tuple[int | float | None, bool]:
    if value is None:
        return None, False
    try:
        quantity = parse_amount(value)
    except ValueError:
        return None, True
    return (
        int(quantity) if quantity == quantity.to_integral() else float(quantity),
        False,
    )


def _date(
    value: str | None, reliable: bool, timezone: str, now: datetime
) -> tuple[datetime, bool]:
    if value is None:
        return now, True
    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=ZoneInfo(timezone))
        return parsed.astimezone(UTC), not reliable
    except (TypeError, ValueError):
        return now, True


def _item(item: ExtractionItem) -> tuple[dict[str, object], bool]:
    quantity, bad_quantity = _quantity(item.quantity)
    unit_price_cents, bad_unit_price = _cents(item.unit_price)
    total_cents, bad_total = _cents(item.total)
    return (
        {
            "description": _text(item.description),
            "quantity": quantity,
            "unit_price_cents": unit_price_cents,
            "total_cents": total_cents,
        },
        bad_quantity or bad_unit_price or bad_total,
    )


def _amount(cents: object) -> float | None:
    return None if cents is None else float(from_cents(cents))  # type: ignore[arg-type]


def _scan_response(expense: dict[str, object]) -> ExpenseResponse:
    details = expense.get("scan_details")
    if not isinstance(details, dict):
        return _expense_response(expense)
    items = details.get("items")
    api_details = {
        "document_type": details.get("document_type"),
        "items": [
            {
                "description": item.get("description"),
                "quantity": item.get("quantity"),
                "unit_price": _amount(item.get("unit_price_cents")),
                "total": _amount(item.get("total_cents")),
            }
            for item in items
        ]
        if isinstance(items, list)
        else [],
        "vat_total": _amount(details.get("vat_total_cents")),
        "vat_number": details.get("vat_number"),
        "payment_method": details.get("payment_method"),
    }
    return _expense_response({**expense, "scan_details": api_details})


def _expense_from_extraction(
    expense_id: str,
    extraction: ExtractionModel,
    category_id: str,
    settings: Settings,
) -> dict[str, object]:
    now = datetime.now(UTC)
    seller = _text(extraction.seller)
    total_cents, bad_total = _cents(extraction.total)
    if seller is None and total_cents is None:
        raise AppError("extraction_failed", 422, "Expense extraction failed")

    date, needs_review = _date(
        extraction.date, extraction.date_reliable, settings.tz_name, now
    )
    needs_review = needs_review or total_cents is None or bad_total
    items = []
    for extracted_item in extraction.items:
        item, bad_item = _item(extracted_item)
        items.append(item)
        needs_review = needs_review or bad_item

    if items and total_cents is not None:
        item_totals = [item["total_cents"] for item in items]
        if any(total is None for total in item_totals) or abs(
            sum(total for total in item_totals if isinstance(total, int)) - total_cents
        ) > len(items):
            needs_review = True

    vat_total_cents, bad_vat = _cents(extraction.vat_total)
    needs_review = needs_review or bad_vat
    return {
        "id": expense_id,
        "date": date,
        "seller": seller,
        "title": seller,
        "description": None,
        "category": category_id,
        "type": "single",
        "recurrence": None,
        "amount_cents": total_cents,
        "currency": "EUR",
        "source": "scan",
        "scan_details": {
            "document_type": extraction.document_type,
            "items": items,
            "vat_total_cents": vat_total_cents,
            "vat_number": _text(extraction.vat_number),
            "payment_method": _text(extraction.payment_method),
        },
        "needs_review": needs_review,
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }


async def scan_expense(
    uid: str,
    image: ImageStream,
    expense_id: UUID | None,
    expenses: ExpensesRepository,
    categories: CategoriesRepository,
    rate_limit: ScanRateLimitRepository,
    settings: Settings,
) -> tuple[ExpenseResponse, bool]:
    identifier = str(expense_id or uuid4())
    if expense_id is not None:
        existing = await expenses.get(uid, identifier)
        if existing is not None:
            return _scan_response(existing), False

    image_bytes = await _read_image(image, settings.max_image_bytes)
    try:
        jpeg_bytes = await prepare_image(image_bytes)
    except UnsupportedImageTypeError as exc:
        raise AppError("unsupported_image_type", 415, "Unsupported image type") from exc

    active_categories = await categories.list_active(uid)
    other = next(
        (category for category in active_categories if category.get("is_other")),
        None,
    )
    if other is None:
        raise AppError("category_not_found", 422, "Category not found or archived")

    await rate_limit.consume(uid, settings.scan_rate_limit_per_hour)
    extraction = await gemini.extract(jpeg_bytes, active_categories)
    active_ids = {category["id"] for category in active_categories}
    category_id = (
        extraction.category_id
        if extraction.category_id in active_ids
        else str(other["id"])
    )
    expense = _expense_from_extraction(identifier, extraction, category_id, settings)
    stored, created = await expenses.create_idempotent(uid, expense)
    if not created and stored.get("deleted_at") is not None:
        raise AppError("not_found", 404, "Expense not found")
    return _scan_response(stored), created
