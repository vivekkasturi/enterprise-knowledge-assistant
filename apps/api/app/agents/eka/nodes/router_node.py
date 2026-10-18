from app.prompts.router_prompt import build_router_messages
from app.agents.eka.state.graph_state import GraphState
from app.services.llmservice import LLMService


def create_router_node(llmservice: LLMService):
    """
    Create the router node for the EKA LangGraph workflow.

    The LLMService is injected when the graph is created.
    The returned router_node receives GraphState from LangGraph.
    """
    async def node(state: GraphState) -> dict:
        return await router_node(state, llmservice)

    return node
   

async def router_node(state: GraphState, llmservice: LLMService) -> dict:
        """
        Classify the user's query and update the graph route.

        Returns:
            A partial GraphState update containing either
            "RAG" or "GENERAL".
        """

        query = state["query"].strip()

        messages = build_router_messages(query)

        response = await llmservice.generate(messages)

        print("ROUTER QUERY:", query)
        print("ROUTER RAW RESPONSE:", repr(response))

        route = response.strip().upper()

        if route not in {"RAG", "GENERAL"}:
            raise ValueError(
                f"Invalid route: {route}. Expected 'RAG' or 'GENERAL'."
            )
        
        return {"route": route}
