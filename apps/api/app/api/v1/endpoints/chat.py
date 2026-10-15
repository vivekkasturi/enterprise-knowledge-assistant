from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
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
    http_request: Request,
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
):
    request_id = getattr(http_request.state, "request_id", None)
    return await chat_service.chat_response(request.message, request_id=request_id)

@router.post("/stream")
async def chat_stream_response(
    request: ChatRequest,
    http_request: Request,
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
):
    request_id = getattr(http_request.state, "request_id", None)
    stream = chat_service.chat_stream(request.message, request_id=request_id)
    return StreamingResponse(
        stream,
        media_type="text/plain"
    )
