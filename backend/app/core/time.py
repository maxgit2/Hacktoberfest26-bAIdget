from datetime import UTC, datetime


def parse_datetime(value: str | datetime) -> datetime:
    try:
        parsed = datetime.fromisoformat(value) if isinstance(value, str) else value
        if not isinstance(parsed, datetime) or parsed.utcoffset() is None:
            raise ValueError
    except (TypeError, ValueError) as exc:
        raise ValueError("Datetime must include a UTC offset") from exc
    return parsed.astimezone(UTC)


def to_z(value: datetime) -> str:
    return parse_datetime(value).isoformat().replace("+00:00", "Z")
