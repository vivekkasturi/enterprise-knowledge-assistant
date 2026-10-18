from app.agents.eka.state.graph_state import GraphState
from app.rag.rag_service import RAGService


def create_rag_node(rag_service: RAGService):
    """
    Create the RAG node for the EKA LangGraph workflow.

    The returned rag_node receives GraphState from LangGraph.
    """
    async def node(state: GraphState) -> dict:
        return await rag_node(state, rag_service)

    return node


async def rag_node(state: GraphState, rag_service: RAGService):
    query = state["query"]
    request_id = state["request_id"]
    response = await rag_service.generate_final_answer(
        query=query, request_id=request_id
    )
    return {"response": response}

