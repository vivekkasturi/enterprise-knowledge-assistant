from app.agents.eka.state.graph_state import GraphState
from app.rag.rag_service import RAGService
from langgraph.config import get_stream_writer


def create_rag_node(rag_service: RAGService):
    """Create the RAG node for the EKA LangGraph workflow."""
    async def node(state: GraphState) -> dict:
        return await rag_node(state, rag_service)

    return node


async def rag_node(state: GraphState, rag_service: RAGService):
    writer = get_stream_writer()
    full_response = ""
    async for chunk in rag_service.stream_final_answer(
        query=state["query"],
        request_id=state.get("request_id"),
    ):
        full_response += chunk
        writer({
            "type": "token",
            "node": "rag",
            "content": chunk,
        })

    return {"response": full_response}
