import asyncio

from app.dependencies.graph import eka_graph


async def test_stream():
    initial_state = {
        "query": "How do I reset my company password?",
        "request_id": "test-stream-001",
    }

    async for event in eka_graph.astream(
        initial_state,
        stream_mode="updates",
    ):
        print("EVENT:", event)


if __name__ == "__main__":
    asyncio.run(test_stream())