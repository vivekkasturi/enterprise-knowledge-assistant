from typing import Literal, TypedDict

class GraphState(TypedDict):
    query: str
    request_id: str
    route: Literal["RAG", "GENERAL"] | None
    response: str | None
    error: str | None