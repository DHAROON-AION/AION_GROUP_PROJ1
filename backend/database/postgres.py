"""PostgreSQL database connection and health utilities."""

import logging
from contextlib import contextmanager
from typing import Any, Generator

import psycopg2
from psycopg2.extensions import connection as PgConnection

from backend.core.config import get_settings

logger = logging.getLogger(__name__)


def get_connection() -> PgConnection:
    """Create a new PostgreSQL connection using application settings."""
    settings = get_settings()
    return psycopg2.connect(settings.database_url)


@contextmanager
def get_db() -> Generator[PgConnection, None, None]:
    """
    Context manager that yields a database connection and ensures cleanup.

    Usage:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def check_postgres_health() -> dict[str, Any]:
    """Verify PostgreSQL connectivity and pgvector extension availability."""
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]

                cur.execute(
                    "SELECT EXISTS("
                    "  SELECT 1 FROM pg_extension WHERE extname = 'vector'"
                    ")"
                )
                pgvector_installed = cur.fetchone()[0]

        return {
            "status": "healthy",
            "pgvector": bool(pgvector_installed),
            "version": version.split(",")[0],
        }
    except Exception as exc:
        logger.warning("PostgreSQL health check failed: %s", exc)
        return {
            "status": "unhealthy",
            "error": str(exc),
        }


def init_database() -> None:
    """
    Ensure required extensions and application tables exist on startup.

    Called once during backend boot; idempotent via IF NOT EXISTS.
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS document_chunks (
                        id TEXT PRIMARY KEY,
                        source TEXT NOT NULL,
                        content TEXT NOT NULL,
                        embedding vector(384),
                        metadata JSONB DEFAULT '{}'
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id TEXT PRIMARY KEY,
                        title TEXT NOT NULL DEFAULT 'New conversation',
                        created_at TIMESTAMPTZ DEFAULT NOW(),
                        updated_at TIMESTAMPTZ DEFAULT NOW()
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id TEXT PRIMARY KEY,
                        conversation_id TEXT REFERENCES conversations(id),
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        sources JSONB DEFAULT '[]',
                        metadata JSONB DEFAULT '{}',
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    )
                """)
        logger.info("Database schema initialized")
    except Exception as exc:
        logger.error("Database initialization failed: %s", exc)
        raise
