"""
AION AI Factory — Streamlit Frontend

Architecture position:
    User → Streamlit UI → FastAPI Backend → LangGraph Agent → ...
"""

import os

import httpx
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def fetch_health() -> dict | None:
    """Call the FastAPI health endpoint and return JSON or None on failure."""
    try:
        response = httpx.get(f"{BACKEND_URL}/health", timeout=10.0)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        st.error(f"Cannot reach backend at {BACKEND_URL}: {exc}")
        return None


def render_health_panel(health: dict) -> None:
    """Display component health status in the sidebar."""
    status = health.get("status", "unknown")
    color = {"healthy": "green", "degraded": "orange", "unhealthy": "red"}.get(
        status, "gray"
    )
    st.markdown(f"**Platform status:** :{color}[{status.upper()}]")

    components = health.get("components", {})
    for name, info in components.items():
        comp_status = info.get("status", "unknown")
        icon = "✅" if comp_status == "healthy" else "⚠️"
        st.caption(f"{icon} {name}: {comp_status}")


def main() -> None:
    st.set_page_config(
        page_title="AION AI Factory",
        page_icon="🏦",
        layout="wide",
    )

    st.title("🏦 AION AI Factory")
    st.caption("Self-hosted AI platform for banking — Phase 1 Infrastructure")

    with st.sidebar:
        st.header("System Status")
        if st.button("Refresh Health", use_container_width=True):
            st.rerun()

        health = fetch_health()
        if health:
            render_health_panel(health)

        st.divider()
        st.markdown(f"**Backend:** `{BACKEND_URL}`")

    st.info(
        "Phase 1 complete: Docker infrastructure is running. "
        "Chat, agents, and RAG will be enabled in upcoming phases."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Phase", "1 / 10", "Infrastructure")
    with col2:
        st.metric("Agent Framework", "—", "Phase 3")
    with col3:
        st.metric("RAG", "—", "Phase 5")

    st.subheader("Chat (Coming in Phase 6)")
    st.text_input(
        "Message",
        placeholder="Chat will be available after LangGraph agent is implemented...",
        disabled=True,
    )

    st.subheader("Quick Links")
    link_col1, link_col2, link_col3 = st.columns(3)
    with link_col1:
        st.markdown(f"[API Docs]({BACKEND_URL}/docs)")
    with link_col2:
        st.markdown("[Langfuse](http://localhost:3000)")
    with link_col3:
        st.markdown("[Health Check](http://localhost:8000/health)")


if __name__ == "__main__":
    main()
