# Design Decisions

Each entry: **Problem**, **Options considered**, **What we tried**, **What we measured**, **Decision**.
Newest entries at the bottom.

---

## D1. Search provider (2026-10-26)
- **Problem:** The search agent needs real Google results.
- **Options considered:** Scraping google.com HTML; Serper.dev; other search APIs.
- **What we tried:** n/a (decided up front).
- **What we measured:** n/a. Scraping violates Google's ToS and breaks easily; Serper returns Google results as JSON and has free signup credits.
- **Decision:** Serper.dev.

## D2. Agent architecture (2026-10-26)
- **Problem:** How to build and connect the agents.
- **Options considered:** Agent framework (LangChain, etc.); hand-written LLM + tool-calling loop.
- **What we tried:** n/a.
- **What we measured:** n/a.
- **Decision:** Hand-written loop, so every step is visible. A plain-Python orchestrator calls the agents in a fixed order and passes typed dataclasses between them. The fetch agent is deterministic (no LLM), which is allowed by the course and makes it cheaper and easier to measure.

## D3. LLM model (2026-10-26)
- **Problem:** Need a cheap but capable model with tool calling, within a ~$5 total budget.
- **Options considered** (USD per 1M tokens, input / output, from OpenAI's pricing page on 2026-10-26):
  - gpt-6-luna: 0.10 / 0.50, current "efficient" model, supports function calling, no retirement date.
  - gpt-5.4-mini: 0.75 / 4.50, stronger but ~8x the price.
  - gpt-5.4-nano: 0.20 / 1.25, scheduled for shutdown 2027-04-01.
  - gpt-5-mini / gpt-5-nano: cheap but shut down 2026-12-11, during the project.
  - gpt-4o-mini / gpt-4.1-mini: older, shut down 2027-01-14.
- **What we tried:** Not yet.
- **What we measured:** Estimated cost per run with gpt-6-luna is ~20k input + ~2k output tokens ≈ $0.003, so $5 covers more than 1,000 runs.
- **Decision:** gpt-6-luna with reasoning effort "low" as the default. Keep gpt-5.4-mini as a comparison model and re-check this choice once the eval set exists.

## D4. Python version (2026-10-26)
- **Problem:** Choose a Python version.
- **Options considered:** 3.14.7 (newest installed), 3.12.10.
- **What we tried:** Installed all dependencies on 3.14. Every package installed from wheels.
- **What we measured:** No install errors.
- **Decision:** Python 3.14. Fall back to 3.12 if a later dependency fails.

## D5. Initial hard limits (2026-10-26)
- **Problem:** Keep every run within budget and stop it from looping forever.
- **Options considered:** n/a (starting values).
- **What we tried:** Not yet.
- **What we measured:** Not yet.
- **Decision:** See `config.py`: 2 rounds, 3 queries per round, 8 results per query, 5 pages, 6,000 characters per page, 30k tokens per run, 6 agent steps. Revisit after the eval runs.
