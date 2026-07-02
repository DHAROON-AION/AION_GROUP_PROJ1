# AION AI Factory

Self-hosted, open-source AI platform for banking environments.  
No cloud APIs. All components run locally via Docker.

## Quick Start

**Always run commands from the project root** (`AION_GROUP_PROJ1`), not the `frontend` folder.

```powershell
cd "C:\Users\ibrah\OneDrive\Desktop\AI Factory AION\AION_GROUP_PROJ1"

# Standard start (CPU Ollama in Docker)
docker compose up -d --remove-orphans

# Fastest on Windows laptop with NVIDIA GPU — install Ollama app first, then:
.\scripts\start.ps1 -HostOllama

# Or GPU inside Docker (needs Docker Desktop GPU support):
.\scripts\start.ps1 -Gpu
```

> **Important:** `docker compose down` stops everything. Run tests only while the stack is **up**:
> ```powershell
> docker compose exec backend pytest /app/tests -v
> ```

### Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Banking Assistant | http://localhost:8501 | Enterprise chat UI |
| API Docs | http://localhost:8000/docs | OpenAPI documentation |
| Health Check | http://localhost:8000/health | Platform status |
| Langfuse | http://localhost:3000 | Observability & tracing |
| Ollama | http://localhost:11434 | Local LLM API (not a web page — shows minimal text) |

**URLs not loading?** All of these require the Docker stack to be running (`docker compose up -d`). On Windows, if you see `ERR_SOCKET_NOT_CONNECTED` or a blank page, restart the stack:

```powershell
docker compose down
docker compose up -d --remove-orphans
```

Use **Chrome or Edge** instead of the Cursor built-in browser if localhost links fail. The chat UI at **:8501** is the main app — the other URLs are for developers and demos.

## Architecture

```
User → React UI → FastAPI → LangGraph Agent → Tools/MCP → Ollama → pgvector → Langfuse
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full system diagram.

## Implementation Status

| Phase | Module | Status |
|-------|--------|--------|
| 1 | Docker Infrastructure | ✅ |
| 2 | Professional Banking Chat UI (React) | ✅ |
| 3 | LangGraph + Agno + LangChain agents | ✅ |
| 4 | Tool Calling (calculator, transaction, sector signal, MCP) | ✅ |
| 5 | RAG (BGE embeddings, pgvector, citations) | ✅ |
| 6 | Frontend ↔ Backend integration (chat, upload, streaming) | ✅ |
| 7 | Evaluation (Ragas, Promptfoo, benchmarks) | ✅ |
| 8 | Guardrails (Presidio PII, content safety) | ✅ |
| 9 | Integration tests | ✅ |
| 10 | Documentation | ✅ |

## Key Features

- **LangGraph** primary agent with human-in-the-loop risk checkpoints
- **Agno** and **LangChain** agents for framework comparison
- **3 banking tools** exposed via MCP-compatible registry
- **RAG** over 10+ synthetic bank policy documents with citations
- **Presidio PII** masking with regex fallback
- **Content safety** guardrails on input and output
- **Langfuse** tracing for every agent run
- **Benchmark harness** comparing all three frameworks

## Running Tests

```bash
docker compose exec backend pytest /app/tests -v
```

## Running Benchmarks

```bash
docker compose exec backend python /app/evaluation/run_benchmark.py
```

## Document Upload

Use the attachment button in the chat UI, or:

```bash
curl -X POST http://localhost:8000/api/documents/ingest-all
```

## Local Frontend Development

```bash
cd frontend && npm install && npm run dev
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Agent Framework Bake-Off](docs/AGENT_BAKEOFF.md)
- [Internship Requirements](docs/INTERNSHIP_REQUIREMENTS.md)

## Constraints

- No cloud AI APIs — all local Ollama
- Open-source components only
- Synthetic/public sample data only
- Secrets in `.env` — never committed
