# AION AI Factory — System Architecture

## Overview

AION is a self-hosted AI platform for banking environments. All components run locally via Docker with no cloud API dependencies.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     User (Browser)                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              React Banking Assistant (Nginx :8501)           │
└─────────────────────────┬───────────────────────────────────┘
                          │ /api/*
┌─────────────────────────▼───────────────────────────────────┐
│                    FastAPI Backend (:8000)                   │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │ Guardrails  │→ │ Agent Router │→ │ RAG Retriever      │  │
│  │ PII + Safety│  │ LG/Agno/LC   │  │ pgvector + BGE     │  │
│  └─────────────┘  └──────┬───────┘  └────────────────────┘  │
└──────────────────────────┼────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   ┌──────────┐    ┌────────────┐    ┌──────────────┐
   │  Ollama  │    │ PostgreSQL │    │   Langfuse   │
   │  (LLM)   │    │ + pgvector │    │  (Tracing)   │
   └──────────┘    └────────────┘    └──────────────┘
```

## Agent Frameworks

| Framework | Role | File |
|-----------|------|------|
| LangGraph | Primary orchestrator with human-in-the-loop | `backend/agents/langgraph_agent.py` |
| Agno | Framework comparison (identical I/O) | `backend/agents/agno_agent.py` |
| LangChain | Minimal comparison implementation | `backend/agents/langchain_agent.py` |

## Banking Tools (MCP-compatible)

| Tool | Purpose |
|------|---------|
| `calculate_ratios` | SME credit ratio analysis |
| `get_transactions` | Synthetic transaction cash-flow data |
| `get_sector_signal` | Sector economic deterioration signals |

## Data Flow

1. User sends message via React UI
2. Guardrails mask PII and block unsafe inputs
3. Agent router dispatches to selected framework
4. RAG retriever fetches relevant bank documents
5. Tools invoked based on message content
6. Ollama generates response
7. Output guardrails applied
8. Response traced in Langfuse
9. Reply returned with source citations

## Infrastructure Services

| Service | Port | Purpose |
|---------|------|---------|
| frontend | 8501 | React UI (Nginx) |
| backend | 8000 | FastAPI API |
| ollama | 11434 | Local LLM |
| postgres | 5432 | App DB + vectors |
| langfuse-web | 3000 | Observability |

## Security

- All PII masked via Presidio (with regex fallback)
- Content safety guardrails on input and output
- No cloud API keys — all processing on-premises
- Synthetic data only for demos
