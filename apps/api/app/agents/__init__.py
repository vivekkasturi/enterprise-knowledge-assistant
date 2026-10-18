from typing import TypedDict, Literal

class GraphState(TypedDict):
    """Graph state representation."""
    query: str
    request_id: str
    route: Literal ["RAG", "GENERAL"] | None
    response: str | None
    error: str | None
