from typing import Literal

from pydantic import BaseModel


# Gemini response_schema rejects additionalProperties, so no extra="forbid" here.
class ExtractionItem(BaseModel):
    description: str | None
    quantity: str | None
    unit_price: str | None
    total: str | None


class ExtractionModel(BaseModel):
    document_type: Literal["receipt", "invoice", "payment_screenshot", "other"]
    seller: str | None
    date: str | None
    date_reliable: bool
    total: str | None
    currency: str | None
    items: list[ExtractionItem]
    vat_total: str | None
    vat_number: str | None
    payment_method: str | None
    category_id: str | None
