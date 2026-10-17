import json
import logging
import logging.config
from datetime import UTC, datetime
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        for field in ("request_id", "method", "status"):
            if hasattr(record, field):
                payload[field] = getattr(record, field)
        return json.dumps(payload)


def configure_logging() -> None:
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"json": {"()": JsonFormatter}},
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                }
            },
            "root": {"handlers": ["default"], "level": "INFO"},
        }
    )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = str(uuid4())
        request.state.request_id = request_id
        try:
            response = await call_next(request)
        except Exception:
            self._log(request, request_id, 500)
            raise
        response.headers["X-Request-ID"] = request_id
        self._log(request, request_id, response.status_code)
        return response

    @staticmethod
    def _log(request: Request, request_id: str, status: int) -> None:
        logging.getLogger("baidget.request").info(
            "request_completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "status": status,
            },
        )
