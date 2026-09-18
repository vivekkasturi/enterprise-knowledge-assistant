import asyncio

from app.core.config import get_settings
from app.integrations.llm.groq_client import GroqClient
from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.RAGService.RAGService import RAGService
from app.rag.retrieval.retriever_service import RetrieverService
from app.rag.vectorstore.vector_store_service import VectorStoreService


async def main():

    settings = get_settings()
    # initialize dependencies
    llm_service = GroqClient(
        api_key=settings.groq_api_key,
        model=settings.llm_model,
    )
    retriever_service = RetrieverService(
        embedding_service=EmbeddingService(),
        vector_store_service=VectorStoreService(
            supabase_url=settings.supabase_url,
            supabase_key=settings.supabase_key,
        ),
    )

    # create RAGService
    rag_service = RAGService(
        retriever_service=retriever_service,
        llm_service=llm_service,
    )
    # await rag_service.answer(...)
    results = await rag_service.generate_final_answer(
        query="What is the captical of India?",  # Expected output: "I dont have enough information."
        # query="How to reset password",  # Expected output: "should give correct answer."
        top_k=5,
    )
    # print response

    print(results)


asyncio.run(main())
