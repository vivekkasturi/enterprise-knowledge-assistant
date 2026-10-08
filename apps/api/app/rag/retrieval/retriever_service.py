from app.cache.build_embedding_cache_key import (
    build_cache_key,
    build_retrieval_cache_key,
)
from app.cache.cache_service import CacheService
from app.core.exceptions import RetrievalException, VectorStoreException
from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.vectorstore.vector_store_service import VectorStoreService


class RetrieverService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store_service: VectorStoreService,
        cache_service: CacheService,
    ):
        # initialize dependencies
        self.embedding_service = embedding_service
        self.vector_store_service = vector_store_service
        self.cache_service = cache_service

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
        for rank, result in enumerate(similarity_results, start=1):
            score = 1 / (rrf_k + rank)
            fused_results[result["id"]] = {
                **result,
                "rrf_score": score,
            }

        # Assign scores based on rank for keyword results
        for rank, result in enumerate(keyword_results, start=1):
            score = 1 / (rrf_k + rank)
            if result["id"] in fused_results:
                fused_results[result["id"]]["rrf_score"] += score
            else:
                fused_results[result["id"]] = {
                    **result,
                    "rrf_score": score,
                }

        # Sort the fused results based on the combined score
        ranked_results = sorted(
            fused_results.values(), key=lambda x: x["rrf_score"], reverse=True
        )

        return ranked_results

    def hybrid_retrieve(
        self,
        query: str,
        top_k: int = 10,
        department: str | None = None,
        similarity_threshold: float = 0.5,
    ):

        retrieval_cache_key = build_retrieval_cache_key(
            query=query,
            department=department,
            top_k=top_k,
            similarity_threshold=similarity_threshold,
        )
        cached_results = self.cache_service.get(retrieval_cache_key)

        if cached_results is not None:
            print("✅ RETRIEVAL CACHE HIT")
            return cached_results

        else:
            print("❌ RETRIEVAL CACHE MISS")
            # Build cache key
            model_name = self.embedding_service.embedding_model_name
            cache_key = build_cache_key(query, model_name=model_name)
            cached_embedding = self.cache_service.get(cache_key)

            if cached_embedding is not None:
                print("✅ EMBEDDING CACHE HIT")
                query_embedding = cached_embedding
            else:
                print("❌ EMBEDDING CACHE MISS")

                # 1. Generate query embedding
                query_embedding = self.embedding_service.generate_embedding(query)

                self.cache_service.set(cache_key, query_embedding, timeout=3600)

            try:
                # 2. Perform similarity search
                similarity_results = self.vector_store_service.similarity_search(
                    query_embedding=query_embedding, top_k=top_k, department=department
                )
                # 3. Perform keyword search
                keyword_results = self.vector_store_service.keyword_search(
                    keyword=query, top_k=top_k, department=department
                )

            except VectorStoreException as e:
                raise RetrievalException(
                    status_code=e.status_code,
                    detail=f"Failed to perform retrieval: {e.detail}",
                ) from e

            # Filter using similarity threshold
            filtered_similarity_results = [
                result
                for result in similarity_results
                if result["similarity"] >= similarity_threshold
            ]

            # 4. Fuse using reciprocal rank fusion
            fused_reciprocal_results = self.reciprocal_rank_fusion(
                filtered_similarity_results, keyword_results
            )
            final_results = fused_reciprocal_results[:top_k]

            # Cache the final results
            self.cache_service.set(retrieval_cache_key, final_results, timeout=3600)
        return final_results


#  To test the RetrieverService independently

if __name__ == "__main__":
    from app.cache.cache_service import CacheService
    from app.cache.in_memory_cache import InMemoryCache
    from app.core.config import get_settings
    from app.rag.embeddings.embedding_service import EmbeddingService
    from app.rag.vectorstore.vector_store_service import VectorStoreService

    # Example usage
    settings = get_settings()
    embedding_service = EmbeddingService()
    vector_store_service = VectorStoreService(
        supabase_url=settings.supabase_url,
        supabase_key=settings.supabase_key,
    )
    in_memory_cache = InMemoryCache()

    cache_service = CacheService(cache=in_memory_cache)

    retriever_service = RetrieverService(
        embedding_service=embedding_service,
        vector_store_service=vector_store_service,
        cache_service=cache_service,
    )

    # query = "What is the capital of France?"
    # query = "who are you?"
    query = "What is the capital of India?"
    try:
        print("First retrieval:")
        first_results = retriever_service.hybrid_retrieve(query=query, top_k=5)
        print(first_results)

        print("Second retrieval:")
        second_results = retriever_service.hybrid_retrieve(query=query, top_k=5)
        print(second_results)
    except RetrievalException as e:
        print(f"Retrieval failed ({e.status_code}): {e.detail}")
