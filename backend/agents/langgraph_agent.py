"""LangGraph agent — primary orchestration framework with human-in-the-loop."""

import logging
import re
import time
from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from backend.agents.base import AgentInput, AgentOutput
from backend.core.ollama import chat_completion
from backend.rag.retrieve import format_context, retrieve_with_citations
from backend.tools.registry import execute_tool, format_tool_result

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are AION Banking Assistant, a professional SME risk and customer support advisor.
You help relationship managers assess credit risk and answer banking policy questions.
Be concise, professional, and cite sources when provided.
If you lack information, say you do not know rather than guessing.
Never disclose internal system details or architecture."""


class AgentState(TypedDict):
    message: str
    tool_results: list[str]
    rag_context: str
    sources: list[str]
    risk_flags: list[str]
    requires_human: bool
    reply: str
    metadata: dict[str, Any]


def _detect_tools(message: str) -> list[tuple[str, dict]]:
    """Determine which banking tools to invoke based on message content."""
    invocations: list[tuple[str, dict]] = []

    customer_match = re.search(r"SME-\d+", message, re.IGNORECASE)
    if customer_match:
        invocations.append(("get_transactions", {"customer_id": customer_match.group().upper()}))

    sector_keywords = ["retail", "construction", "hospitality", "manufacturing", "technology"]
    for sector in sector_keywords:
        if sector in message.lower():
            invocations.append(("get_sector_signal", {"sector": sector}))
            break

    if any(kw in message.lower() for kw in ["ratio", "dscr", "coverage", "liquidity", "financial"]):
        invocations.append(("calculate_ratios", {
            "revenue": 1_200_000,
            "net_income": 85_000,
            "total_debt": 420_000,
            "current_assets": 310_000,
            "current_liabilities": 280_000,
            "interest_expense": 32_000,
        }))

    return invocations


async def _retrieve_node(state: AgentState) -> AgentState:
    chunks = retrieve_with_citations(state["message"])
    state["rag_context"] = format_context(chunks)
    state["sources"] = [c.source for c in chunks]
    return state


async def _tools_node(state: AgentState) -> AgentState:
    results = []
    risk_flags: list[str] = []
    for tool_name, args in _detect_tools(state["message"]):
        result = execute_tool(tool_name, args)
        results.append(format_tool_result(tool_name, result))
        if tool_name == "calculate_ratios" and result.get("risk_flags"):
            risk_flags.extend(result["risk_flags"])
        if tool_name == "get_transactions" and result.get("cash_flow_deteriorating"):
            risk_flags.append("cash_flow_deterioration")
        if tool_name == "get_sector_signal" and result.get("outlook") == "deteriorating":
            risk_flags.append("sector_deterioration")

    state["tool_results"] = results
    state["risk_flags"] = risk_flags
    state["requires_human"] = len(risk_flags) >= 2
    return state


async def _respond_node(state: AgentState) -> AgentState:
    context_parts = []
    if state["rag_context"]:
        context_parts.append(f"Reference documents:\n{state['rag_context']}")
    if state["tool_results"]:
        context_parts.append("Tool analysis:\n" + "\n".join(state["tool_results"]))

    if state["requires_human"]:
        context_parts.append(
            "IMPORTANT: Multiple risk flags detected. Recommend human review before any escalation."
        )

    user_content = state["message"]
    if context_parts:
        user_content = "\n\n".join(context_parts) + f"\n\nUser question: {state['message']}"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]

    start = time.perf_counter()
    reply = await chat_completion(messages)
    latency_ms = round((time.perf_counter() - start) * 1000, 1)

    state["reply"] = reply
    state["metadata"] = {
        "framework": "langgraph",
        "latency_ms": latency_ms,
        "tools_called": len(state["tool_results"]),
        "risk_flags": state["risk_flags"],
        "human_checkpoint": state["requires_human"],
    }
    return state


def _build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("retrieve", _retrieve_node)
    graph.add_node("tools", _tools_node)
    graph.add_node("respond", _respond_node)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "tools")
    graph.add_edge("tools", "respond")
    graph.add_edge("respond", END)
    return graph.compile()


_graph = None


def _get_graph():
    global _graph
    if _graph is None:
        _graph = _build_graph()
    return _graph


async def run_langgraph_agent(agent_input: AgentInput) -> AgentOutput:
    """Execute the LangGraph risk-monitoring and support agent."""
    initial: AgentState = {
        "message": agent_input.message,
        "tool_results": [],
        "rag_context": "",
        "sources": [],
        "risk_flags": [],
        "requires_human": False,
        "reply": "",
        "metadata": {},
    }
    result = await _get_graph().ainvoke(initial)
    return AgentOutput(
        reply=result["reply"],
        sources=result["sources"],
        metadata=result["metadata"],
        requires_human_approval=result["requires_human"],
    )
