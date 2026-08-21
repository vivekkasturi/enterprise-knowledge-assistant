from fastapi import APIRouter, Depends
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


def get_chat_service()->ChatService:
    return ChatService()

@router.get("")
async def chat(
    chat_service: ChatService = Depends(get_chat_service)
):
    return await chat_service.chat()

@router.post("/response")
async def chat_response(
    chat_service: ChatService = Depends(get_chat_service),
):
    return await chat_service.chat_response()
