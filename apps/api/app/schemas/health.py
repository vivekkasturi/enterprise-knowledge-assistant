from typing import Literal
from pydantic import BaseModel

class HealthCheckResponse(BaseModel):
    status: Literal["healthy"]
    service: str
    version: str

class ChatResponse(BaseModel):
    response: str
    
class ChatRequest(BaseModel):
    message: str