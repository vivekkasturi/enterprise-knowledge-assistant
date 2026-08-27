from groq import AsyncGroq

from app.core.exceptions import LLMServiceException


class GroqClient:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = AsyncGroq(api_key=api_key)

    async def generate(
        self,
        messages: list[dict],
        max_tokens: int = 100,
        temperature: float = 0.7,
    ) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=messages,
            )
        except Exception as e:
            raise LLMServiceException(
                status_code=500,
                detail=f"Failed to generate response from Groq API: {(e)}",

            ) from e

        return response.choices[0].message.content

    
