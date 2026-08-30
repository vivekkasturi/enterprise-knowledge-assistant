from datasets import load_dataset
from app.rag.ingestion.document_factory import create_document
from langchain_core.documents import Document


def load_enterprise_dataset(limit: int = 10) -> list[Document]:

    dataset = load_dataset(
        "onyx-dot-app/EnterpriseRAG-Bench", "documents", split="test", streaming=True
    )

    documents = []

    for record in dataset.take(limit):
        raw_text = record["content"]
        metadata = {
            "id": record["doc_id"],
            "source": record["source_type"],
            "title": record["title"],
        }
        document = create_document(raw_text, metadata)
        documents.append(document)

    return documents
