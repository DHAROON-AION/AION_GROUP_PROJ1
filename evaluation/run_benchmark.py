#!/usr/bin/env python3
"""Agent framework benchmark — compares LangGraph, Agno, and LangChain."""

import asyncio
import json
import sys
import time
from pathlib import Path

from backend.agents.router import run_agent
from backend.core.ollama import check_ollama_health

BENCHMARK_PROMPTS = [
    "What is the minimum balance for a personal savings account?",
    "Assess credit risk for customer SME-1042 in the retail sector.",
    "What documents are needed for a business current account?",
    "What are the credit card payment terms?",
]

FRAMEWORKS = ["langgraph", "agno", "langchain"]
RESULTS_PATH = Path("/app/evaluation/results/benchmark.json")


async def _wait_for_ollama(retries: int = 12, delay_s: float = 5.0) -> None:
    """Ensure Ollama is reachable before running long benchmark jobs."""
    for attempt in range(1, retries + 1):
        health = await check_ollama_health()
        if health.get("status") == "healthy":
            print(f"Ollama ready at {health.get('url')} (models: {health.get('models')})")
            return
        print(
            f"Waiting for Ollama ({attempt}/{retries}): {health.get('error', 'unavailable')}",
            file=sys.stderr,
        )
        await asyncio.sleep(delay_s)
    raise RuntimeError(
        "Ollama is not reachable. Start the stack with "
        "'docker compose up -d' and ensure the ollama container is healthy."
    )


async def run_benchmark() -> dict:
    await _wait_for_ollama()

    results = []
    total = len(FRAMEWORKS) * len(BENCHMARK_PROMPTS)
    step = 0

    for framework in FRAMEWORKS:
        for prompt in BENCHMARK_PROMPTS:
            step += 1
            print(f"[{step}/{total}] {framework}: {prompt[:50]}...", flush=True)
            start = time.perf_counter()
            try:
                output = await run_agent(prompt, session_id=None, framework=framework)
                latency = round((time.perf_counter() - start) * 1000, 1)
                results.append({
                    "framework": framework,
                    "prompt": prompt[:60],
                    "latency_ms": latency,
                    "reply_length": len(output.reply),
                    "tools_called": output.metadata.get("tools_called", 0),
                    "sources": len(output.sources),
                    "success": True,
                })
                print(f"  ok ({latency} ms)", flush=True)
            except Exception as exc:
                latency = round((time.perf_counter() - start) * 1000, 1)
                results.append({
                    "framework": framework,
                    "prompt": prompt[:60],
                    "latency_ms": latency,
                    "success": False,
                    "error": str(exc),
                })
                print(f"  failed ({latency} ms): {exc}", flush=True)

    summary = {}
    for fw in FRAMEWORKS:
        fw_all = [r for r in results if r["framework"] == fw]
        fw_results = [r for r in fw_all if r["success"]]
        if fw_results:
            latencies = [r["latency_ms"] for r in fw_results]
            summary[fw] = {
                "avg_latency_ms": round(sum(latencies) / len(latencies), 1),
                "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0,
                "success_rate": len(fw_results) / len(fw_all),
            }
        else:
            summary[fw] = {"avg_latency_ms": 0, "p95_latency_ms": 0, "success_rate": 0.0}

    report = {"results": results, "summary": summary}
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(report, indent=2))
    print("\nSummary:")
    print(json.dumps(summary, indent=2))
    print(f"\nFull report: {RESULTS_PATH}")
    return report


if __name__ == "__main__":
    asyncio.run(run_benchmark())
