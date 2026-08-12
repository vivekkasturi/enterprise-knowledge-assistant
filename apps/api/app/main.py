# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.api.v1.router import router as api_router
# from app.core.config import settings, setup_logging
# from app.core.config import settings

# app = FastAPI(
#     title=settings.app_name,
#     description="API for the Enterprise Knowledge Assistant application.",
#     version=settings.app_version,
# )


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[settings.frontend_url],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# setup_logging()

# logger = setup_logging().getLogger(__name__)

# logger.info(f"Starting {settings.app_name} version {settings.app_version} in {settings.environment} environment.")

# app.include_router(
#     api_router,
#     prefix="/api/v1",
# )

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_router
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.core.exceptions import AppException
from fastapi.responses import JSONResponse
from app.middleware.request_id import request_id_middleware

setup_logging()

logger = get_logger(__name__)


app = FastAPI(
    title=settings.app_name,
    description="API for the Enterprise Knowledge Assistant application.",
    version=settings.app_version,
)

app.add_middleware(request_id_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    api_router,
    prefix="/api/v1",
)


logger.info("Enterprise Knowledge Assistant API started")
logger.debug("Debug logging is enabled")


@app.exception_handler(AppException)
async def app_expection_handler(request, exc: AppException):
    logger.error("An unhandled exception occurred in the application.")
    return  JSONResponse(
        status_code=exc.status_code,
        content={"success": False,
        "error": {
            "message": exc.detail,
        }}
    )


