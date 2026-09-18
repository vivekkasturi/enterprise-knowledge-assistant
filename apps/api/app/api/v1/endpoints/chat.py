from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.rag import rag_service
from app.schemas.health import ChatRequest
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


def get_chat_service() -> ChatService:
    return ChatService(rag_service=rag_service)


@router.get("")
async def chat(chat_service: Annotated[ChatService, Depends(get_chat_service)]):
    return await chat_service.chat()


@router.post("/response")
async def chat_response(
    request: ChatRequest,
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
):
    return await chat_service.chat_response(request.message)
