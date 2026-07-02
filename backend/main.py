"""
AION AI Factory — FastAPI Application Entry Point

Architecture position:
    React UI → FastAPI → LangGraph Agent → Tools/MCP → Ollama → pgvector → Langfuse
"""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import chat, documents, health
from backend.core.config import get_settings
from backend.database.postgres import init_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown hooks for the FastAPI application."""
    settings = get_settings()
    logger.info("Starting %s [%s]", settings.app_name, settings.app_env)

    try:
        init_database()
        logger.info("PostgreSQL + pgvector ready")

        import asyncio
        from pathlib import Path

        from backend.rag.ingest import ingest_directory

        docs_dir = Path("/app/documents")

        async def ingest_in_background() -> None:
            if not docs_dir.exists() or not any(docs_dir.glob("*.md")):
                return
            try:
                results = await asyncio.to_thread(ingest_directory, docs_dir)
                logger.info("Document ingestion: %s", results)
            except Exception as exc:
                logger.error("Background document ingestion failed: %s", exc)

        asyncio.create_task(ingest_in_background())
    except Exception as exc:
        logger.error("Database init failed (will retry on health checks): %s", exc)

    yield

    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    """Application factory — keeps testability and modularity clean."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Self-hosted AI Factory platform for banking environments",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(chat.router, prefix="/api")
    app.include_router(documents.router, prefix="/api")

    @app.get("/")
    async def root():
        return {
            "service": settings.app_name,
            "status": "running",
            "docs": "/docs",
            "health": "/health",
        }

    return app


app = create_app()
