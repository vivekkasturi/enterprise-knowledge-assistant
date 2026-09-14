from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.vectorstore.vector_store_service import VectorStoreService


class RetrieverService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store_service: VectorStoreService,
    ):
        # initialize dependencies
        self.embedding_service = embedding_service
        self.vector_store_service = vector_store_service

    def retrieve(self, query: str, top_k: int = 5):

        # 1. Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)
        # 2. Perform similarity search
        results = self.vector_store_service.similarity_search(query_embedding=query_embedding, top_k=top_k)
        # 3. Return results
        return results