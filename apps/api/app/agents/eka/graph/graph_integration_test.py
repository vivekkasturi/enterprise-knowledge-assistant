import asyncio

from app.agents.eka.graph.graph import build_eka_graph
from app.dependencies.llm import llm_service
from app.dependencies.rag import rag_service


async def main():
    graph = build_eka_graph(
        llmservice=llm_service,
        rag_service=rag_service,
    )

    initial_state = {
        "query": "How to reset password?",
        "request_id": "integration-test-002",
    }

    print("Starting graph...")

    result = await graph.ainvoke(initial_state)

    print("\nGraph Result:")
    print(result)


# if __name__ == "__main__":
#     asyncio.run(main())