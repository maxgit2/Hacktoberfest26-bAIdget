from fastapi import APIRouter, status

from app.models.errors import error_responses

router = APIRouter()


@router.get(
    "/health",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
    operation_id="healthCheck",
    responses=error_responses("internal_error"),
)
async def health() -> dict[str, str]:
    return {"status": "ok"}
