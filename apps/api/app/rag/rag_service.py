from app.prompts.rag_prompt import build_rag_messages
from app.rag.retrieval.retriever_service import RetrieverService
from app.services.llmservice import LLMService


class RAGService:
    def __init__(
        self,
        retriever_service: RetrieverService,
        llm_service: LLMService,
    ):
        self.retriever_service = retriever_service
        self.llm_service = llm_service

    def build_context(
        self,
        query: str,
        top_k: int = 5,
    ) -> str:
        results = self.retriever_service.retrieve(
            query=query,
            top_k=top_k,
        )

        context = "\n\n".join(
            f"[Source: {result['metadata'].get('title', 'Unknown')}]\n{result['content']}"
            for result in results
        )
        return context

    async def generate_final_answer(
        self,
        query: str,
        top_k: int = 5,
    ) -> str:

        # 1. Retrieve relevant chunks and build context
        context = self.build_context(
            query=query,
            top_k=top_k,
        )

        print("context", context)
        if not context:
            return "I'm sorry, I couldn't find any relevant information to answer your question."

        print("LLM is not called because context is empty")
        # 2. Build RAG-specific prompt
        messages = build_rag_messages(
            query=query,
            context=context,
        )

        # 3. Send messages to LLM
        response = await self.llm_service.generate(
            messages=messages,
        )
        print(f"RAGService generated response: {response}")

        # 4. Return generated answer
        return response
