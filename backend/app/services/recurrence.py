import calendar
from datetime import datetime, timedelta
from typing import Literal
from uuid import UUID, uuid5

Frequency = Literal["weekly", "monthly", "yearly"]
OCCURRENCE_NAMESPACE = UUID("5d738426-e018-4a75-933d-47b1939b0528")


def occurrence_date(start_local: datetime, frequency: Frequency, n: int) -> datetime:
    if start_local.utcoffset() is None:
        raise ValueError("start_local must include a UTC offset")
    if n < 0:
        raise ValueError("n must be non-negative")
    if frequency == "weekly":
        return start_local + timedelta(weeks=n)

    months = n if frequency == "monthly" else 12 * n
    if frequency not in {"monthly", "yearly"}:
        raise ValueError("Unsupported frequency")
    month_index = start_local.year * 12 + start_local.month - 1 + months
    year, zero_based_month = divmod(month_index, 12)
    month = zero_based_month + 1
    day = min(start_local.day, calendar.monthrange(year, month)[1])
    return start_local.replace(year=year, month=month, day=day)


def occurrence_id(rule_id: str, n: int) -> str:
    return str(uuid5(OCCURRENCE_NAMESPACE, f"{rule_id}:{n}"))
