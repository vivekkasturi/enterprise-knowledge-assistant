from app.core.config import get_settings
from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.retrieval.retriever_service import RetrieverService
from app.rag.vectorstore.vector_store_service import VectorStoreService

settings = get_settings()

embedding_service = EmbeddingService()

vector_store_service = VectorStoreService(
    supabase_url=settings.supabase_url,
    supabase_key=settings.supabase_key,
)

retriever_service = RetrieverService(
    embedding_service=embedding_service,
    vector_store_service=vector_store_service,
)

results = retriever_service.retrieve(
    query="How can employees reset their password?",
    top_k=5,
)

#print(results)

# Test for reciprocal rank fusion
# hybrid_results = retriever_service.hybrid_retrieve(
#     query="How can employees reset their password?",
#     top_k=5)

# print(hybrid_results)


# Test for hybrid retrieval with department filter
hybrid_results = retriever_service.hybrid_retrieve(
    query="How should an enterprise billing dispute be investigated?",
    top_k=5,
    department="finance",)

for result in hybrid_results:
    print(
        result["document_id"],
        result["metadata"].get("department"),
    )


