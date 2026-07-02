"""Vector retrieval with citations from pgvector."""

import logging
from dataclasses import dataclass

from backend.database.postgres import get_db
from backend.rag.embeddings import embed_text

logger = logging.getLogger(__name__)


@dataclass
class RetrievedChunk:
    content: str
    source: str
    score: float


def retrieve_with_citations(query: str, top_k: int = 4) -> list[RetrievedChunk]:
    """
    Retrieve the most relevant document chunks for a query.

    Returns chunks with source citations for grounded answers.
    """
    query_vector = embed_text(query)

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT source, content,
                       1 - (embedding <=> %s::vector) AS score
                FROM document_chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (str(query_vector), str(query_vector), top_k),
            )
            rows = cur.fetchall()

    if not rows:
        return []

    return [
        RetrievedChunk(content=row[1], source=row[0], score=float(row[2]))
        for row in rows
        if float(row[2]) > 0.3
    ]


def format_context(chunks: list[RetrievedChunk]) -> str:
    """Format retrieved chunks as LLM context with citations."""
    if not chunks:
        return ""
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(f"[{i}] Source: {chunk.source}\n{chunk.content}")
    return "\n\n".join(parts)
