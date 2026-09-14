from app.rag.embeddings.embedding_service import EmbeddingService

from app.rag.vectorstore.vector_store_service import VectorStoreService

service = EmbeddingService()

texts = [
    "How do I reset my password?",
    "Employees can reset passwords from the security portal.",
]

embeddings = service.generate_embedding(texts)

print("Number of embeddings:", len(embeddings)) # 2
print("Vector dimension:", len(embeddings[0])) # 384

vector_service = VectorStoreService()

content = "How do I reset my password?"


result = vector_service.add_chunk(
    document_id="test-doc-001",
    content=content,
    metadata={
        "source": "test",
        "title": "Password Reset"
    },
    embedding=embeddings,
)

print("Chunk added to vector store:", result)