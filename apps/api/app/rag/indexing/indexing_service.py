from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.ingestion.document_chunker import document_chunker
from app.rag.ingestion.enterprise_dataset_loader import load_enterprise_dataset
from app.rag.vectorstore.vector_store_service import VectorStoreService


class IndexingService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store_service: VectorStoreService,
    ):
        self.embedding_service = embedding_service
        self.vector_store_service = vector_store_service

    def index_documents(self, limit: int = 10) -> int:
        """
        Load documents, chunk them, generate embeddings,
        and store them in the vector store.
        """

        # 1. Load documents
        documents = load_enterprise_dataset(limit=limit)

        # 2. Chunk documents
        chunks = document_chunker(documents)

        # 3. Extract text from each chunk
        chunk_texts = [chunk.page_content for chunk in chunks]

        # 4. Generate embeddings in batch
        chunk_embeddings = self.embedding_service.batch_embeddings(chunk_texts)

        # 5. Store each chunk with its corresponding embedding
        for chunk, embedding in zip(chunks, chunk_embeddings):
            self.vector_store_service.add_chunk(
                document_id=chunk.metadata["id"],
                content=chunk.page_content,
                metadata=chunk.metadata,
                embedding=embedding,
            )

        # 6. Return number of indexed chunks
        return len(chunks)
