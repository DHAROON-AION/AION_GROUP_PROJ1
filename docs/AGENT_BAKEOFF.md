# Agent Framework Bake-Off

## Objective

Compare LangGraph, Agno, and LangChain for the AION SME risk-monitoring and customer support agent.

## Test Setup

- **Model:** Ollama `llama3.2:3b` (local, no cloud API)
- **Tools:** calculate_ratios, get_transactions, get_sector_signal
- **RAG:** BGE embeddings + pgvector over 10+ bank policy documents
- **Metrics:** Latency (avg, p95), tool-call accuracy, source citation rate

## How to Run

```bash
docker compose exec backend python evaluation/run_benchmark.py
```

Results saved to `evaluation/results/benchmark.json`.

## Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Latency | 30% | Average and p95 response time |
| Tool accuracy | 25% | Correct tool selection and invocation |
| Answer quality | 25% | Grounded, professional banking responses |
| Developer ergonomics | 20% | Code clarity, debugging, extensibility |

## Framework Verdict Template

| Framework | Avg Latency | Tool Calls | Verdict |
|-----------|-------------|------------|---------|
| LangGraph | Run benchmark | Primary orchestrator | Adopt |
| Agno | Run benchmark | Comparison | Trial |
| LangChain | Run benchmark | Minimal impl | Hold |

> Run `evaluation/run_benchmark.py` after `docker compose up` to populate measured values.

## Recommendation

**LangGraph** is the primary orchestration framework due to:
- Explicit multi-step graph with human-in-the-loop checkpoints
- Native support for conditional routing (risk escalation)
- Production-grade state management

**Agno** provides a simpler agent abstraction suitable for rapid prototyping.

**LangChain** serves as a baseline comparison with minimal implementation overhead.
