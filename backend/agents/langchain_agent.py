"""LangChain minimal agent — optional framework comparison."""

import logging
import time

from backend.agents.base import AgentInput, AgentOutput
from backend.agents.langgraph_agent import _detect_tools, SYSTEM_PROMPT
from backend.core.config import get_settings
from backend.core.ollama import chat_completion
from backend.rag.retrieve import format_context, retrieve_with_citations
from backend.tools.registry import execute_tool, format_tool_result

logger = logging.getLogger(__name__)


async def run_langchain_agent(agent_input: AgentInput) -> AgentOutput:
    """Minimal LangChain agent implementation for framework bake-off."""
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

    requires_human = len(risk_flags) >= 2

    try:
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_ollama import ChatOllama

        llm = ChatOllama(
            model=settings.ollama_default_model,
            base_url=settings.ollama_base_url,
            temperature=0.3,
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "{input}"),
        ])
        chain = prompt | llm

        context = agent_input.message
        if rag_context or tool_results:
            parts = []
            if rag_context:
                parts.append(rag_context)
            if tool_results:
                parts.append("\n".join(tool_results))
            context = "\n\n".join(parts) + f"\n\nQuestion: {agent_input.message}"

        response = await chain.ainvoke({"input": context})
        reply = response.content if hasattr(response, "content") else str(response)
    except Exception as exc:
        logger.warning("LangChain agent failed, using Ollama fallback: %s", exc)
        reply = await chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": agent_input.message},
        ])

    latency_ms = round((time.perf_counter() - start) * 1000, 1)
    return AgentOutput(
        reply=reply,
        sources=sources,
        metadata={
            "framework": "langchain",
            "latency_ms": latency_ms,
            "tools_called": len(tool_results),
            "risk_flags": risk_flags,
            "human_checkpoint": requires_human,
        },
        requires_human_approval=requires_human,
    )
