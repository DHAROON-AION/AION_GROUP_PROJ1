"""
AION AI Factory — Streamlit Frontend

Architecture position:
    User → Streamlit UI → FastAPI Backend → LangGraph Agent → ...
"""

import os
import uuid
from datetime import datetime

import httpx
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

EXAMPLE_QUESTIONS = [
    "What are the KYC requirements?",
    "What is the business loan policy?",
    "What happens if my debit card is lost?",
    "What are the daily fund transfer limits?",
]


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
        st.caption(f"{icon} {name.capitalize()}: {comp_status}")


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
    except httpx.TimeoutException:
        st.error("Request timed out — the model may be under heavy load. Try again.")
        return None
    except Exception as exc:
        st.error(f"Chat request failed: {exc}")
        return None


def render_copy_button(text: str, key: str) -> None:
    """Render a small copy-to-clipboard button using inline JS (no rerun triggered)."""
    escaped = text.replace("\\", "\\\\").replace("`", "\\`").replace("\n", "\\n")
    st.markdown(
        f"""
        <button onclick="navigator.clipboard.writeText(`{escaped}`);
            const el = document.getElementById('copied-{key}');
            el.style.display='inline'; setTimeout(() => el.style.display='none', 1500);"
            style="background:none;border:1px solid #ccc;border-radius:6px;
            padding:2px 8px;font-size:12px;cursor:pointer;color:#666;">
            📋 Copy
        </button>
        <span id="copied-{key}" style="display:none;font-size:12px;color:green;margin-left:6px;">Copied!</span>
        """,
        unsafe_allow_html=True,
    )


def render_message(msg: dict) -> None:
    """Render a single chat message with timestamp, sources, and copy button."""
    role = msg["role"]
    avatar = "🧑" if role == "user" else "🏦"
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg["content"])

        footer_cols = st.columns([1, 1, 6])
        with footer_cols[0]:
            if msg.get("timestamp"):
                st.caption(msg["timestamp"])
        with footer_cols[1]:
            if role == "assistant":
                render_copy_button(msg["content"], msg.get("id", str(uuid.uuid4())))

        sources = msg.get("sources")
        if sources:
            with st.expander(f"📄 Sources ({len(sources)})"):
                for src in sources:
                    st.markdown(f"- `{src}`")


def render_welcome() -> None:
    """Shown when there's no conversation yet."""
    st.markdown(
        """
        <div style="text-align:center; padding: 40px 20px; color:#666;">
            <div style="font-size:48px;">🏦</div>
            <h3 style="margin-top:8px;">Welcome to AION AI Factory</h3>
            <p>Ask me anything about bank policies — KYC, loans, cards, transfers, complaints, and more.<br>
            All answers are grounded in our official documents, with sources cited.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="AION AI Factory",
        page_icon="🏦",
        layout="wide",
    )

    st.markdown(
        """
        <style>
        .stChatMessage { border-radius: 12px; padding: 4px; }
        div[data-testid="stChatInput"] textarea { font-size: 15px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🏦 AION AI Factory")
    st.caption("Self-hosted AI banking assistant — ask about policies, KYC, loans, cards, and more")

    with st.sidebar:
        st.header("System Status")
        if st.button("🔄 Refresh Health", use_container_width=True):
            st.rerun()

        health = fetch_health()
        if health:
            render_health_panel(health)

        st.divider()
        st.markdown(f"**Backend:** `{BACKEND_URL}`")

        st.divider()
        st.subheader("💡 Try asking")
        for q in EXAMPLE_QUESTIONS:
            if st.button(q, use_container_width=True, key=f"example_{q}"):
                st.session_state.pending_question = q

        st.divider()
        if st.button("🗑️ Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None

    if not st.session_state.messages:
        render_welcome()

    for msg in st.session_state.messages:
        render_message(msg)

    prompt = st.chat_input("Ask about bank policies, KYC, loans, etc...")

    if st.session_state.pending_question:
        prompt = st.session_state.pending_question
        st.session_state.pending_question = None

    if prompt:
        now = datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append(
            {"role": "user", "content": prompt, "timestamp": now, "id": str(uuid.uuid4())}
        )
        render_message(st.session_state.messages[-1])

        with st.chat_message("assistant", avatar="🏦"):
            with st.spinner("Thinking..."):
                result = send_chat_message(prompt)
            if result:
                reply_time = datetime.now().strftime("%I:%M %p")
                st.markdown(result["reply"])

                msg_id = str(uuid.uuid4())
                cols = st.columns([1, 1, 6])
                with cols[0]:
                    st.caption(reply_time)
                with cols[1]:
                    render_copy_button(result["reply"], msg_id)

                sources = result.get("sources", [])
                if sources:
                    with st.expander(f"📄 Sources ({len(sources)})"):
                        for src in sources:
                            st.markdown(f"- `{src}`")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["reply"],
                        "sources": sources,
                        "timestamp": reply_time,
                        "id": msg_id,
                    }
                )


if __name__ == "__main__":
    main()