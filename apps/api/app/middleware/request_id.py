import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.logging import get_logger


logger = get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):        
        request_id = str(uuid.uuid4())
        logger.debug(f"Request ID: {request_id}")
        request.state.request_id = request_id
        logger.info(f"Request ID middleware called for path: {request.url.path}")
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        logger.info(f"Request ID {request_id} added to response headers for path: {request.url.path}")
        return response


request_id_middleware = RequestIDMiddleware
