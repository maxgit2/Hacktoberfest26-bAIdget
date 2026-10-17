from decimal import ROUND_HALF_UP, Decimal, DecimalException

CENT = Decimal("0.01")
MAX_AMOUNT = Decimal("1000000.00")


def parse_amount(value: str | float | Decimal) -> Decimal:
    normalized: str | float | Decimal = "" if isinstance(value, bool) else value
    if isinstance(value, str):
        normalized = value.strip()
        # The last separator is the decimal one: "1.234,56" and "1,234.56" -> 1234.56
        if "," in normalized and normalized.rfind(",") > normalized.rfind("."):
            normalized = normalized.replace(".", "").replace(",", ".")
        else:
            normalized = normalized.replace(",", "")

    try:
        amount = Decimal(str(normalized))
        rounded = amount.quantize(CENT, rounding=ROUND_HALF_UP)
    except (DecimalException, ValueError) as exc:
        raise ValueError("Amount must be a number") from exc

    if not amount.is_finite() or amount != rounded:
        raise ValueError("Amount must have at most two decimal places")
    if amount <= 0 or amount > MAX_AMOUNT:
        raise ValueError("Amount must be greater than 0 and at most 1000000")
    return rounded


def to_cents(amount: Decimal) -> int:
    return int(parse_amount(amount) * 100)


def from_cents(cents: int) -> Decimal:
    if isinstance(cents, bool) or not isinstance(cents, int):
        raise TypeError("Cents must be an integer")
    return (Decimal(cents) / 100).quantize(CENT)
