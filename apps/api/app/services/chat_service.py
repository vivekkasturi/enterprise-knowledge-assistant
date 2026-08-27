from app.core.logging import get_logger
from app.services.llmservice import LLMService

logger = get_logger(__name__)


class ChatService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    async def chat(self) -> dict:
        logger.info("ChatService chat method called")
        return {"message": "Hello from ChatService!"}

    async def chat_response(self, user_message: str):
        logger.info("ChatService chat_response method called")

        response = await self.llm_service.generate_response(user_message)
        return {"message": response}
