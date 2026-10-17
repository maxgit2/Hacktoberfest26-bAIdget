from decimal import Decimal

import pytest

from app.core.money import from_cents, parse_amount, to_cents


def test_money_converts_exactly_through_cents():
    assert to_cents(Decimal("0.10")) + to_cents(Decimal("0.20")) == 30
    assert from_cents(30) == Decimal("0.30")


def test_parse_amount_normalizes_comma_formats():
    assert parse_amount("1.234,56") == Decimal("1234.56")
    assert parse_amount("12,5") == Decimal("12.50")


@pytest.mark.parametrize("value", ["0.001", "0", "1000000.01", "nan", True])
def test_parse_amount_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        parse_amount(value)


def test_parse_amount_handles_both_separator_styles():
    from decimal import Decimal

    from app.core.money import parse_amount

    assert parse_amount("1.234,56") == Decimal("1234.56")
    assert parse_amount("1,234.56") == Decimal("1234.56")
    assert parse_amount("12,5") == Decimal("12.50")
    assert parse_amount("12.50") == Decimal("12.50")
