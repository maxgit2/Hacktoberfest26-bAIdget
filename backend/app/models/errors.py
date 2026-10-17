from typing import Any

from pydantic import BaseModel


class ErrorBody(BaseModel):
    code: str
    message: str
    details: dict[str, Any]


class ErrorResponse(BaseModel):
    error: ErrorBody


ERRORS = {
    "unauthenticated": (401, "Authentication required"),
    "not_found": (404, "Resource not found"),
    "already_onboarded": (409, "Onboarding is already complete"),
    "category_in_use": (409, "The category is currently in use"),
    "cannot_modify_other": (409, "The Other category cannot be deleted"),
    "category_name_taken": (409, "An active category already has this name"),
    "already_recurring": (409, "Expense is already recurring"),
    "image_too_large": (413, "Image exceeds the size limit"),
    "unsupported_image_type": (415, "Unsupported image type"),
    "validation_error": (422, "Request validation failed"),
    "min_categories": (422, "Choose at least two categories"),
    "max_categories": (422, "A maximum of 30 categories is allowed"),
    "category_not_found": (422, "Category not found or archived"),
    "extraction_failed": (422, "Expense extraction failed"),
    "rate_limited": (429, "Too many scans"),
    "extraction_unavailable": (503, "Expense extraction is unavailable"),
    "extraction_timeout": (504, "Expense extraction timed out"),
    "internal_error": (500, "Internal server error"),
}


def error_responses(*codes: str) -> dict[int, dict[str, Any]]:
    responses = {}
    for status_code in sorted({ERRORS[code][0] for code in codes}):
        status_codes = [code for code in codes if ERRORS[code][0] == status_code]
        responses[status_code] = {
            "model": ErrorResponse,
            "description": "Possible errors: "
            + ", ".join(f"`{code}`" for code in status_codes),
            "content": {
                "application/json": {
                    "examples": {
                        code: {
                            "value": {
                                "error": {
                                    "code": code,
                                    "message": ERRORS[code][1],
                                    "details": {},
                                }
                            }
                        }
                        for code in status_codes
                    }
                }
            },
        }
    return responses
