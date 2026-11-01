from app.core.logging import get_logger
from app.rag.rag_service import RAGService
from typing import Any

logger = get_logger(__name__)


# class ChatService:
#     def __init__(self, llm_service: LLMService):
#         self.llm_service = llm_service

#     async def chat(self) -> dict:
#         logger.info("ChatService chat method called")
#         return {"message": "Hello from ChatService!"}

#     async def chat_response(self, user_message: str):
#         logger.info("ChatService chat_response method called")

#         response = await self.llm_service.generate_response(user_message)
#         return {"message": response}


class ChatService:
    def __init__(self, rag_service: RAGService, eka_graph: Any):
        self.rag_service = rag_service
        self.eka_graph = eka_graph

    async def chat(self) -> dict:
        logger.info("ChatService chat method called")
        return {"message": "Hello from ChatService!"}

    async def chat_response(self, user_message: str, request_id: str | None = None):
        logger.info("ChatService chat_response method called")

        response = await self.rag_service.generate_final_answer(
            query=user_message, top_k=5, request_id=request_id
        )
        return {"message": response}

    async def chat_stream(self, user_message: str, request_id: str | None = None):
        logger.info("ChatService chat_stream method called")

        async for chunk in self.rag_service.stream_final_answer(
            query=user_message, top_k=5, request_id=request_id
        ):
            yield chunk

    async def langgraph_response(self, user_message: str, request_id: str | None):
        logger.info("Langgraph is started")

        initial_state = {
             "query": user_message,
              "request_id": request_id,
        }
        response = await self.eka_graph.ainvoke(initial_state)

        return {"message": response["response"]}

    async def langgraph_stream(self, user_message:str, request_id:str | None):
        logger.info("Langraph streaming is activated")

        initial_state = {
            "query": user_message,
            "request_id": request_id
        }
        streamed_nodes = set()
        try:
            async for mode, event in self.eka_graph.astream(
                initial_state, stream_mode=["updates", "custom"]
            ):
                if mode == "custom" and event.get("type") == "token":
                    content = event.get("content")
                    if content:
                        streamed_nodes.add(event.get("node"))
                        yield content
                elif mode == "updates":
                    for node, update in event.items():
                        # General answers arrive as a completed node update. RAG
                        # answers have already been emitted through token events.
                        if node not in streamed_nodes and isinstance(update, dict):
                            response = update.get("response")
                            if response:
                                yield response
        except Exception:
            logger.exception("Chat stream failed | request_id=%s", request_id)
            yield (
                "\nUnable to complete your answer. Please try again. "
                "If this continues, ask support to check the server logs"
                + (f" for request {request_id}." if request_id else ".")
            )
