from fastapi import APIRouter, Depends
from app.dependencies.llm import llm_service
from app.schemas.health import ChatRequest
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


def get_chat_service()->ChatService:
    return ChatService(llm_service=llm_service)

@router.get("")
async def chat(
    chat_service: ChatService = Depends(get_chat_service)
):
    return await chat_service.chat()

@router.post("/response")
async def chat_response(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
):
    return await chat_service.chat_response(request.message)
