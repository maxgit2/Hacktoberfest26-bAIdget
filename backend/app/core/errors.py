from collections.abc import Mapping
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException


class AppError(Exception):
    def __init__(
        self,
        code: str,
        http_status: int,
        message: str,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.http_status = http_status
        self.message = message
        self.details = dict(details or {})


def _response(
    status: int,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={"error": {"code": code, "message": message, "details": details or {}}},
    )


async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    return _response(exc.http_status, exc.code, exc.message, exc.details)


async def http_error_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    errors = {
        401: ("unauthenticated", "Authentication required"),
        404: ("not_found", "Resource not found"),
    }
    code, message = errors.get(
        exc.status_code, ("internal_error", "Internal server error")
    )
    status = exc.status_code if exc.status_code in errors else 500
    return _response(status, code, message)


async def validation_error_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    fields = [
        {
            "field": ".".join(
                str(part)
                for part in error["loc"]
                if part not in {"body", "query", "path"}
            ),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]
    return _response(
        422, "validation_error", "Request validation failed", {"fields": fields}
    )


async def internal_error_handler(_request: Request, _exc: Exception) -> JSONResponse:
    response = _response(500, "internal_error", "Internal server error")
    if request_id := getattr(_request.state, "request_id", None):
        response.headers["X-Request-ID"] = request_id
    return response


def install_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, internal_error_handler)
