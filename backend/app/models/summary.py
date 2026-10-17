from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, field_serializer

from app.core.time import to_z


class SummaryPeriod(BaseModel):
    type: Literal["month", "year"]
    value: str
    from_: datetime = Field(alias="from")
    to: datetime

    @field_serializer("from_", "to")
    def serialize_datetime(self, value: datetime) -> str:
        return to_z(value)


class CategorySummary(BaseModel):
    category: str
    name: str
    total: Decimal
    count: int
    percentage: Decimal

    @field_serializer("total", "percentage")
    def serialize_decimal(self, value: Decimal) -> float:
        return float(value)


class MonthSummary(BaseModel):
    month: str
    total: Decimal
    count: int

    @field_serializer("total")
    def serialize_decimal(self, value: Decimal) -> float:
        return float(value)


class SummaryBase(BaseModel):
    period: SummaryPeriod
    currency: Literal["EUR"] = "EUR"
    total: Decimal
    count: int
    uncounted: int
    by_category: list[CategorySummary]

    @field_serializer("total")
    def serialize_decimal(self, value: Decimal) -> float:
        return float(value)


class MonthlySummaryResponse(SummaryBase):
    pass


class YearlySummaryResponse(SummaryBase):
    by_month: list[MonthSummary]
