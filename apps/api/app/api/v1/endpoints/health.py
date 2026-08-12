from fastapi import APIRouter, Request, Response

from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.health import HealthCheckResponse

router = APIRouter(prefix="/health", tags=["Health"])
logger = get_logger(__name__)


@router.get("", response_model=HealthCheckResponse, status_code=200)
async def health_check(request: Request, response: Response) -> HealthCheckResponse:
    request_id = getattr(request.state, "request_id", None)
    logger.debug(f"Logger name: {logger.name}")
    logger.info("Health check endpoint called")
    logger.debug(f"Request ID: {request_id}")
    logger.debug(f"Response headers: {response.headers}")
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Request URL: {request.url}")
    logger.debug(f"Response status code: {response.status_code}")

    return HealthCheckResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
    )


# @router.get("", response_model=HealthCheckResponse)
# async def health_check()-> HealthCheckResponse:
#     raise AppException(status_code=500, detail="Health check failed. Service is unhealthy.")
