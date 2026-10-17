import asyncio

from google import genai
from google.genai import errors, types
from pydantic import ValidationError

from app.core.config import get_settings
from app.core.errors import AppError
from app.llm.prompt import build_prompt
from app.llm.schema import ExtractionModel


async def extract(
    image_bytes: bytes, categories: list[dict[str, object]]
) -> ExtractionModel:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise AppError(
            "extraction_unavailable", 503, "Expense extraction is unavailable"
        )

    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        response = await asyncio.wait_for(
            client.aio.models.generate_content(
                model=settings.gemini_model,
                contents=[
                    build_prompt(categories),
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ExtractionModel,
                ),
            ),
            timeout=settings.gemini_timeout_seconds,
        )
    except TimeoutError as exc:
        raise AppError(
            "extraction_timeout", 504, "Expense extraction timed out"
        ) from exc
    except errors.APIError as exc:
        raise AppError(
            "extraction_unavailable", 503, "Expense extraction is unavailable"
        ) from exc

    if isinstance(response.parsed, ExtractionModel):
        return response.parsed
    try:
        return ExtractionModel.model_validate_json(response.text)
    except (TypeError, ValidationError, ValueError) as exc:
        raise AppError("extraction_failed", 422, "Expense extraction failed") from exc
