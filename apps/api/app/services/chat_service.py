from app.core.logging import get_logger

logger = get_logger(__name__)


class ChatService:
    async def chat(self)-> dict:
        logger.info("ChatService chat method called")
        return {
            "message": "Hello from ChatService!"
        }
    async def chat_response(self):
        logger.info("ChatService chat_response method called")

        return {
            "message": "This is a response from ChatService!"
        }


chat_service = ChatService()
