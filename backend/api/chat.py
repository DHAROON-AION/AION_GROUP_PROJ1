"""Chat API routes — Phase 2+ implementation."""

from fastapi import APIRouter, HTTPException

from backend.models.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message through the selected agent framework.

    TODO (Phase 3): Wire LangGraph agent as primary orchestrator.
    TODO (Phase 3): Wire Agno agent for framework comparison.
    TODO (Phase 3): Optional LangChain minimal implementation.
    """
    raise HTTPException(
        status_code=501,
        detail=(
            f"Chat endpoint not yet implemented for framework "
            f"'{request.agent_framework}'. See Phase 3 roadmap."
        ),
    )
