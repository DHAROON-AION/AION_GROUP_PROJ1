from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    agent_framework: str = "langchain"

class ChatResponse(BaseModel):
    reply: str
    sources: list[str] = []
    framework_used: str