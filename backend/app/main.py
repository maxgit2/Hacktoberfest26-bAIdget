from fastapi import FastAPI

from app.core.errors import install_error_handlers
from app.core.logging import RequestLoggingMiddleware, configure_logging
from app.repositories.client import lifespan
from app.routers.categories import router as categories_router
from app.routers.expenses import router as expenses_router
from app.routers.health import router as health_router
from app.routers.me import router as me_router
from app.routers.summary import router as summary_router


def create_app() -> FastAPI:
    configure_logging()
    application = FastAPI(
        title="bAIdget API",
        docs_url="/v1/docs",
        redoc_url="/v1/redoc",
        openapi_url="/v1/openapi.json",
        lifespan=lifespan,
    )
    application.add_middleware(RequestLoggingMiddleware)
    install_error_handlers(application)
    application.include_router(health_router)
    application.include_router(me_router)
    application.include_router(categories_router)
    application.include_router(expenses_router)
    application.include_router(summary_router)
    return application


app = create_app()
