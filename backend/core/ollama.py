"""Ollama local LLM client utilities."""

import logging
from typing import Any

import httpx

from backend.core.config import get_settings

logger = logging.getLogger(__name__)


async def check_ollama_health() -> dict[str, Any]:
    """
    Verify Ollama is reachable and report available models.

    Returns a status dict used by the health endpoint.
    """
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.ollama_base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
            models = [m.get("name") for m in data.get("models", [])]
            return {
                "status": "healthy",
                "url": settings.ollama_base_url,
                "models": models,
                "default_model": settings.ollama_default_model,
            }
    except Exception as exc:
        logger.warning("Ollama health check failed: %s", exc)
        return {
            "status": "unhealthy",
            "url": settings.ollama_base_url,
            "error": str(exc),
        }


async def list_models() -> list[str]:
    """Return a list of model names available in Ollama."""
    health = await check_ollama_health()
    return health.get("models", [])
