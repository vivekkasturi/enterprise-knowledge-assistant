from app.core.config import settings
from app.integrations.llm.groq_client import GroqClient
from app.services.llmservice import LLMService

groq_client = GroqClient(
    api_key=settings.groq_api_key,
    model=settings.llm_model,
)


llm_service = LLMService(llm_client=groq_client)
