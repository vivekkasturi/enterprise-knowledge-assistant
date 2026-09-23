from sentence_transformers import CrossEncoder


class RerankService:

    def __init__(self, CrossEncoder_model_name: str = "cross-encoder/ms-marco-MiniLM-L6-v2"):
        self.cross_encoder = CrossEncoder(CrossEncoder_model_name)
    

    def rerank(self, query: str, documents: list[dict], top_k: int =5) -> list[dict]:
        """
        Rerank the documents based on their relevance to the query using a CrossEncoder model.

        Args:
            query (str): The query string.
            documents (list[dict]): A list of documents, where each document is a dictionary containing at least 'content'.
            top_k (int): The number of top documents to return after reranking.

        Returns:
            list[dict]: A list of reranked documents, sorted by relevance score in descending order.
        """
       # 1. Handle the case where there are no documents to rerank
        if not documents:
              return []

        # 2. Prepare the input for the CrossEncoder model
        for doc in documents:
            pairs = [ (query, doc['content']) for doc in documents]

        # 3. Get relevance scores from the CrossEncoder model

        scores = self.cross_encoder.predict(pairs)

        # 4. Attach scores to documents

        for doc, score in zip(documents, scores):
            doc['rerank_score'] = score

        # 5. Sort documents by score in descending order
        ranked_documents = sorted(documents, key=lambda x: x['rerank_score'], reverse=True)
        # 6. Return the top_k documents
        return ranked_documents[:top_k]