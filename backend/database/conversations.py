"""Conversation persistence layer."""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from backend.database.postgres import get_db

logger = logging.getLogger(__name__)


def create_conversation(title: str = "New conversation") -> str:
    """Create a new conversation and return its ID."""
    conv_id = str(uuid.uuid4())
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO conversations (id, title) VALUES (%s, %s)",
                (conv_id, title),
            )
    return conv_id


def save_message(
    conversation_id: str,
    role: str,
    content: str,
    sources: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> str:
    """Persist a chat message."""
    msg_id = str(uuid.uuid4())
    import json
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO messages (id, conversation_id, role, content, sources, metadata)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    msg_id,
                    conversation_id,
                    role,
                    content,
                    json.dumps(sources or []),
                    json.dumps(metadata or {}),
                ),
            )
            cur.execute(
                "UPDATE conversations SET updated_at = %s WHERE id = %s",
                (datetime.now(timezone.utc), conversation_id),
            )
    return msg_id


def get_conversations(limit: int = 20) -> list[dict[str, Any]]:
    """List recent conversations."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.id, c.title, c.updated_at,
                       (SELECT content FROM messages m
                        WHERE m.conversation_id = c.id
                        ORDER BY m.created_at DESC LIMIT 1) AS preview
                FROM conversations c
                ORDER BY c.updated_at DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
    return [
        {
            "id": row[0],
            "title": row[1],
            "updated_at": row[2].isoformat() if row[2] else "",
            "preview": row[3] or "",
        }
        for row in rows
    ]


def get_messages(conversation_id: str) -> list[dict[str, Any]]:
    """Retrieve all messages for a conversation."""
    import json
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, role, content, sources, created_at
                FROM messages
                WHERE conversation_id = %s
                ORDER BY created_at ASC
                """,
                (conversation_id,),
            )
            rows = cur.fetchall()
    return [
        {
            "id": row[0],
            "role": row[1],
            "content": row[2],
            "sources": json.loads(row[3]) if row[3] else [],
            "timestamp": row[4].strftime("%I:%M %p") if row[4] else "",
        }
        for row in rows
    ]
