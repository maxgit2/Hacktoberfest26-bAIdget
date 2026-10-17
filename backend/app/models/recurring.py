from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    field_serializer,
    field_validator,
    model_validator,
)

from app.core.money import parse_amount
from app.core.time import to_z
from app.models.expense import ExpenseResponse


class MakeRecurringRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    frequency: Literal["weekly", "monthly", "yearly"]
    end_date: date | None = None


class RecurringRuleUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    seller: str | None = None
    title: str | None = None
    description: str | None = None
    category: str | None = None
    amount: Decimal | None = None
    end_date: date | None = None
    active: bool | None = None

    @field_validator("amount", mode="before")
    @classmethod
    def validate_amount(cls, value: object) -> Decimal | None:
        return None if value is None else parse_amount(value)  # type: ignore[arg-type]

    @model_validator(mode="after")
    def validate_fields(self) -> "RecurringRuleUpdate":
        if not self.model_fields_set:
            raise ValueError("At least one field is required")
        for field in ("category", "active"):
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class RecurringTemplateResponse(BaseModel):
    seller: str | None
    title: str | None
    description: str | None
    category: str
    amount: float | None
    currency: Literal["EUR"]


class RecurringRuleResponse(BaseModel):
    id: str
    frequency: Literal["weekly", "monthly", "yearly"]
    start: datetime
    end_date: date | None
    active: bool
    template: RecurringTemplateResponse

    @field_serializer("start")
    def serialize_start(self, value: datetime) -> str:
        return to_z(value)


class RecurringRuleListResponse(BaseModel):
    items: list[RecurringRuleResponse]


class MakeRecurringResponse(BaseModel):
    rule: RecurringRuleResponse
    expense: ExpenseResponse
    created_occurrences: int


class RecurringSyncResponse(BaseModel):
    created: int
    rules_processed: int
    has_more: bool
