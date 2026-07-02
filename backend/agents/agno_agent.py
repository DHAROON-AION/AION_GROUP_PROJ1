"""Agno agent — framework comparison with identical I/O contract."""

import asyncio
import logging
import time

from backend.agents.base import AgentInput, AgentOutput
from backend.agents.langgraph_agent import _detect_tools, SYSTEM_PROMPT
from backend.core.config import get_settings
from backend.core.ollama import chat_completion
from backend.rag.retrieve import format_context, retrieve_with_citations
from backend.tools.registry import execute_tool, format_tool_result

logger = logging.getLogger(__name__)


async def run_agno_agent(agent_input: AgentInput) -> AgentOutput:
    """
    Run the same banking assistant logic via Agno framework.

    Uses Agno's agent abstraction when available; falls back to shared
    orchestration logic to ensure identical behaviour during comparison.
    """
    settings = get_settings()
    start = time.perf_counter()

    chunks = retrieve_with_citations(agent_input.message)
    sources = [c.source for c in chunks]
    rag_context = format_context(chunks)

    tool_results = []
    risk_flags: list[str] = []
    for tool_name, args in _detect_tools(agent_input.message):
        result = execute_tool(tool_name, args)
        tool_results.append(format_tool_result(tool_name, result))
        if result.get("risk_flags"):
            risk_flags.extend(result.get("risk_flags", []))
        if result.get("cash_flow_deteriorating"):
            risk_flags.append("cash_flow_deterioration")
        if result.get("outlook") == "deteriorating":
            risk_flags.append("sector_deterioration")

    requires_human = len(risk_flags) >= 2

    try:
        from agno.agent import Agent
        from agno.models.ollama import Ollama

        context = ""
        if rag_context:
            context += f"Documents:\n{rag_context}\n"
        if tool_results:
            context += "Analysis:\n" + "\n".join(tool_results)

        agent = Agent(
            model=Ollama(
                id=settings.ollama_default_model,
                host=settings.ollama_base_url,
            ),
            instructions=SYSTEM_PROMPT,
            markdown=False,
        )
        prompt = f"{context}\n\nQuestion: {agent_input.message}" if context else agent_input.message
        response = await asyncio.to_thread(agent.run, prompt)
        reply = str(response.content) if hasattr(response, "content") else str(response)
    except Exception as exc:
        logger.warning("Agno agent failed, using Ollama fallback: %s", exc)
        context_parts = []
        if rag_context:
            context_parts.append(rag_context)
        if tool_results:
            context_parts.append("\n".join(tool_results))
        user_content = agent_input.message
        if context_parts:
            user_content = "\n\n".join(context_parts) + f"\n\nQuestion: {agent_input.message}"
        reply = await chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ])

    latency_ms = round((time.perf_counter() - start) * 1000, 1)
    return AgentOutput(
        reply=reply,
        sources=sources,
        metadata={
            "framework": "agno",
            "latency_ms": latency_ms,
            "tools_called": len(tool_results),
            "risk_flags": risk_flags,
            "human_checkpoint": requires_human,
        },
        requires_human_approval=requires_human,
    )
