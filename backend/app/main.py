from fastapi import FastAPI

from app.core.errors import install_error_handlers
from app.core.logging import RequestLoggingMiddleware, configure_logging
from app.routers.health import router as health_router


def create_app() -> FastAPI:
    configure_logging()
    application = FastAPI(
        title="bAIdget API",
        docs_url="/v1/docs",
        redoc_url="/v1/redoc",
        openapi_url="/v1/openapi.json",
    )
    application.add_middleware(RequestLoggingMiddleware)
    install_error_handlers(application)
    application.include_router(health_router)
    return application


app = create_app()
