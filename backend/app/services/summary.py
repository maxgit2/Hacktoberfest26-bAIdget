from datetime import UTC, datetime
from decimal import ROUND_HALF_UP, Decimal
from zoneinfo import ZoneInfo

from app.core.config import Settings
from app.core.errors import AppError
from app.core.money import from_cents
from app.models.summary import (
    CategorySummary,
    MonthlySummaryResponse,
    MonthSummary,
    SummaryPeriod,
    YearlySummaryResponse,
)
from app.repositories.categories import CategoriesRepository
from app.repositories.expenses import ExpensesRepository


def _invalid_period(field: str) -> AppError:
    return AppError(
        "validation_error",
        422,
        f"Invalid {field}",
        {"fields": [{"field": field, "message": f"Invalid {field}"}]},
    )


def _month_period(month: str, timezone: ZoneInfo) -> tuple[datetime, datetime]:
    try:
        year, month_number = map(int, month.split("-"))
        if month != f"{year:04d}-{month_number:02d}":
            raise ValueError
        start = datetime(year, month_number, 1, tzinfo=timezone)
        end = (
            datetime(year + 1, 1, 1, tzinfo=timezone)
            if month_number == 12
            else datetime(year, month_number + 1, 1, tzinfo=timezone)
        )
    except (TypeError, ValueError):
        raise _invalid_period("month") from None
    return start.astimezone(UTC), end.astimezone(UTC)


def _year_period(year: str, timezone: ZoneInfo) -> tuple[datetime, datetime]:
    try:
        number = int(year)
        if year != f"{number:04d}":
            raise ValueError
        start = datetime(number, 1, 1, tzinfo=timezone)
        end = datetime(number + 1, 1, 1, tzinfo=timezone)
    except (TypeError, ValueError):
        raise _invalid_period("year") from None
    return start.astimezone(UTC), end.astimezone(UTC)


async def _totals(
    uid: str,
    from_utc: datetime,
    to_utc: datetime,
    timezone: ZoneInfo,
    expenses_repository: ExpensesRepository,
    categories_repository: CategoriesRepository,
) -> tuple[int, int, int, list[CategorySummary], dict[int, tuple[int, int]]]:
    total_cents = 0
    count = 0
    uncounted = 0
    categories: dict[str, tuple[int, int]] = {}
    months = {month: (0, 0) for month in range(1, 13)}

    async for expense in expenses_repository.list_in_range(uid, from_utc, to_utc):
        amount_cents = expense.get("amount_cents")
        if amount_cents is None:
            uncounted += 1
            continue
        if isinstance(amount_cents, bool) or not isinstance(amount_cents, int):
            raise TypeError("Stored amount_cents must be an integer or null")

        category_id = str(expense["category"])
        category_total, category_count = categories.get(category_id, (0, 0))
        categories[category_id] = (
            category_total + amount_cents,
            category_count + 1,
        )
        month = expense["date"].astimezone(timezone).month  # type: ignore[union-attr]
        month_total, month_count = months[month]
        months[month] = (month_total + amount_cents, month_count + 1)
        total_cents += amount_cents
        count += 1

    by_category = []
    for category_id, (category_total, category_count) in categories.items():
        category = await categories_repository.get_any(uid, category_id)
        if category is None:
            raise RuntimeError("Expense category document is missing")
        percentage = (
            Decimal("0.0")
            if total_cents == 0
            else (Decimal(category_total) * 100 / total_cents).quantize(
                Decimal("0.1"), rounding=ROUND_HALF_UP
            )
        )
        by_category.append(
            CategorySummary(
                category=category_id,
                name=str(category["name"]),
                total=from_cents(category_total),
                count=category_count,
                percentage=percentage,
            )
        )
    by_category.sort(key=lambda item: item.total, reverse=True)
    return total_cents, count, uncounted, by_category, months


async def monthly_summary(
    uid: str,
    month: str,
    settings: Settings,
    expenses_repository: ExpensesRepository,
    categories_repository: CategoriesRepository,
) -> MonthlySummaryResponse:
    timezone = ZoneInfo(settings.tz_name)
    from_utc, to_utc = _month_period(month, timezone)
    total, count, uncounted, by_category, _ = await _totals(
        uid,
        from_utc,
        to_utc,
        timezone,
        expenses_repository,
        categories_repository,
    )
    return MonthlySummaryResponse(
        period=SummaryPeriod(
            type="month", value=month, **{"from": from_utc}, to=to_utc
        ),
        total=from_cents(total),
        count=count,
        uncounted=uncounted,
        by_category=by_category,
    )


async def yearly_summary(
    uid: str,
    year: str,
    settings: Settings,
    expenses_repository: ExpensesRepository,
    categories_repository: CategoriesRepository,
) -> YearlySummaryResponse:
    timezone = ZoneInfo(settings.tz_name)
    from_utc, to_utc = _year_period(year, timezone)
    total, count, uncounted, by_category, months = await _totals(
        uid,
        from_utc,
        to_utc,
        timezone,
        expenses_repository,
        categories_repository,
    )
    return YearlySummaryResponse(
        period=SummaryPeriod(type="year", value=year, **{"from": from_utc}, to=to_utc),
        total=from_cents(total),
        count=count,
        uncounted=uncounted,
        by_category=by_category,
        by_month=[
            MonthSummary(
                month=f"{year}-{month:02d}",
                total=from_cents(months[month][0]),
                count=months[month][1],
            )
            for month in range(1, 13)
        ],
    )
