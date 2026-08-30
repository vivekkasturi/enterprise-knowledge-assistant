from app.rag.embeddings.embedding_service import EmbeddingService


service = EmbeddingService()

texts = [
    "How do I reset my password?",
    "Employees can reset passwords from the security portal.",
]

embeddings = service.generate_embedding(texts)

print("Number of embeddings:", len(embeddings)) # 2
print("Vector dimension:", len(embeddings[0])) # 384

