"""Chat API routes."""

import json
import logging
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.agents.router import run_agent
from backend.core.ollama import chat_completion_stream
from backend.database.conversations import (
    create_conversation,
    get_conversations,
    get_messages,
    save_message,
)
from backend.guardrails.pipeline import process_input, process_output
from backend.models.schemas import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat message through the selected agent framework."""
    sanitized, input_meta = process_input(request.message)

    if input_meta.get("blocked"):
        session_id = request.session_id or str(uuid.uuid4())
        return ChatResponse(
            reply=sanitized,
            session_id=session_id,
            agent_framework=request.agent_framework,
            metadata={"blocked": True, **input_meta},
        )

    session_id = request.session_id or create_conversation(
        title=request.message[:60]
    )

    save_message(session_id, "user", sanitized)

    try:
        output = await run_agent(
            message=sanitized,
            session_id=session_id,
            framework=request.agent_framework,
        )
    except Exception as exc:
        logger.exception("Agent execution failed")
        raise HTTPException(status_code=500, detail=f"Assistant unavailable: {exc}") from exc

    reply, output_meta = process_output(output.reply)
    metadata = {**output.metadata, **input_meta, **output_meta}

    save_message(session_id, "assistant", reply, output.sources, metadata)

    return ChatResponse(
        reply=reply,
        session_id=session_id,
        agent_framework=request.agent_framework,
        sources=output.sources,
        metadata=metadata,
    )


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """Stream a chat response token-by-token via Server-Sent Events."""
    sanitized, input_meta = process_input(request.message)

    if input_meta.get("blocked"):
        async def blocked_stream():
            yield f"data: {json.dumps({'type': 'token', 'content': sanitized})}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'blocked': True})}\n\n"

        return StreamingResponse(blocked_stream(), media_type="text/event-stream")

    session_id = request.session_id or create_conversation(title=request.message[:60])
    save_message(session_id, "user", sanitized)

    async def event_stream():
        full_reply = ""
        messages = [
            {"role": "system", "content": "You are AION Banking Assistant. Be professional and concise."},
            {"role": "user", "content": sanitized},
        ]
        try:
            async for token in chat_completion_stream(messages):
                full_reply += token
                yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"

            reply, output_meta = process_output(full_reply)
            save_message(session_id, "assistant", reply, metadata=output_meta)
            yield f"data: {json.dumps({'type': 'done', 'session_id': session_id, 'metadata': output_meta})}\n\n"
        except Exception as exc:
            yield f"data: {json.dumps({'type': 'error', 'message': str(exc)})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/conversations")
async def list_conversations():
    """Return recent conversation history."""
    return {"conversations": get_conversations()}


@router.get("/conversations/{conversation_id}/messages")
async def conversation_messages(conversation_id: str):
    """Return messages for a specific conversation."""
    return {"messages": get_messages(conversation_id)}
