"""Document ingestion pipeline — chunk, embed, and store in pgvector."""

import logging
import uuid
from pathlib import Path

from backend.database.postgres import get_db
from backend.rag.embeddings import embed_texts

logger = logging.getLogger(__name__)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def _chunk_text(text: str, source: str) -> list[dict]:
    """Split document text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()
        if chunk:
            chunks.append({"content": chunk, "source": source})
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def _source_already_ingested(source: str) -> bool:
    """Skip re-embedding when this document was ingested in a previous run."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM document_chunks WHERE source = %s LIMIT 1",
                (source,),
            )
            return cur.fetchone() is not None


def delete_source_chunks(source: str) -> int:
    """Remove all vector chunks for a document source. Returns rows deleted."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM document_chunks WHERE source = %s", (source,))
            deleted = cur.rowcount
    return deleted


def ingest_file(file_path: Path, *, force: bool = False) -> int:
    """Ingest a single document file into the vector store. Returns chunk count."""
    if not force and _source_already_ingested(file_path.name):
        logger.info("Skipping already ingested document: %s", file_path.name)
        return 0

    if force and _source_already_ingested(file_path.name):
        delete_source_chunks(file_path.name)

    text = file_path.read_text(encoding="utf-8", errors="ignore")
    chunks = _chunk_text(text, source=file_path.name)
    if not chunks:
        return 0

    contents = [c["content"] for c in chunks]
    vectors = embed_texts(contents)

    with get_db() as conn:
        with conn.cursor() as cur:
            for chunk, vector in zip(chunks, vectors):
                cur.execute(
                    """
                    INSERT INTO document_chunks (id, source, content, embedding, metadata)
                    VALUES (%s, %s, %s, %s::vector, %s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (
                        str(uuid.uuid4()),
                        chunk["source"],
                        chunk["content"],
                        str(vector),
                        "{}",
                    ),
                )
    logger.info("Ingested %d chunks from %s", len(chunks), file_path.name)
    return len(chunks)


def ingest_directory(directory: Path) -> dict[str, int]:
    """Ingest all supported documents from a directory."""
    results: dict[str, int] = {}
    if not directory.exists():
        logger.warning("Documents directory not found: %s", directory)
        return results

    for pattern in ("*.md", "*.txt"):
        for file_path in directory.glob(pattern):
            results[file_path.name] = ingest_file(file_path)
    return results
