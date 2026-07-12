"""
AION AI Factory — Streamlit Frontend
Restyled to match the BSF Business Banking "Customer Intelligence Engine" UI concept
(navy sidebar, teal accents, card-based chat bubbles).

Architecture position:
    User → Streamlit UI → FastAPI Backend → LangGraph Agent → ...
"""
from PIL import Image 
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

# ---------------------------------------------------------------------------
# BSF-inspired design tokens
# ---------------------------------------------------------------------------
NAVY = "#0A272D"          # sidebar / header background
NAVY_LIGHT = "#173B5C"    # hover / active row background
TEAL = "#14B8A6"          # primary accent (buttons, active tab, links)
TEAL_DARK = "#0E9488"
BG = "#F4F6F8"            # main content background
CARD = "#FFFFFF"
TEXT_DARK = "#0F2A44"
TEXT_MUTED = "#6B7280"
BORDER = "#E6E9EE"
USER_BUBBLE = "#0E2A44"
ASSISTANT_BUBBLE = "#EFF7F6"


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"], [data-testid="stAppViewContainer"], 
        [data-testid="stAppViewContainer"] *, 
        [data-testid="stSidebar"] *,
        .app-header, .app-header h1, .app-header p,
        .welcome-card, .welcome-card h3, .welcome-card p,
        .bubble, .msg-meta, .powered-by,
        div[data-testid="stChatInput"] textarea,
        div[data-testid="stChatInput"] * {{
        font-family: 'Times New Roman', Times, serif !important;
        }}

        /* Restore icon font for Material Symbols icons (sidebar collapse arrow, etc.) */
        [data-testid="stIconMaterial"],
        span[class*="material-symbols"],
        [data-testid="stSidebarCollapseButton"] * {{
            font-family: 'Material Symbols Outlined', 'Material Symbols Rounded', sans-serif !important;
        }}

        /* ---- App background ---- */
        [data-testid="stAppViewContainer"] > .main {{
            background-color: {BG};
        }}

        /* ---- Sidebar ---- */
        [data-testid="stSidebar"] {{
            background-color: {NAVY};
        }}
        [data-testid="stSidebar"] * {{
            color: #E7ECF2 !important;
        }}
        [data-testid="stSidebar"] hr {{
            border-color: {NAVY_LIGHT};
        }}

        /* Sidebar buttons look like nav rows, not default Streamlit buttons */
        [data-testid="stSidebar"] .stButton > button {{
            background-color: transparent;
            border: 1px solid transparent;
            text-align: left;
            border-radius: 8px;
            font-weight: 500;
            padding: 0.4rem 0.6rem;
        }}
        [data-testid="stSidebar"] .stButton > button:hover {{
            background-color: {NAVY_LIGHT};
            border-color: {NAVY_LIGHT};
        }}

        /* Primary "New chat" icon button, top-right of sidebar header */
        [data-testid="stSidebar"] .new-chat-btn .stButton > button {{
            background-color: {TEAL};
            color: #FFFFFF !important;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            padding: 0.35rem 0.6rem;
            text-align: center;
        }}
        [data-testid="stSidebar"] .new-chat-btn .stButton > button:hover {{
            background-color: {TEAL_DARK};
        }}

        /* Sidebar brand row */
        .sidebar-brand {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 800;
            font-size: 1.6rem;
            font-family: 'Times New Roman', Times, serif;
            letter-spacing: 0.02em;
            padding-top: 4px;
        }}
        .sidebar-brand .badge {{
            background: {TEAL};
            color: #06231F;
            font-size: 0.7rem;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 4px;
            letter-spacing: 0.04em;
        }}

        /* ---- Main header (mimics BSF top bar) ---- */
        .app-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 1px solid {BORDER};
            padding-bottom: 14px;
            margin-bottom: 18px;
        }}
        .app-header h1 {{
            color: {TEXT_DARK};
            font-size: 1.7rem;
            font-weight: 800;
            margin: 0;
        }}
        .app-header p {{
            color: {TEXT_MUTED};
            font-size: 0.9rem;
            margin: 2px 0 0 0;
        }}
        .powered-by {{
            color: {TEXT_MUTED};
            font-size: 0.75rem;
            text-align: right;
        }}
        .powered-by b {{
            color: {TEAL_DARK};
        }}

        /* ---- Chat bubbles ---- */
        .msg-row {{
            display: flex;
            margin: 10px 0;
        }}
        .msg-row.user {{ justify-content: flex-end; }}
        .msg-row.assistant {{ justify-content: flex-start; }}

        .bubble {{
            max-width: 72%;
            padding: 12px 16px;
            border-radius: 14px;
            font-size: 0.95rem;
            line-height: 1.5;
        }}
        .bubble.user {{
            background: {USER_BUBBLE};
            color: #FFFFFF;
            border-bottom-right-radius: 4px;
        }}
        .bubble.assistant {{
            background: {ASSISTANT_BUBBLE};
            color: {TEXT_DARK};
            border: 1px solid #DCEFEC;
            border-bottom-left-radius: 4px;
        }}
        .msg-meta {{
            font-size: 0.7rem;
            color: {TEXT_MUTED};
            margin-top: 2px;
        }}
        .msg-row.user + .msg-meta {{ text-align: right; }}

        /* Welcome card */
        .welcome-card {{
            text-align: center;
            padding: 48px 20px;
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 14px;
            color: {TEXT_MUTED};
        }}
        .welcome-card h3 {{ color: {TEXT_DARK}; margin-top: 10px; }}

        /* Chat input */
        div[data-testid="stChatInput"] {{
            border-top: 1px solid {BORDER};
        }}
        div[data-testid="stChatInput"] textarea {{
            font-size: 15px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Backend calls
# ---------------------------------------------------------------------------
def fetch_health() -> dict | None:
    try:
        response = httpx.get(f"{BACKEND_URL}/health", timeout=10.0)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        st.error(f"Cannot reach backend at {BACKEND_URL}: {exc}")
        return None


def render_health_panel(health: dict) -> None:
    status = health.get("status", "unknown")
    color = {"healthy": "🟢", "degraded": "🟠", "unhealthy": "🔴"}.get(status, "⚪")
    st.markdown(f"**Platform status:** {color} {status.upper()}")
    components = health.get("components", {})
    for name, info in components.items():
        comp_status = info.get("status", "unknown")
        icon = "✅" if comp_status == "healthy" else "⚠️"
        st.caption(f"{icon} {name.capitalize()}: {comp_status}")


def send_chat_message(message: str) -> dict | None:
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


def list_saved_chats() -> list[dict]:
    try:
        response = httpx.get(f"{BACKEND_URL}/api/chats/", timeout=10.0)
        response.raise_for_status()
        return response.json()
    except Exception:
        return []


def load_saved_chat(chat_id: str) -> dict | None:
    try:
        response = httpx.get(f"{BACKEND_URL}/api/chats/{chat_id}", timeout=10.0)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def save_current_chat() -> None:
    """Persist the current conversation to the backend."""
    if not st.session_state.messages:
        return
    try:
        httpx.post(
            f"{BACKEND_URL}/api/chats/{st.session_state.chat_id}",
            json={"messages": st.session_state.messages},
            timeout=10.0,
        )
    except Exception:
        pass  # saving failures shouldn't interrupt the chat experience


def delete_saved_chat(chat_id: str) -> None:
    try:
        httpx.delete(f"{BACKEND_URL}/api/chats/{chat_id}", timeout=10.0)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
def render_copy_button(text: str, key: str) -> None:
    escaped = text.replace("\\", "\\\\").replace("`", "\\`").replace("\n", "\\n")
    st.markdown(
        f"""
        <button onclick="navigator.clipboard.writeText(`{escaped}`);
            const el = document.getElementById('copied-{key}');
            el.style.display='inline'; setTimeout(() => el.style.display='none', 1500);"
            style="background:none;border:1px solid {BORDER};border-radius:6px;
            padding:2px 8px;font-size:11px;cursor:pointer;color:{TEXT_MUTED};">
            📋 Copy
        </button>
        <span id="copied-{key}" style="display:none;font-size:11px;color:{TEAL_DARK};margin-left:6px;">Copied!</span>
        """,
        unsafe_allow_html=True,
    )


def render_message(msg: dict) -> None:
    role = msg["role"]
    content = msg["content"].replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="msg-row {role}">
            <div class="bubble {role}">{content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    meta_cols = st.columns([1, 1, 6])
    with meta_cols[0]:
        if msg.get("timestamp"):
            st.caption(msg["timestamp"])
    with meta_cols[1]:
        if role == "assistant":
            render_copy_button(msg["content"], msg.get("id", str(uuid.uuid4())))

    sources = msg.get("sources")
    if sources:
        with st.expander(f"📄 Sources ({len(sources)})"):
            for src in sources:
                st.markdown(f"- `{src}`")


def render_welcome() -> None:
    st.markdown(
        """
        <div class="welcome-card">
            <div style="font-size:44px;">🏦</div>
            <h3>Welcome to AION AI Factory</h3>
            <p>Ask me anything about bank policies — KYC, loans, cards, transfers, complaints, and more.<br>
            All answers are grounded in our official documents, with sources cited.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    left, spacer, right = st.columns([8, 2, 1])

    with left:
        st.markdown("""
        <h1 style="margin-bottom:0;">AION - BUSINESS BANKING</h1>
        <p style="color:#6B7280;">
        Chat with your data • customer-state briefings • outcome loop
        </p>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(
            "<div style='text-align:right;font-size:12px;color:#888;'>powered by</div>",
            unsafe_allow_html=True,
        )
        st.image(Image.open("assets/aion_logo.png"), width=90)


def start_new_chat() -> None:
    save_current_chat()
    st.session_state.chat_id = str(uuid.uuid4())
    st.session_state.messages = []


def switch_to_chat(chat_id: str) -> None:
    save_current_chat()
    loaded = load_saved_chat(chat_id)
    if loaded:
        st.session_state.chat_id = chat_id
        st.session_state.messages = loaded["messages"]


def main() -> None:
    st.set_page_config(page_title="AION AI Factory", page_icon="🏦", layout="wide")
    inject_css()

    if "chat_id" not in st.session_state:
        st.session_state.chat_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None

    with st.sidebar:
        # --- Brand row (left) + New chat icon button (right) ---
        brand_col, new_chat_col = st.columns([4, 1])
        with brand_col:
            st.markdown(
                """<div class="sidebar-brand"> AION <span class="badge">AI FACTORY</span></div>""",
                unsafe_allow_html=True,
            )
        with new_chat_col:
            st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
            if st.button("➕", key="new_chat_btn", help="New chat"):
                start_new_chat()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        st.subheader("🕓 Recent chats")
        saved_chats = list_saved_chats()
        if not saved_chats:
            st.caption("No saved chats yet")
        for chat in saved_chats:
            is_current = chat["id"] == st.session_state.chat_id
            cols = st.columns([5, 1])
            with cols[0]:
                label = ("🟢 " if is_current else "") + chat["title"]
                if st.button(label, key=f"chat_{chat['id']}", use_container_width=True):
                    switch_to_chat(chat["id"])
                    st.rerun()
            with cols[1]:
                if st.button("🗑️", key=f"del_{chat['id']}"):
                    delete_saved_chat(chat["id"])
                    if is_current:
                        start_new_chat()
                    st.rerun()

        st.divider()
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

    render_header()

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

        with st.spinner("Thinking..."):
            result = send_chat_message(prompt)

        if result:
            reply_time = datetime.now().strftime("%I:%M %p")
            msg_id = str(uuid.uuid4())
            sources = result.get("sources", [])

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": result["reply"],
                    "sources": sources,
                    "timestamp": reply_time,
                    "id": msg_id,
                }
            )
            render_message(st.session_state.messages[-1])
            save_current_chat()


if __name__ == "__main__":
    main()