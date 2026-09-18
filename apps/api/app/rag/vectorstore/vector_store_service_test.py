from app.core.config import get_settings
from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.vectorstore.vector_store_service import VectorStoreService

settings = get_settings()

embedding_service = EmbeddingService()

vector_store = VectorStoreService(
    supabase_url=settings.supabase_url, supabase_key=settings.supabase_key
)

content = "Employees can reset their password from the security portal."

embedding = embedding_service.generate_embedding(content)

result = vector_store.add_chunk(
    document_id="test-doc-001",
    content=content,
    metadata={"source": "test", "title": "Password Reset"},
    embedding=embedding,
)

print(result)
