from app.prompts.rag_prompt import build_rag_messages
from app.rag.retrieval.retriever_service import RetrieverService
from app.rag.reranking.reranker_service import RerankerService
from app.rag.tokenization.token_counter import TokenCounter
from app.services.llmservice import LLMService

class RAGService:
    def __init__(
        self,
        retriever_service: RetrieverService,
        llm_service: LLMService,
        reranker_service: RerankerService,
        token_counter: TokenCounter,
        rag_max_tokens: int
    ):
        self.retriever_service = retriever_service
        self.llm_service = llm_service
        self.reranker_service = reranker_service
        self.token_counter = token_counter
        self.rag_max_tokens = rag_max_tokens


    def build_context(
        self,
        query: str,
        top_k: int = 5,
    ) -> str:
        results = self.retriever_service.hybrid_retrieve(
            query=query,
            top_k=top_k,
        )
        selected_chunks = []
        total_tokens = 0
        # Rerank the retrieved documents using the RerankerService

        reranked_docs = self.reranker_service.rerank(query=query, documents=results, top_k=top_k)

        if not reranked_docs:
            return ""
        
        for result in reranked_docs:
           formatted_content = (
                    f"[Source: {result['metadata'].get('title', 'Unknown')}]\n"
                 f"{result['content']}"
)
            chunk_tokens = self.token_counter.count_tokens(formatted_content)
            if total_tokens + chunk_tokens > self.rag_max_tokens:
                continue
            
            selected_chunks.append(formatted_content)
            total_tokens += chunk_tokens

        context = "\n\n".join(selected_chunks)
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
