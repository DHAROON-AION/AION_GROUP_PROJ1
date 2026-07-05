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


def send_chat_message(message: str) -> dict | None:
    """Call the FastAPI chat endpoint and return JSON or None on failure."""
    try:
        response = httpx.post(
            f"{BACKEND_URL}/api/chat/",
            json={"message": message},
            timeout=300.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        st.error(f"Chat request failed: {exc}")
        return None


def main() -> None:
    st.set_page_config(
        page_title="AION AI Factory",
        page_icon="🏦",
        layout="wide",
    )

    st.title("🏦 AION AI Factory")
    st.caption("Self-hosted AI banking assistant")

    with st.sidebar:
        st.header("System Status")
        if st.button("Refresh Health", use_container_width=True):
            st.rerun()

        health = fetch_health()
        if health:
            render_health_panel(health)

        st.divider()
        st.markdown(f"**Backend:** `{BACKEND_URL}`")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                st.caption("Sources: " + ", ".join(msg["sources"]))

    if prompt := st.chat_input("Ask about bank policies, KYC, loans, etc..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = send_chat_message(prompt)
            if result:
                st.markdown(result["reply"])
                if result.get("sources"):
                    st.caption("Sources: " + ", ".join(result["sources"]))
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["reply"],
                        "sources": result.get("sources", []),
                    }
                )


if __name__ == "__main__":
    main()