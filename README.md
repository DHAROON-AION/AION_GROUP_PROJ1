# AION AI Factory

Self-hosted, open-source AI platform for banking environments.  
No cloud APIs. All components run locally via Docker.

## Quick Start

```bash
# 1. Copy environment template (first time only)
cp .env.example .env

# 2. Start the entire platform
docker compose up --build
```

### Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Streamlit UI | http://localhost:8501 | User interface |
| FastAPI Backend | http://localhost:8000 | API + agents |
| API Docs | http://localhost:8000/docs | OpenAPI documentation |
| Health Check | http://localhost:8000/health | Platform status |
| Langfuse | http://localhost:3000 | Observability & tracing |
| Ollama | http://localhost:11434 | Local LLM runtime |
| PostgreSQL | localhost:5432 | App DB + pgvector |

## Architecture

```
User
  ↓
Streamlit UI (frontend:8501)
  ↓
FastAPI (backend:8000)
  ↓
LangGraph Agent          [Phase 3 — TODO]
  ↓
Tool Calling (MCP)       [Phase 4 — TODO]
  ↓
Ollama (local LLM)
  ↓
PostgreSQL + pgvector
  ↓
Langfuse (tracing)
```

## Project Structure

```
AION_GROUP_PROJ1/
├── backend/           # FastAPI application
├── frontend/          # Streamlit UI
├── documents/         # RAG source documents
├── docker/            # Dockerfiles & init scripts
├── docker-compose.yml
├── .env
└── README.md
```

## Phase 1 — Docker Infrastructure ✅

Phase 1 delivers:

- Multi-container Docker Compose stack
- Ollama local LLM with automatic model pull
- PostgreSQL + pgvector for application data
- Langfuse v3 self-hosted observability (Postgres, ClickHouse, Redis, MinIO)
- FastAPI backend with health checks
- Streamlit frontend with system status panel
- Environment-driven configuration via `.env`

### How to Test Phase 1

```bash
# Validate compose file
docker compose config

# Start all services
docker compose up --build

# Check backend health (wait ~2 min for Langfuse to boot)
curl http://localhost:8000/health

# Expected: status "healthy" or "degraded" (degraded if Ollama model still pulling)
```

Open http://localhost:8501 — the sidebar shows live component health.

### Langfuse Setup (First Time)

1. Open http://localhost:3000
2. Create an account and project
3. Copy API keys into `.env`:
   ```
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   LANGFUSE_SECRET_KEY=sk-lf-...
   ```
4. Restart backend: `docker compose restart backend`

## Implementation Roadmap

| Phase | Module | Status |
|-------|--------|--------|
| 1 | Docker Infrastructure | ✅ Complete |
| 2 | FastAPI (routing, config, DI, logging) | 🔲 TODO |
| 3 | LangGraph + Agno agents (+ LangChain comparison) | 🔲 TODO |
| 4 | Tool Calling (calculator, transaction, sector signal, MCP) | 🔲 TODO |
| 5 | RAG (LlamaIndex, BGE, pgvector, citations) | 🔲 TODO |
| 6 | Frontend (chat, upload, history, streaming) | 🔲 TODO |
| 7 | Evaluation (Ragas, Promptfoo, benchmarks) | 🔲 TODO |
| 8 | Guardrails (Presidio PII, NeMo Guardrails) | 🔲 TODO |
| 9 | Testing (integration, Docker, performance) | 🔲 TODO |
| 10 | Documentation (architecture diagram, developer guide) | 🔲 TODO |

## Internship Framework Comparison (TODO)

Per internship requirements, the same risk-monitoring agent must be implemented in:

- **LangGraph** (primary orchestration)
- **Agno** (comparison)
- **LangChain** (optional minimal implementation)

Benchmarks will compare latency, tool-call accuracy, and developer ergonomics.

## Constraints

- No cloud AI APIs (OpenAI, Anthropic, Gemini, etc.)
- All components are open-source and self-hosted
- Synthetic/public sample data only
- Secrets in `.env` — never committed to git

See [docs/INTERNSHIP_REQUIREMENTS.md](docs/INTERNSHIP_REQUIREMENTS.md) for the full internship roadmap and acceptance criteria.

## Development

```bash
# View logs for a specific service
docker compose logs -f backend

# Rebuild after code changes
docker compose up --build backend frontend

# Stop everything
docker compose down

# Stop and remove volumes (full reset)
docker compose down -v
```

## Hardware Requirements

Minimum for local development:

- 16 GB RAM (Langfuse + Ollama + ClickHouse)
- 20 GB free disk (Ollama models)
- Docker Desktop with Compose v2

For GPU acceleration, configure Ollama with NVIDIA Container Toolkit.
