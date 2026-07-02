"""
LangGraph Agent for Banking RAG

Flow:

START
   ↓
Retrieve & Answer
   ↓
Customer Sentiment Analysis
   ↓
END
"""

from typing import TypedDict
from langgraph.graph import END, StateGraph

from backend.rag.retrieve import ask_question


class AgentState(TypedDict):
    question: str
    answer: str
    sources: list[str]
    sentiment: str


def rag_node(state: AgentState):
    """
    Retrieve relevant banking documents and generate an answer.
    """

    answer, sources = ask_question(state["question"])

    return {
        "answer": answer,
        "sources": sources,
    }


def sentiment_node(state: AgentState):
    """
    Rule-based customer sentiment classifier.
    """

    text = state["question"].lower()

    negative_keywords = [
        "failed",
        "failure",
        "error",
        "problem",
        "issue",
        "complaint",
        "deducted",
        "not dispensed",
        "didn't",
        "blocked",
        "lost",
        "fraud",
        "unauthorized",
        "cannot",
        "can't",
        "unable",
        "delay",
        "declined",
        "crash",
    ]

    positive_keywords = [
        "thank",
        "thanks",
        "appreciate",
        "great",
        "excellent",
        "good",
        "happy",
        "awesome",
        "perfect",
    ]

    if any(word in text for word in positive_keywords):
        sentiment = "Positive"

    elif any(word in text for word in negative_keywords):
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
    }
graph = StateGraph(AgentState)

graph.add_node("rag", rag_node)
graph.add_node("sentiment", sentiment_node)

graph.set_entry_point("rag")

graph.add_edge("rag", "sentiment")
graph.add_edge("sentiment", END)

banking_agent = graph.compile()