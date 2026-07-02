# Developer Guide

## Quick Start

```bash
docker compose up --build
```

| URL | Service |
|-----|---------|
| http://localhost:8501 | Banking Assistant UI |
| http://localhost:8000/docs | API Documentation |
| http://localhost:3000 | Langfuse Tracing |

## Project Structure

```
backend/
  agents/       LangGraph, Agno, LangChain agents
  api/          FastAPI routes (chat, health, documents)
  core/         Config, Ollama client, Langfuse
  database/     PostgreSQL + conversation persistence
  guardrails/   PII masking + content safety
  rag/          Embeddings, ingest, retrieval
  tools/        Banking tools + MCP registry

frontend/
  src/components/  React UI components
  src/services/    API integration layer
  src/hooks/       State management

documents/      Bank policy documents for RAG
evaluation/     Benchmark and Promptfoo configs
tests/          Integration tests
```

## Adding a New Tool

1. Create `backend/tools/my_tool.py` with a function returning `dict`
2. Register in `backend/tools/registry.py`
3. Add detection logic in `backend/agents/langgraph_agent.py` `_detect_tools()`

## Switching Agent Framework

The API accepts `agent_framework` parameter: `langgraph`, `agno`, or `langchain`.

```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the minimum savings balance?", "agent_framework": "langgraph"}'
```

## Running Tests

```bash
docker compose exec backend pytest /app/tests -v
```

## Running Benchmarks

```bash
docker compose exec backend python /app/evaluation/run_benchmark.py
```

## Document Ingestion

Place `.md` or `.txt` files in `documents/`, then:

```bash
curl -X POST http://localhost:8000/api/documents/ingest-all
```

Or upload via the UI attachment button.

## Environment Variables

See `.env.example` for all configuration options.

Key variables:
- `OLLAMA_DEFAULT_MODEL` — LLM model name
- `EMBEDDING_MODEL` — BGE embedding model
- `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` — Tracing credentials
