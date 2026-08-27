class LLMService:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    async def generate_response(self, user_message: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
        response = await self.llm_client.generate(messages=messages)
        return response
