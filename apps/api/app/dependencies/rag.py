from app.core.config import get_settings
from app.dependencies.llm import llm_service
from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.rag_service import RAGService
from app.rag.retrieval.retriever_service import RetrieverService
from app.rag.vectorstore.vector_store_service import VectorStoreService

settings = get_settings()

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
)

# RAG service
rag_service = RAGService(
    retriever_service=retriever_service,
    llm_service=llm_service,
)
