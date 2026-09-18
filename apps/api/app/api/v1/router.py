from fastapi import APIRouter

from app.api.v1.endpoints.chat import router as chat
from app.api.v1.endpoints.health import router as health

router = APIRouter()
router.include_router(health)
router.include_router(chat)
