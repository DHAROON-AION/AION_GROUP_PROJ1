"""Langfuse observability integration."""

import logging
from typing import Any

import httpx

from backend.core.config import get_settings

logger = logging.getLogger(__name__)

_langfuse_client = None


def get_langfuse_client():
    """
    Return a Langfuse client if credentials are configured.

    Returns None when Langfuse is disabled or keys are not set,
    allowing the app to run without observability during bootstrap.
    """
    global _langfuse_client

    settings = get_settings()
    if not settings.langfuse_enabled:
        return None

    if not settings.langfuse_public_key or not settings.langfuse_secret_key:
        logger.info("Langfuse keys not configured; tracing disabled")
        return None

    if _langfuse_client is None:
        try:
            from langfuse import Langfuse

            _langfuse_client = Langfuse(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_host,
            )
        except Exception as exc:
            logger.warning("Failed to initialize Langfuse client: %s", exc)
            return None

    return _langfuse_client


async def check_langfuse_health() -> dict[str, Any]:
    """Verify Langfuse web UI is reachable."""
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.langfuse_host}/api/public/health")
            response.raise_for_status()
            return {
                "status": "healthy",
                "url": settings.langfuse_host,
                "enabled": settings.langfuse_enabled,
            }
    except Exception as exc:
        logger.warning("Langfuse health check failed: %s", exc)
        return {
            "status": "unhealthy",
            "url": settings.langfuse_host,
            "enabled": settings.langfuse_enabled,
            "error": str(exc),
        }
