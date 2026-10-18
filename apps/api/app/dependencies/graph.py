from app.agents.eka.graph.graph import build_eka_graph
from app.dependencies.llm import llm_service
from app.dependencies.rag import rag_service


eka_graph = build_eka_graph(
    llmservice=llm_service,
    rag_service=rag_service,
)

