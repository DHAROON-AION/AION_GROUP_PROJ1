"""Chat API"""

from fastapi import APIRouter

from backend.agents.langgraph_agent import banking_agent
from backend.models.schemas import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):

    result = banking_agent.invoke(
        {
            "question": request.message,
            "answer": "",
            "sources": [],
            "sentiment": "",
        }
    )

    return ChatResponse(
        reply=result["answer"],
        sources=result["sources"],
        sentiment=result["sentiment"],
        framework_used="langgraph",
    )