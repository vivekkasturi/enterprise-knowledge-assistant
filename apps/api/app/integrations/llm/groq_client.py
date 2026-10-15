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

    async def stream(
        self,
        messages: list[dict], 
        max_tokens: int = 100,
        temperature: float = 0.7,
    ):
        try:
            stream = await self.client.chat.completions.create(
            #     model=self.model,
            #     max_tokens=max_tokens,
            #     temperature=temperature,
            #     messages=messages,
            #     stream=True,
            # )
           model=self.model,
           messages=messages,
           stream=True,
           max_completion_tokens=512,
           temperature=0.6,
           reasoning_effort="low",
           include_reasoning=False,
            )
            async for chunk in stream:
                  # TEMP DEBUG
                print("RAW GROQ CHUNK:", chunk)
                content = chunk.choices[0].delta.content
                # Temp debug: print the content of each chunk
                print("CONTENT:", repr(content))

                if content:
                    yield content

        except Exception as e:
            raise LLMServiceException(
                status_code=500,
                detail=f"Failed to stream response from Groq API: {e}",
            ) from e