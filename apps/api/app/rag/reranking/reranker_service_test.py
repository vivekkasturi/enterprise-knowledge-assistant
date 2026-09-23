from app.rag.reranking.reranker_service import RerankService

query = "How can employees reset their password?"

documents = [
    {
        "id": "1",
        "content": "Employees receive 20 days of annual leave."
    },
    {
        "id": "2",
        "content": "Employees can reset their password from the security portal."
    },
    {
        "id": "3",
        "content": "The company provides health insurance benefits."
    },
]

reranker = RerankService()

results = reranker.rerank(
    query=query,
    documents=documents,
    top_k=2,
)

for result in results:
    print(f"Document ID: {result['id']}, Rerank Score: {result['rerank_score']}, Content: {result['content']}")
