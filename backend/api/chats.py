"""Chat session persistence API — save, list, and load conversation history."""

import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, String, Text, DateTime, desc

from backend.database.postgres import Base, engine, SessionLocal

router = APIRouter(prefix="/chats", tags=["chats"])


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, default="New chat")
    messages_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Idempotent — only creates the table if it doesn't already exist. Doesn't
# touch any other tables (e.g. extracted_invoices) defined in postgres.py.
Base.metadata.create_all(bind=engine)


class ChatSessionSummary(BaseModel):
    id: str
    title: str
    updated_at: datetime


class ChatSessionDetail(BaseModel):
    id: str
    title: str
    messages: list[dict]
    updated_at: datetime


class ChatSessionSave(BaseModel):
    title: Optional[str] = None
    messages: list[dict]


def _derive_title(messages: list[dict]) -> str:
    """Generate a short title from the first user message."""
    for msg in messages:
        if msg.get("role") == "user":
            text = msg.get("content", "").strip()
            return (text[:40] + "…") if len(text) > 40 else (text or "New chat")
    return "New chat"


@router.get("/", response_model=list[ChatSessionSummary])
async def list_chats():
    """Return all saved chat sessions, most recently updated first."""
    db = SessionLocal()
    try:
        sessions = db.query(ChatSession).order_by(desc(ChatSession.updated_at)).all()
        return [
            ChatSessionSummary(id=s.id, title=s.title, updated_at=s.updated_at)
            for s in sessions
        ]
    finally:
        db.close()


@router.get("/{chat_id}", response_model=ChatSessionDetail)
async def get_chat(chat_id: str):
    """Return one chat session's full message history."""
    db = SessionLocal()
    try:
        session = db.query(ChatSession).filter(ChatSession.id == chat_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Chat not found")
        return ChatSessionDetail(
            id=session.id,
            title=session.title,
            messages=json.loads(session.messages_json),
            updated_at=session.updated_at,
        )
    finally:
        db.close()


@router.post("/{chat_id}", response_model=ChatSessionSummary)
async def save_chat(chat_id: str, payload: ChatSessionSave):
    """Create or update a chat session's messages."""
    db = SessionLocal()
    try:
        session = db.query(ChatSession).filter(ChatSession.id == chat_id).first()
        title = payload.title or _derive_title(payload.messages)

        if session:
            session.messages_json = json.dumps(payload.messages)
            session.title = title
        else:
            session = ChatSession(
                id=chat_id,
                title=title,
                messages_json=json.dumps(payload.messages),
            )
            db.add(session)

        db.commit()
        db.refresh(session)
        return ChatSessionSummary(id=session.id, title=session.title, updated_at=session.updated_at)
    finally:
        db.close()


@router.delete("/{chat_id}")
async def delete_chat(chat_id: str):
    """Delete a chat session."""
    db = SessionLocal()
    try:
        session = db.query(ChatSession).filter(ChatSession.id == chat_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Chat not found")
        db.delete(session)
        db.commit()
        return {"status": "deleted"}
    finally:
        db.close()