"""Agent framework router — dispatches to LangGraph, Agno, or LangChain."""

import logging
import uuid

from backend.agents.agno_agent import run_agno_agent
from backend.agents.base import AgentInput, AgentOutput
from backend.agents.langchain_agent import run_langchain_agent
from backend.agents.langgraph_agent import run_langgraph_agent
from backend.core.langfuse import get_langfuse_client

logger = logging.getLogger(__name__)

FRAMEWORKS = {
    "langgraph": run_langgraph_agent,
    "agno": run_agno_agent,
    "langchain": run_langchain_agent,
}


async def run_agent(
    message: str,
    session_id: str | None,
    framework: str = "langgraph",
) -> AgentOutput:
    """Route a chat message to the selected agent framework with tracing."""
    session_id = session_id or str(uuid.uuid4())
    framework = framework.lower()
    runner = FRAMEWORKS.get(framework, run_langgraph_agent)

    agent_input = AgentInput(message=message, session_id=session_id)
    langfuse = get_langfuse_client()

    if langfuse:
        try:
            trace = langfuse.trace(
                name=f"chat_{framework}",
                session_id=session_id,
                input={"message": message, "framework": framework},
            )
            span = trace.span(name="agent_run", input=agent_input.__dict__)
            output = await runner(agent_input)
            span.end(output=output.__dict__)
            trace.update(output=output.__dict__)
            return output
        except AttributeError:
            pass
        except Exception as exc:
            logger.warning("Langfuse tracing failed: %s", exc)

    return await runner(agent_input)
