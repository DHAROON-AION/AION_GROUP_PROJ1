from datetime import datetime
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    agent_framework: str = "langchain"

class ChatResponse(BaseModel):
    reply: str
    sources: list[str] = []
    sentiment: str = ""
    framework_used: str

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    components: dict