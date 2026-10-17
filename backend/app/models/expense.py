from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    field_serializer,
    field_validator,
    model_validator,
)

from app.core.money import parse_amount
from app.core.time import parse_datetime, to_z


class ExpenseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID | None = None
    date: datetime
    category: str
    amount: Decimal | None = None
    currency: Literal["EUR"] = "EUR"
    seller: str | None = None
    title: str | None = None
    description: str | None = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: UUID | None) -> UUID | None:
        if value is not None and value.version != 4:
            raise ValueError("Expense id must be a UUIDv4")
        return value

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: datetime) -> datetime:
        return parse_datetime(value)

    @field_validator("amount", mode="before")
    @classmethod
    def validate_amount(cls, value: object) -> Decimal | None:
        return None if value is None else parse_amount(value)  # type: ignore[arg-type]


class ExpenseUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    date: datetime | None = None
    seller: str | None = None
    title: str | None = None
    description: str | None = None
    category: str | None = None
    amount: Decimal | None = None
    currency: Literal["EUR"] | None = None
    needs_review: bool | None = None

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: datetime | None) -> datetime | None:
        return None if value is None else parse_datetime(value)

    @field_validator("amount", mode="before")
    @classmethod
    def validate_amount(cls, value: object) -> Decimal | None:
        return None if value is None else parse_amount(value)  # type: ignore[arg-type]

    @model_validator(mode="after")
    def validate_fields(self) -> "ExpenseUpdate":
        if not self.model_fields_set:
            raise ValueError("At least one field is required")
        for field in ("date", "category", "currency", "needs_review"):
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class RecurrenceResponse(BaseModel):
    rule_id: str


class ExpenseResponse(BaseModel):
    id: str
    owner: str
    date: datetime
    seller: str | None
    title: str | None
    description: str | None
    category: str
    type: Literal["single", "recurring"]
    recurrence: RecurrenceResponse | None
    amount: float | None
    currency: Literal["EUR"]
    source: Literal["manual", "scan"]
    scan_details: dict[str, object] | None
    needs_review: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    @field_serializer("date", "created_at", "updated_at", "deleted_at")
    def serialize_datetime(self, value: datetime | None) -> str | None:
        return None if value is None else to_z(value)


class ExpenseListResponse(BaseModel):
    items: list[ExpenseResponse]
    next_cursor: str | None
