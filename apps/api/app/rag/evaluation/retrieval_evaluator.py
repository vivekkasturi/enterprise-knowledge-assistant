from app.rag.retrieval.retriever_service import RetrieverService
from app.core.config import get_settings
from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.vectorstore.vector_store_service import VectorStoreService

settings = get_settings()

embedding_service = EmbeddingService()

def get_relevant_documents(query, top_k):
    retriver_service = RetrieverService(
        embedding_service = embedding_service,
        vector_store_service = VectorStoreService(
            supabase_url=settings.supabase_url,
            supabase_key=settings.supabase_key,
        )
    )
    hybrid_retriver_docs = retriver_service.hybrid_retrieve(query=query, top_k=top_k, similarity_threshold=0.5)
    return hybrid_retriver_docs


    
def precision_at_k(query, top_k, relevant_document_ids):
    relevant_docs_top_k = get_relevant_documents(query, top_k)

    print("\nGround truth:")
    print(relevant_document_ids)

    print("\nRetrieved Top-K:")
    for index, doc in enumerate(relevant_docs_top_k, start=1):
        print(
            index,
            doc.get("document_id"),
            doc.get("metadata", {}).get("title"),
            doc.get("similarity"),
            doc.get("rrf_score"),
        )
    
    if not relevant_docs_top_k:
        return 0.0

    ground_truth_relevant_ids = set(relevant_document_ids)

    retrieved_document_ids = {
        doc["document_id"]
        for doc in relevant_docs_top_k
    }

    matched_ids = retrieved_document_ids.intersection(
        ground_truth_relevant_ids
    )

    precision = (
        len(matched_ids) / len(retrieved_document_ids)
        if retrieved_document_ids
        else 0.0
    )

    return precision

def recall_at_k(query, top_k, relevant_document_ids):
    relevant_docs_top_k = get_relevant_documents(query, top_k)

    if not relevant_docs_top_k:
        return 0.0

    ground_truth_relevant_ids = set(relevant_document_ids)

    retrieved_document_ids = {
        doc["document_id"]
        for doc in relevant_docs_top_k
    }

    matched_ids = retrieved_document_ids.intersection(
        ground_truth_relevant_ids
    )

    recall = (
        len(matched_ids) / len(ground_truth_relevant_ids)
        if ground_truth_relevant_ids
        else 0.0
    )

    return recall

def hit_rate_at_k(query, top_k, relevant_document_ids):
    relevant_docs_top_k = get_relevant_documents(query, top_k)

    if not relevant_docs_top_k:
        return 0.0

    ground_truth_relevant_ids = set(relevant_document_ids)

    retrieved_document_ids = {
        doc["document_id"]
        for doc in relevant_docs_top_k
    }

    matched_ids = retrieved_document_ids.intersection(
        ground_truth_relevant_ids
    )

    hit_rate = 1.0 if matched_ids else 0.0

    return hit_rate

def reciprocal_rank_at_k(query, top_k, relevant_document_ids):
    relevant_docs_top_k = get_relevant_documents(query, top_k)

    if not relevant_docs_top_k:
        return 0.0
    
    ground_truth_relevant_ids = (relevant_document_ids)

    for rank, doc in enumerate(relevant_docs_top_k, start=1):
        if doc["document_id"] in ground_truth_relevant_ids:
            return 1/rank
        
    return 0.0


    # mean reciprocal rank (MRR) is calculated by averaging the reciprocal ranks of multiple queries. If you have multiple queries, you can compute the MRR as follows:
    # query1_rr = reciprocal_rank_at_k(query, top_k, relevant_document_ids)
    # query2_rr = reciprocal_rank_at_k(query, top_k, relevant_document_ids)
    # query3_rr = reciprocal_rank_at_k(query, top_k, relevant_document_ids)

    # mrr = (query1_rr + query2_rr + query3_rr) / 3

        
if(__name__ == "__main__"):
    query = "What should be checked when troubleshooting NAT or egress exhaustion during cross-account GPU bursting?"
    top_k = 5
    precision = precision_at_k(query, top_k, ["dsid_229dd48e9b1d466a81ebaffe3ec84469"])
    recall = recall_at_k(query, top_k, ["dsid_229dd48e9b1d466a81ebaffe3ec84469"])
    hit_rate = hit_rate_at_k(query, top_k, ["dsid_229dd48e9b1d466a81ebaffe3ec84469"])
    reciprocal_rank = reciprocal_rank_at_k(query, top_k, ["dsid_229dd48e9b1d466a81ebaffe3ec84469"])
    print(f"Precision@{top_k} for query '{query}': {precision:.2f}")
    print(f"recall@{top_k} for query '{query}': {recall:.2f}")
    print(f"hit_rate@{top_k} for query '{query}': {hit_rate:.2f}")
    print(f"mmr@{top_k} for query '{query}': {reciprocal_rank}")

    
    

