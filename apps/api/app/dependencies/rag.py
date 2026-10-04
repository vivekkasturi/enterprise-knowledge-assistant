from app.cache.cache_service import CacheService
from app.cache.in_memory_cache import InMemoryCache
from app.core.config import get_settings
from app.dependencies.llm import llm_service
from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.rag_service import RAGService
from app.rag.reranking.reranker_service import RerankService
from app.rag.retrieval.retriever_service import RetrieverService
from app.rag.tokenization.token_counter import TokenCounter
from app.rag.vectorstore.vector_store_service import VectorStoreService

settings = get_settings()

# Cache service
in_memory_cache = InMemoryCache()

cache_service = CacheService(cache=in_memory_cache)

# Embedding service
embedding_service = EmbeddingService()

# Vector store service
vector_store_service = VectorStoreService(
    supabase_url=settings.supabase_url,
    supabase_key=settings.supabase_key,
)

# Retriever service
retriever_service = RetrieverService(
    embedding_service=embedding_service,
    vector_store_service=vector_store_service,
    cache_service=cache_service,
)

# Rerank service
rerank_service = RerankService()

# Token counter
token_counter = TokenCounter()

# RAG service
rag_service = RAGService(
    retriever_service=retriever_service,
    llm_service=llm_service,
    reranker_service=rerank_service,
    token_counter=token_counter,
    rag_max_tokens=settings.rag_max_tokens,
)
