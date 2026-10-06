import time

from app.core.logging import get_logger
from app.prompts.rag_prompt import build_rag_messages
from app.rag.reranking.reranker_service import RerankService
from app.rag.retrieval.retriever_service import RetrieverService
from app.rag.tokenization.token_counter import TokenCounter
from app.services.llmservice import LLMService
from app.core.exceptions import RetrievalException,LLMServiceException

logger = get_logger(__name__)


class RAGService:
    def __init__(
        self,
        retriever_service: RetrieverService,
        llm_service: LLMService,
        reranker_service: RerankService,
        token_counter: TokenCounter,
        rag_max_tokens: int,
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
        request_id: str | None = None,
    ) -> str:
        context, _ = self._build_context_with_metrics(
            query=query, top_k=top_k, request_id=request_id
        )
        return context

    def _log_latency(
        self,
        request_id: str | None,
        stage: str,
        latency_ms: float,
        **metrics,
    ) -> None:
        logger.info(
            "RAG latency | request_id=%s | stage=%s | latency_ms=%.2f | metrics=%s",
            request_id or "unknown",
            stage,
            latency_ms,
            metrics,
        )

    def _build_context_with_metrics(
        self,
        query: str,
        top_k: int = 5,
        request_id: str | None = None,
    ) -> tuple[str, dict]:
        start_time = time.perf_counter()
        try:
            results = self.retriever_service.hybrid_retrieve(query=query, top_k=top_k)
            retrieval_latency_ms = (time.perf_counter() - start_time) * 1000
            retrieval_count = len(results)
            self._log_latency(
                request_id,
                "retrieval",
                retrieval_latency_ms,
                document_count=retrieval_count,
            )

        except RetrievalException as e:
            failure_latency_ms = (time.perf_counter() - start_time) * 1000

            logger.exception(
                "RAG retrieval failed | request_id=%s | latency_ms=%.2f |  stage=retrieval | error=%s",
                request_id or "unknown",
                failure_latency_ms,
                e.detail,
            )
            raise
        if not results:
            return "", {
                "retrieval_document_count": retrieval_count,
                "rerank_input_document_count": 0,
                "rerank_output_document_count": 0,
                "context_token_count": 0,
            }

        selected_chunks = []
        total_tokens = 0

        start_time = time.perf_counter()
        reranked_docs = self.reranker_service.rerank(
            query=query, documents=results, top_k=top_k
        )
        rerank_latency_ms = (time.perf_counter() - start_time) * 1000
        rerank_output_count = len(reranked_docs)
        self._log_latency(
            request_id,
            "reranking",
            rerank_latency_ms,
            input_document_count=retrieval_count,
            output_document_count=rerank_output_count,
        )

        if not reranked_docs:
            return "", {
                "retrieval_document_count": retrieval_count,
                "rerank_input_document_count": retrieval_count,
                "rerank_output_document_count": rerank_output_count,
                "context_token_count": 0,
            }

        start_time = time.perf_counter()
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
        context_latency_ms = (time.perf_counter() - start_time) * 1000
        self._log_latency(
            request_id,
            "context_construction",
            context_latency_ms,
            context_token_count=total_tokens,
        )
        return context, {
            "retrieval_document_count": retrieval_count,
            "rerank_input_document_count": retrieval_count,
            "rerank_output_document_count": rerank_output_count,
            "context_token_count": total_tokens,
        }

    async def generate_final_answer(
        self,
        query: str,
        top_k: int = 5,
        request_id: str | None = None,
    ) -> str:
        rag_start_time = time.perf_counter()

        # 1. Retrieve relevant chunks and build context
        context, context_metrics = self._build_context_with_metrics(
            query=query,
            top_k=top_k,
            request_id=request_id,
        )

        if not context:
            total_latency_ms = (time.perf_counter() - rag_start_time) * 1000
            self._log_latency(
                request_id,
                "entire_rag_request",
                total_latency_ms,
                **context_metrics,
            )
            return "I'm sorry, I couldn't find any relevant information to answer your question."
        # 2. Build RAG-specific prompt
        messages = build_rag_messages(
            query=query,
            context=context,
        )

        # 3. Send messages to LLM
        start_time = time.perf_counter()

        try:
            response = await self.llm_service.generate(
                messages=messages,
            )
            llm_latency_ms = (time.perf_counter() - start_time) * 1000

            self._log_latency(
                request_id,
                "llm",
                llm_latency_ms,
                token_usage=None,
            )
            
        except LLMServiceException as e:
            llm_failure_latency_ms = (time.perf_counter() - start_time) * 1000
            logger.exception(
                "RAG LLM generation failed | request_id=%s | latency_ms=%.2f |  stage=llm | error=%s",
                request_id or "unknown",
                llm_failure_latency_ms,
                e.detail,
            )
            raise

        # Successful complete RAG request
        total_latency_ms = (time.perf_counter() - rag_start_time) * 1000
        self._log_latency(
                request_id,
                "entire_rag_request",
                total_latency_ms,
                **context_metrics,
        )

        # 4. Return generated answer
        return response
