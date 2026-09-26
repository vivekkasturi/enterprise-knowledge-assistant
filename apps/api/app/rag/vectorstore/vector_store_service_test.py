from app.core.config import get_settings
from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.vectorstore.vector_store_service import VectorStoreService

settings = get_settings()

embedding_service = EmbeddingService()

vector_store = VectorStoreService(
    supabase_url=settings.supabase_url, supabase_key=settings.supabase_key
)

# content = "Employees can reset their password from the security portal."
# content = "How should an enterprise billing dispute be investigated?"

# embedding = embedding_service.generate_embedding(content)

# Test for adding a chunk to the vector store
# result = vector_store.add_chunk(
#     document_id="test-doc-001",
#     content=content,
#     metadata={"source": "test", "title": "Password Reset"},
#     embedding=embedding,
# )

#print(result)

# keyword_results = vector_store.keyword_search(keyword="How to do password reset?", top_k=5, department="finance")



# Test for similarity search with department filter
content = "How should an enterprise billing dispute be investigated?"

embedding = embedding_service.generate_embedding(content)

# keyword_results = vector_store.keyword_search(keyword="How to do password reset?", top_k=5, department="finance")
# Test for similarity search with department filter
vector_similarity_results = vector_store.similarity_search(
    query_embedding=embedding,
    top_k=5,
    department="finance"
)

for result in vector_similarity_results:
    print(
        result["document_id"],
        result["metadata"].get("department"),
        result["similarity"],
    )

# Test for keyword search with department filter
# content = "How should an enterprise billing dispute be investigated?"

# embedding = embedding_service.generate_embedding(content)

keyword_results = vector_store.keyword_search(keyword="billing dispute", top_k=5, department="finance")

for result in keyword_results:
    print(
        result["document_id"],
        result["metadata"].get("department"),
        result["keyword_rank"],
    )

print(keyword_results)