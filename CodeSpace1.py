"""
TRACK C - Step 1: Plain chat with local Ollama model via LangChain.
No documents yet. Just proving LangChain and Ollama works, with basic memory so it remembers earlier turns.
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# --- 1. Connect to the local model ---
llm = ChatOllama(
    model="llama3",
    temperature=0,
)

# --- 2. System prompt: sets the bot's behavior ---
SYSTEM_PROMPT = (
    "You are a bank assistant. You have NOT been given any policy documents yet. You must NOT invent numbers, percentages, dollar amounts, or policy details under any circumstances. If asked about a specific bank policy, rate, or rule respond ONLY with: I don't have that document loaded yet, so I can't answer that accurately. Do not guess or fill in plausible-sounding details. Do not make up any details you cannot prove."
)

# --- 3. Conversation memory: a running list of messages ---
chat_history = [SystemMessage(content=SYSTEM_PROMPT)]


def ask(user_input: str) -> str:
    """Send one message, get one reply, remember both."""
    chat_history.append(HumanMessage(content=user_input))
    response = llm.invoke(chat_history)
    chat_history.append(AIMessage(content=response.content))
    return response.content


if __name__ == "__main__":
    print("Bank Assistant (plain chat, no documents yet). Type 'quit' to exit.\n")
    while True:
        user_msg = input("You: ").strip()
        if user_msg.lower() in {"quit", "exit"}:
            break
        reply = ask(user_msg)
        print(f"Bot: {reply}\n")