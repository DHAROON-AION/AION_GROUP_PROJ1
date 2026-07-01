"""Health check API routes."""

from datetime import datetime, timezone

from fastapi import APIRouter

from backend.core.langfuse import check_langfuse_health
from backend.core.ollama import check_ollama_health
from backend.database.postgres import check_postgres_health
from backend.models.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Aggregate health status across all platform dependencies.

    Returns healthy when all components are up, degraded when some are down,
    and unhealthy when critical components (postgres) fail.
    """
    postgres = check_postgres_health()
    ollama = await check_ollama_health()
    langfuse = await check_langfuse_health()

    components = {
        "postgres": postgres,
        "ollama": ollama,
        "langfuse": langfuse,
    }

    statuses = [c.get("status") for c in components.values()]
    if all(s == "healthy" for s in statuses):
        overall = "healthy"
    elif postgres.get("status") == "unhealthy":
        overall = "unhealthy"
    else:
        overall = "degraded"

    return HealthResponse(
        status=overall,
        timestamp=datetime.now(timezone.utc),
        components=components,
    )


@router.get("/health/live")
async def liveness() -> dict[str, str]:
    """Kubernetes-style liveness probe — process is running."""
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness() -> dict[str, str]:
    """
    Kubernetes-style readiness probe — can serve traffic.

    Requires PostgreSQL to be reachable.
    """
    postgres = check_postgres_health()
    if postgres.get("status") != "healthy":
        return {"status": "not_ready", "reason": "postgres_unavailable"}
    return {"status": "ready"}
