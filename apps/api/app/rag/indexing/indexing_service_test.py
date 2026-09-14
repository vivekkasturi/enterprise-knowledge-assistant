from app.core.config import get_settings
from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.indexing.indexing_service import IndexingService
from app.rag.vectorstore.vector_store_service import VectorStoreService

settings = get_settings()

embedding_service = EmbeddingService()

vector_store_service = VectorStoreService(
    supabase_url=settings.supabase_url,
    supabase_key=settings.supabase_key,
)

indexing_service = IndexingService(
    embedding_service=embedding_service,
    vector_store_service=vector_store_service,
)

indexed_count = indexing_service.index_documents(limit=10)

print(f"Indexed chunks: {indexed_count}")
