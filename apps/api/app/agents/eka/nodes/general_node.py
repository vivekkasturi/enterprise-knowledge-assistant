from app.agents.eka.state.graph_state import GraphState
from app.services.llmservice import LLMService


def create_general_node(llmservice:LLMService):
    
    async def node(state: GraphState):
        return await general_node(state, llmservice)

    return node



async def general_node(state: GraphState, llmservice: LLMService):

    query = state["query"]
    llm_response = await llmservice.generate_response(query)
    return {"response": llm_response}