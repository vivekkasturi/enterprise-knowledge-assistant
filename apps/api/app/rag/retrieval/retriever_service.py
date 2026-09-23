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
        results = self.vector_store_service.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
        )
        similarity_threshold: float = 0.5
        # Filter results based on similarity threshold
        filtered_results = [
            result for result in results if result["similarity"] >= similarity_threshold
        ]
        # 3. Return results
        return filtered_results

    def reciprocal_rank_fusion(self, similarity_results, keyword_results):
        # Create a dictionary to hold the fused results
        fused_results = {}
        rrf_k = 60  # You can adjust this parameter based on your needs

        # Assign scores based on rank for similarity results
        for rank, result in enumerate(similarity_results, start = 1):
            score = 1 / (rrf_k + rank)
            fused_results[result["id"]] = {
                **result,
                "rrf_score": score,
            }

        # Assign scores based on rank for keyword results
        for rank, result in enumerate(keyword_results, start = 1):
            score = 1 / (rrf_k + rank)
            if result["id"] in fused_results:
                fused_results[result["id"]]["rrf_score"] += score
            else:
                fused_results[result["id"]] = {
                    **result,
                    "rrf_score": score,
                }

        # Sort the fused results based on the combined score
        ranked_results = sorted(fused_results.values(), key = lambda x: x["rrf_score"], reverse = True)
        
        return ranked_results
        

    def hybrid_retrieve(self, query: str, top_k: int = 10, similarity_threshold: float = 0.5):
        # 1. Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)

        # 2. Perform similarity search
        similarity_results = self.vector_store_service.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
        )
        # 3. Perform keyword search
        keyword_results = self.vector_store_service.keyword_search(
            keyword=query, top_k=top_k
        )

        # Filter using similarity threshold
        filtered_similarity_results = [
            result for result in similarity_results if result["similarity"] >= similarity_threshold
        ]

        # 4. Fuse using reciprocal rank fusion
        fused_reciprocal_results = self.reciprocal_rank_fusion(filtered_similarity_results, keyword_results)

        return fused_reciprocal_results[:top_k]