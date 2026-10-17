from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from app.services.recurrence import occurrence_date

ROME = ZoneInfo("Europe/Rome")


@pytest.mark.parametrize(
    ("start", "frequency", "index", "expected"),
    [
        (datetime(2026, 3, 22, 9, tzinfo=ROME), "weekly", 1, (2026, 3, 29, 9)),
        (datetime(2025, 1, 31, 9, tzinfo=ROME), "monthly", 1, (2025, 2, 28, 9)),
        (datetime(2025, 1, 31, 9, tzinfo=ROME), "monthly", 2, (2025, 3, 31, 9)),
        (datetime(2024, 2, 29, 9, tzinfo=ROME), "yearly", 1, (2025, 2, 28, 9)),
        (datetime(2024, 2, 29, 9, tzinfo=ROME), "yearly", 4, (2028, 2, 29, 9)),
    ],
)
def test_occurrence_date_is_computed_from_start(start, frequency, index, expected):
    result = occurrence_date(start, frequency, index)

    assert (result.year, result.month, result.day, result.hour) == expected
    assert result.tzinfo is ROME


def test_occurrence_date_rejects_invalid_input():
    with pytest.raises(ValueError):
        occurrence_date(datetime(2026, 1, 1), "monthly", 1)
    with pytest.raises(ValueError):
        occurrence_date(datetime(2026, 1, 1, tzinfo=ROME), "monthly", -1)
