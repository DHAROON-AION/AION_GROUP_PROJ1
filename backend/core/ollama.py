"""Ollama local LLM client utilities."""

import json
import logging
from collections.abc import AsyncIterator
from typing import Any

import httpx

from backend.core.config import get_settings

logger = logging.getLogger(__name__)


async def check_ollama_health() -> dict[str, Any]:
    """Verify Ollama is reachable and report available models."""
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


async def chat_completion(
    messages: list[dict[str, str]],
    model: str | None = None,
    temperature: float = 0.3,
) -> str:
    """Send a chat completion request to Ollama and return the assistant reply."""
    settings = get_settings()
    model = model or settings.ollama_default_model
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
    }
    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(
            f"{settings.ollama_base_url}/api/chat",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "")


async def chat_completion_stream(
    messages: list[dict[str, str]],
    model: str | None = None,
    temperature: float = 0.3,
) -> AsyncIterator[str]:
    """Stream chat tokens from Ollama."""
    settings = get_settings()
    model = model or settings.ollama_default_model
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {"temperature": temperature},
    }
    async with httpx.AsyncClient(timeout=300.0) as client:
        async with client.stream(
            "POST",
            f"{settings.ollama_base_url}/api/chat",
            json=payload,
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                try:
                    chunk = json.loads(line)
                    content = chunk.get("message", {}).get("content", "")
                    if content:
                        yield content
                except json.JSONDecodeError:
                    continue
