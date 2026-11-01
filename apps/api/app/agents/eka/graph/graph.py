from langgraph.graph import StateGraph, START, END
from app.agents.eka.nodes.router_node import create_router_node
from app.agents.eka.nodes.rag_node import create_rag_node
from app.agents.eka.nodes.general_node import create_general_node
from app.agents.eka.state.graph_state import GraphState
from app.services.llmservice import LLMService
from app.rag.rag_service import RAGService


def build_eka_graph(
    llmservice: LLMService,
    rag_service: RAGService,
):
    builder = StateGraph(GraphState)

    # Inject already-created services into nodes
    router = create_router_node(llmservice)
    rag = create_rag_node(rag_service)
    general = create_general_node(llmservice)

    # Register nodes
    builder.add_node("router", router)
    builder.add_node("rag", rag)
    builder.add_node("general", general)

    # Start -> Router
    builder.add_edge(START, "router")

    def route_query(state: GraphState) -> str:
        return state["route"]

    # Router decision
    builder.add_conditional_edges(
        "router",
        route_query,
        {
            "RAG": "rag",
            "GENERAL": "general",
        },
    )

    # Finish
    builder.add_edge("rag", END)
    builder.add_edge("general", END)

    return builder.compile()