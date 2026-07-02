"""Shared agent request/response contracts."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentInput:
    message: str
    session_id: str
    conversation_history: list[dict[str, str]] = field(default_factory=list)


@dataclass
class AgentOutput:
    reply: str
    sources: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    requires_human_approval: bool = False
