# AION · AI FACTORY
## Summer Intern Sprint 2026
### Project Requirements, Use Cases & Roadmap
#### Open-Source, On-Premise AI Stack for Banking

**Document Version:** 1.0

---

## Project at a Glance
A six-week internship sprint (Jun 23 – Aug 04, 2026) in which five interns build, evaluate, and document an open-source, fully self-hosted AI stack for a GCC bank — covering local LLM serving, agents, retrieval-augmented generation, document intelligence, observability, and guardrails.

Nothing in the stack depends on a cloud API; every component is chosen so that customer data never leaves the bank's own infrastructure.

---

## Table of Contents
1. [Introduction](#introduction)
   - [Background](#background)
   - [Purpose of this Document](#purpose of this document)
   - [Project Objectives](#project objectives)
   - [Scope](#scope)
2. [Stakeholders](#stakeholders)
3. [System Overview](#system overview)
   - [Architecture Layers](#architecture layers)
   - [Shared Foundation](#shared-foundation)
   - [Team Structure](#team-structure)
4. [Functional Requirements](#functional-requirements)
5. [Non-Functional Requirements](#non-functional-requirements)
6. [Use Cases](#use-cases)
7. [Constraints & Assumptions](#constraints--assumptions)
8. [Roadmap](#roadmap)
   - [Week-by-Week Plan](#week-by-week-plan)
   - [First-Monday Checklist](#first-monday-checklist)
   - [How Interns Should Approach the Work](#how-interns-should-approach-the-work)
9. [Definition of Done](#definition-of-done)
10. [Success Criteria](#success-criteria)
11. [The Banker's Read on the Toolchain](#the-bankers-read-on-the-toolchain)
12. [Closing Note](#closing-note)

---

## Introduction

### Background
Cloud-based AI tools such as ChatGPT cannot be used on real customer data inside a GCC bank, because regulations such as SAMA's framework and the PDPL (Personal Data Protection Law) prohibit sending customer records to third-party services outside the bank's control.

This project, AION – AI Factory, is a structured six-week internship sprint in which five interns learn to design, build, and evaluate an AI stack made entirely of open-source components that can be self-hosted on the bank's own infrastructure — with no cloud API key required at any point.

The project is deliberately structured as a shared foundation (Week 1) followed by five parallel, specialised tracks, so that the pieces each intern builds can ultimately be combined into a single working system.

### Purpose of this Document
This document defines the functional and non-functional requirements, the core use cases, and a starting roadmap for the AION AI Factory internship project. It is intended to give the interns and their supervisor a single shared reference for what the system must do, what quality bars it must meet, and how the work should be sequenced over six weeks.

### Project Objectives
* Stand up a fully self-hosted, open-source AI stack that never sends data outside the bank's infrastructure.
* Give five interns hands-on, end-to-end experience across the major layers of a modern AI system: model serving, agents, retrieval, document intelligence, observability, and guardrails.
* Produce a portfolio of four working demos (not notebooks) that map directly to real banking problems.
* Build a shared evaluation harness so every demo is judged on measured evidence, not claims.
* Reach a documented Build / Buy / Partner / Park verdict for each demo, and an Adopt / Trial / Hold verdict for each tool evaluated.

### Scope

#### In Scope:
* Five workstreams: model serving, agents & tool access, retrieval/RAG & chat, document intelligence & evaluation, and observability & guardrails.
* A shared base platform (repo, container runtime, local LLM, vector store, tracing) that all five tracks build on.
* Four demo applications: a risk-monitoring agent, a corporate customer assistant, an invoice auto-coding pipeline, and the cross-cutting control tower (tracing + guardrails).
* Synthetic or public sample data only.

#### Out of Scope:
* Any use of real customer data or production banking systems.
* Any cloud-hosted model or API-metered service.
* Production deployment / go-live; the sprint produces evaluated prototypes and a recommendation, not a shipped product.

---

## Stakeholders

| Field | Description |
| :--- | :--- |
| **Interns A–E** | Five summer interns, each owning one layer of the stack end-to-end. |
| **Project Supervisor / Sponsor** | Sets direction, runs Friday teach-backs, makes the final Build/Buy/Partner/Park call on Demo Day. |
| **Risk & Compliance** | Reviews observability, guardrail, and PII-redaction evidence before anything could be considered for production. |
| **IT / Infrastructure** | Provides the on-prem hardware (laptops and/or data-centre capacity) the stack runs on. |
| **End users (illustrative)** | Branch staff, relationship managers, and finance/ops staff who would use the resulting assistants and automations if adopted. |

---

## System Overview

The system is organised in layers, from what the user touches at the top to the infrastructure that runs on bare metal at the bottom. Every layer in every tier is open source and self-hostable.

### Architecture Layers

| Layer | Representative tools |
| :--- | :--- |
| **Interface** | Streamlit, Gradio, Chainlit, Open WebUI |
| **Guardrails & PII** | Microsoft Presidio, NeMo Guardrails, Llama Guard |
| **Agents & orchestration** | Agno, LangChain, LangGraph, CrewAI |
| **Tool access** | MCP (Model Context Protocol), native function calling |
| **Retrieval / RAG** | LlamaIndex, Qdrant, pgvector, BGE embeddings |
| **Models & serving** | Ollama, vLLM, Llama 3 / Qwen / Mistral |
| **Observability & evaluation** | Langfuse, Arize Phoenix, Ragas, promptfoo |
| **Infrastructure** | Docker, FastAPI, PostgreSQL |

### Shared Foundation (built once, used by all tracks)
Before any intern branches into their specialised track, the whole team stands up an identical Week 1 base so that every later piece can interoperate:
* Python, Git, and Docker in one repository with a single `docker-compose` file that runs identically on every laptop and in the bank's data centre.
* A local LLM served via Ollama (Llama 3 or Qwen) — no cloud key needed to start building.
* A shared “hello agent” starter template that everyone forks, so nobody begins from a blank file.
* PostgreSQL plus a vector store (pgvector or Qdrant) as the shared memory layer for all retrieval work.
* Langfuse running locally, tracing every run from day one.
* One make/run command: if the project does not start with a single command from the README, it is not considered finished.

### Team Structure

| Owner | Track | Primary demo |
| :--- | :--- | :--- |
| **Intern A** | Models & serving | Local-model gateway and on-prem model recommendation |
| **Intern B** | Agents & tool access | SME early-warning risk agent (framework bake-off: Agno vs LangChain vs LangGraph) |
| **Intern C** | Retrieval, RAG & chat | Corporate customer assistant grounded in bank documents |
| **Intern D** | Documents & evaluation | Spend invoice auto-coding, plus the shared evaluation harness used by every track |
| **Intern E** | Observability & guardrails | The control tower: tracing, PII redaction, and guardrails across all four demos |

---

## Functional Requirements

### Shared Platform (FR-0.x)

| ID | Requirement | Acceptance criteria |
| :--- | :--- | :--- |
| **FR-0.1** | The system shall provide one shared Git repository and a single docker-compose configuration that starts the entire base stack. | Running one command from the README brings up the model runtime, database, vector store, and tracing UI. |
| **FR-0.2** | The system shall serve at least one local LLM with no external API dependency. | Ollama (or vLLM) serves Llama 3 or Qwen locally; no cloud key is configured anywhere. |
| **FR-0.3** | The system shall persist application and vector data in a self-hosted database. | PostgreSQL with pgvector, or Qdrant, runs as a container in the stack. |
| **FR-0.4** | The system shall trace every model and agent run automatically. | Langfuse runs locally and captures input/output/tool-calls for every request without extra code per call site. |

### Track A — Models & Serving (FR-A.x)

| ID | Requirement | Acceptance criteria |
| :--- | :--- | :--- |
| **FR-A.1** | The system shall expose one local-model endpoint that the whole team can call. | Ollama or vLLM sits behind a FastAPI endpoint; at least two models are swappable; the service starts from the README. |
| **FR-A.2** | The system shall support benchmarking of multiple open models on the same task. | At least 3 open models are compared on identical prompts for latency, answer quality, and RAM/GPU use, with a written recommendation. |
| **FR-A.3** | The system shall support running a quantized model on modest hardware. | A GGUF/quantized model runs successfully, with a short note on the quality lost versus the hardware saved. |

### Track B — Agents & Tool Access (FR-B.x)

| ID | Requirement | Acceptance criteria |
| :--- | :--- | :--- |
| **FR-B.1** | The system shall implement the same risk-monitoring agent in two different agent frameworks. | An agent built in Agno and the same agent built in LangChain both run, with an identical input/output contract and documented side-by-side notes. |
| **FR-B.2** | The agent shall be able to call external tools through a standard protocol. | At least 3 tools (transaction stub, ratio calculator, sector signal) are callable via MCP, with tool calls visible in Langfuse traces. |
| **FR-B.3** | The system shall support a multi-step agent flow with a human checkpoint. | A LangGraph graph implements interrupt/resume around a human decision point, and a verdict is reached on which framework to standardise on. |

### Track C — Retrieval, RAG & Chat (FR-C.x)

| ID | Requirement | Acceptance criteria |
| :--- | :--- | :--- |
| **FR-C.1** | The system shall answer questions grounded in the bank's own documents, with citations. | LlamaIndex + pgvector + BGE embeddings answer from at least 20 bank documents; answers are cited; the system says “I don't know” when it does not have grounds to answer. |
| **FR-C.2** | The system shall support comparison of vector stores and reranking. | A documented pgvector-vs-Qdrant comparison exists, and a reranker measurably improves the right-answer rate. |
| **FR-C.3** | The system shall expose retrieval through a conversational chat interface with memory. | A Streamlit or Chainlit app supports multi-turn conversation and is demoable end-to-end. |

### Track D — Documents & Evaluation (FR-D.x)

| ID | Requirement | Acceptance criteria |
| :--- | :--- | :--- |
| **FR-D.1** | The system shall extract structured fields from invoices and receipts. | Vendor, amount, VAT, and date are extracted from at least 15 documents; accuracy is reported; output is clean JSON. |
| **FR-D.2** | The system shall provide one evaluation harness usable by every track. | Ragas + promptfoo report accuracy, groundedness, latency, and cost per track, runnable with one command. |
| **FR-D.3** | The system shall support adversarial (“red-team”) testing of prompts and produce a scorecard per demo. | A scorecard exists for each of the four demos, plus a consolidated build-vs-buy verdict. |

### Track E — Observability & Guardrails (FR-E.x)

| ID | Requirement | Acceptance criteria |
| :--- | :--- | :--- |
| **FR-E.1** | The system shall trace every run across all demos in a self-hosted observability tool. | Langfuse runs in Docker; traces exist for all 4 demos; one shared cost/latency dashboard is available. |
| **FR-E.2** | The system shall detect and mask personally identifiable information, and block unsafe inputs/outputs. | Presidio masks PII; NeMo Guardrails or Llama Guard is active; a red-team set of at least 20 cases (via Garak) has a reported block rate. |
| **FR-E.3** | The system shall produce a written run-and-safety report suitable for a risk/compliance review. | The report includes cost per 1,000 runs, p95 latency, a PDPL compliance note, and a production-readiness checklist. |

---

## Non-Functional Requirements

| Category | Requirement |
| :--- | :--- |
| **Data residency & privacy** | All models, vector stores, and databases must run on self-hosted infrastructure. No customer-like data may leave the local environment; only synthetic or public sample data is used, in line with SAMA expectations and the PDPL. |
| **No vendor lock-in** | Every component must be open source and self-hostable, with no per-token cloud billing and no proprietary API dependency, so the bank fully owns the stack. |
| **Auditability** | Open weights, open code, and full execution traces (via Langfuse) must make it possible for risk and compliance teams to see exactly what a model or agent did on any given run. |
| **Security** | Inputs and outputs must pass through guardrails (NeMo Guardrails / Llama Guard) and PII redaction (Presidio) by default; secrets must never be committed to the repository. |
| **Reliability / portability** | The entire stack must be packaged so the same Docker container runs unchanged on a laptop or in the bank's data centre; if it only works on one machine, it is not considered done. |
| **Performance** | Each track must report concrete latency and cost figures (e.g., p95 latency, cost per 1,000 runs) rather than qualitative impressions, so performance can be compared across model and framework choices. |
| **Evaluatability** | Every demo must pass through a shared evaluation harness (Ragas, promptfoo) producing accuracy, groundedness, latency, and cost metrics — claims must be backed by numbers. |
| **Usability** | Each demo intended for end users must be wrapped in a simple chat-style interface (Streamlit/Chainlit/Gradio) that a non-technical colleague could operate without training. |
| **Maintainability / onboarding** | The project must be runnable end-to-end via a single command from the README, with a shared starter template, so a new contributor can get productive within hours, not days. |
| **Collaboration & traceability** | All work lives in one shared repository; every run is traced; every demo and tool is given an explicit, recorded verdict so decisions are not lost after the sprint ends. |

---

## Use Cases

### UC-1: Local-Model Gateway & Benchmark (Track A)
* **Actor:** Intern A (acting as platform engineer)
* **Goal:** Provide one reliable local LLM endpoint that every other track can call, and recommend which open model the bank should standardise on.
* **Preconditions:** The shared base stack (Docker, repo, Postgres/vector store) is already running.
* **Main flow:** 1. Stand up Ollama or vLLM behind a FastAPI endpoint.
  2. Load at least two swappable models (e.g., Llama 3, Qwen).
  3. Run identical prompts representing a real bank task against 3 candidate models.
  4. Record latency, answer quality, and RAM/GPU usage for each.
  5. Produce a written recommendation.
* **Exception / alternate flow:** If a model fails to run on available hardware, quantize it (GGUF) and re-test, noting the quality/hardware trade-off.
* **Postcondition:** The team has one working local-model endpoint and a documented model recommendation with a Build/Buy/Partner/Park and Adopt/Trial/Hold verdict.
* **Related requirements:** FR-A.1, FR-A.2, FR-A.3

### UC-2: SME Early-Warning Risk Agent (Track B)
* **Actor:** Relationship manager / credit risk analyst (illustrative end user); Intern B (builder)
* **Goal:** Catch deterioration in an SME borrower's credit profile earlier, so provisions can be reduced and the bank's agent framework choice is settled with evidence.
* **Preconditions:** A local LLM endpoint (UC-1) is available; tool stubs for transaction data, ratio calculation, and sector signals exist.
* **Main flow:**
  1. Build the same risk-monitoring agent in Agno and in LangChain with an identical input/output contract.
  2. Equip the agent with at least 3 tools via MCP (transaction stub, ratio calculator, sector signal).
  3. Add a multi-step flow in LangGraph with a human-in-the-loop checkpoint before any flagged action is finalised.
  4. Compare the two framework implementations side by side.
* **Exception / alternate flow:** If the agent's tool call produces an ambiguous or low-confidence signal, the flow pauses at the human checkpoint rather than auto-escalating.
* **Postcondition:** A working risk-flagging agent exists in two frameworks with full tool-call traces, plus a documented framework recommendation.
* **Related requirements:** FR-B.1, FR-B.2, FR-B.3

### UC-3: Corporate Customer Assistant (Track C)
* **Actor:** Branch staff / relationship manager (illustrative end user); Intern C (builder)
* **Goal:** Deflect routine customer and staff questions about bank products/policies away from branch and RM staff, lowering cost-to-serve without adding headcount.
* **Preconditions:** At least 20 representative bank documents (synthetic/public) are available; the shared vector store is running.
* **Main flow:**
  1. Ingest ≥20 documents via LlamaIndex into pgvector using BGE embeddings.
  2. A user asks a question in a chat UI (Streamlit/Chainlit).
  3. The system retrieves relevant passages, optionally reranks them, and generates a cited answer.
  4. The conversation supports multi-turn follow-up with memory.
* **Exception / alternate flow:** If no document supports an answer, the assistant explicitly responds that it does not know, rather than inventing a policy.
* **Postcondition:** The user receives a cited, grounded answer or an honest “I don't know”, and the interaction is fully traced.
* **Related requirements:** FR-C.1, FR-C.2, FR-C.3

### UC-4: Spend Invoice Auto-Coding (Track D)
* **Actor:** Finance/operations staff (illustrative end user); Intern D (builder)
* **Goal:** Eliminate manual data entry for incoming invoices and receipts by automatically extracting and coding the key fields.
* **Preconditions:** A batch of at least 15 sample invoices/receipts (synthetic or public) is available.
* **Main flow:**
  1. Parse each document with Docling/PyMuPDF (or Unstructured).
  2. Extract vendor, amount, VAT, and date into clean JSON.
  3. Report extraction accuracy across the batch.
  4. Feed the results into the shared evaluation harness (Ragas/promptfoo) alongside the other three demos.
* **Exception / alternate flow:** If a document is malformed, scanned at low quality, or missing a required field, the pipeline flags it for manual review instead of guessing a value.
* **Postcondition:** Structured, accuracy-scored invoice data is produced automatically, and the evaluation harness can score this track alongside the others.
* **Related requirements:** FR-D.1, FR-D.2, FR-D.3

### UC-5: Control Tower — Tracing, PII & Guardrails (Track E)
* **Actor:** Risk & compliance reviewer (illustrative end user); Intern E (builder)
* **Goal:** Answer the question “can we run this safely under SAMA / PDPL?” for every other demo, since this decides whether anything can ever ship.
* **Preconditions:** Demos from Tracks A–D are producing traceable runs.
* **Main flow:**
  1. Self-host Langfuse and connect it to all four demos.
  2. Build one shared cost/latency dashboard.
  3. Add Presidio for PII masking and NeMo Guardrails / Llama Guard for input/output filtering.
  4. Run a red-team set of ≥20 adversarial prompts (via Garak) and report the block rate.
  5. Write the on-prem run-and-safety report (cost per 1,000 runs, p95 latency, PDPL note, production-readiness checklist).
* **Exception / alternate flow:** If a guardrail blocks a legitimate request (a false positive), the case is logged and reviewed in the Friday teach-back rather than silently dropped.
* **Postcondition:** Every other demo has full tracing, active guardrails, and a documented safety report ready for a risk/compliance conversation.
* **Related requirements:** FR-E.1, FR-E.2, FR-E.3

---

## Constraints & Assumptions

### Constraints
* No cloud API keys may be used anywhere in the project; every model and service must be self-hosted.
* Only synthetic or public sample data may be used — nothing real, nothing personal.
* The project duration is fixed at six weeks (Jun 23 – Aug 04, 2026), ending on a fixed Demo Day.
* Every demo must run from a single shared repository and a single docker-compose command.

### Assumptions
* Each intern has access to a laptop capable of running a quantized local LLM (or equivalent shared GPU capacity is provided).
* Interns have basic familiarity with Python and Git; deep AI/ML experience is not assumed (the roadmap is written for first-time builders).
* The bank can provide, or the team can construct, a small set of representative synthetic documents, invoices, and transaction stubs before Week 1 ends.
* A supervisor or sponsor is available for weekly Friday teach-backs and the final Demo Day review.

---

## Roadmap

The roadmap sequences the six weeks so all five interns share an identical foundation before splitting into their own tracks, and converges back to shared deliverables (evaluation harness, safety report, verdicts) before Demo Day.

### Week-by-Week Plan

| When | What happens |
| :--- | :--- |
| **Week 1** | **Whole team:** stand up the shared repo, Docker/docker-compose, a local LLM via Ollama, Postgres + pgvector/Qdrant, and Langfuse tracing. Fork the shared “hello agent” template. Confirm everything starts with one command. Tracks A, B, and C begin their first tasks (A1, B1, C1). |
| **Week 2** | **A:** benchmarking setup begins. **B:** continue framework bake-off (Agno vs LangChain). **C:** continue RAG ingestion and citation. **D:** begin invoice extraction (D1). **E:** self-host Langfuse fully and trace all in-progress demos (E1). |
| **Week 3** | **A:** benchmark 3 models on a real bank task (A2). **B:** add MCP tool access (B2). **C:** compare vector stores and add a reranker (C2). **D/E:** continue document extraction and begin guardrails/PII work (E2). |
| **Week 4** | **A:** quantize a model for modest hardware (A3). **B:** add the LangGraph human-checkpoint flow (B3, into Week 5). **C:** wrap retrieval in a chat UI with memory (C3, into Week 5). **D:** build the shared evaluation harness (D2, into Week 4–5). **E:** finish PII/guardrails (E2). |
| **Week 5** | **B and C** finish their demos. **D** continues the evaluation harness and begins red-teaming prompts (D3). **E** writes the on-prem run-and-safety report (E3). |
| **Week 6** | **D** finalises scorecards and the build-vs-buy verdict slides (D3). **All tracks:** final polish, rehearse demos, confirm every claim has a number behind it. **Demo Day (Aug 4):** each demo presents a Build/Buy/Partner/Park verdict and each tool an Adopt/Trial/Hold verdict. |

### First-Monday Checklist
Before Week 1 work begins, the following must be settled:
* Assign Interns A–E to their tracks.
* Stand up the shared repository, Ollama, and Langfuse together as one team activity.
* Choose which local models to test first (Llama 3 / Qwen / Mistral).
* Choose the vector store to start with (pgvector or Qdrant).
* Book the recurring Friday teach-backs and lock in Demo Day (Aug 4).

### How Interns Should Approach the Work
Since the team is not expected to know this stack on day one, the following working habits are recommended throughout the six weeks:
* **Run before you build** — get the shared template working end-to-end before changing anything; confidence comes from seeing it work first.
* **Copy, then change one thing** — fork the template, swap one piece, and observe what breaks; this teaches more than reading documentation alone.
* **Read the traces first** — when stuck, check Langfuse to see exactly what the model received and did before searching elsewhere.
* **Pair up, especially in Week 1** — nobody should fight Docker alone; setting up the base together builds a shared mental model.
* **Teach it back on Fridays** — explaining your layer to the other four interns is both a comprehension check and how the team stays aligned.
* **Always ask the banker question** — for everything built, ask “would a bank let this near a customer?”; if the answer is no, that becomes the next task.

---

## Definition of Done
A piece of work on this project is only considered complete when all of the following hold:
* It lives in the shared repository and starts via the single shared `docker-compose` command — if it only runs on one laptop, it is not done.
* It uses local models only, with no cloud API keys, and only synthetic or public sample data.
* Every run shows up in Langfuse, and every demo has passed through the shared evaluation harness with numbers behind any claim.
* It has been shown in a Friday teach-back as working software, not slides.
* PII is redacted, guardrails are active, and no secrets exist in the code.
* It ends with a stated verdict — Build / Buy / Partner / Park for the demo, and Adopt / Trial / Hold for each tool used.

---

## Success Criteria
By Demo Day (August 4, 2026), the project is considered successful if:
* All five interns have a working, demoable system in their track — not a notebook or slide mock-up.
* Every demo has been traced (Langfuse) and scored (Ragas/promptfoo) with concrete accuracy, groundedness, latency, and cost figures.
* PII redaction and guardrails are active and measured (a red-team block rate has been reported) across all demos.
* Each of the six banker questions in Section 9 below can be answered with evidence the interns actually built, not a promise.
* Every demo carries an explicit Build/Buy/Partner/Park verdict, and every tool an Adopt/Trial/Hold verdict.

---

## The Banker's Read on the Toolchain
This table is the project's real deliverable: by Demo Day, every row should be backed by something the interns actually built and measured, not just a design intention.

| Tool choice | The bank's question | The open-source answer |
| :--- | :--- | :--- |
| **Local, self-hosted models** | Where does our customer data go? | Nowhere — it stays on our own hardware. |
| **Open source, no vendor** | Are we locked in to someone? | No — we own the code and can audit it. |
| **Observability (Langfuse)** | Can we prove what the AI did? | Yes — every run is traced and reviewable. |
| **Guardrails + PII redaction** | Will this leak or misbehave? | Inputs are filtered and personal data is masked. |
| **Evaluation harness** | Does it actually work? | Measured on real cases before it ships. |
| **Docker / on-prem packaging** | Can it run in our data centre? | Yes — the same container, on our own metal. |

---

## Closing Note
The intended payoff of this sprint is not just five working demos: it is a team that has hands-on comfort with the entire open-source, on-prem AI stack — models, agents, retrieval, evaluation, and guardrails — and the habit of asking, for everything they build, whether a bank would actually let it near a customer.
