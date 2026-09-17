from app.prompts.chat_prompt import build_chat_messages


class LLMService:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    async def generate(self, messages: list[dict]) -> str:
        response = await self.llm_client.generate(messages=messages)
        return response

    async def generate_response(self, user_message: str) -> str:
        messages = build_chat_messages(user_message)
        response = await self.generate(messages)
        return response
