import asyncio
from app.agents.eka.graph.graph import build_eka_graph

# Fake LLM service only for testing the graph
class FakeLLMService:

    async def generate(self, messages: list[dict]) -> str:
        # Router node calls this
        return "GENE"

    async def generate_response(self, user_message: str) -> str:
        # General node calls this
        return f"General response for: {user_message}"


# Fake RAG service only for testing the graph
class FakeRAGService:

    async def generate_final_answer(self, query: str) -> str:
        return f"RAG response for: {query}"


async def main():

    llmservice = FakeLLMService()
    rag_service = FakeRAGService()

    # Build + compile LangGraph
    graph = build_eka_graph(
        llmservice=llmservice,
        rag_service=rag_service,
    )

    # Initial graph state
    initial_state = {
        "query": "What is captial of India?",
        "request_id": "test-002",
    }

    # Execute graph
    result = await graph.ainvoke(initial_state)

    print("\nGraph Result:")
    print(result)


# if __name__ == "__main__":
#     asyncio.run(main())