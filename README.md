# Sentinel

**Automated red-teaming and trust scoring for tool-using AI agents.**

Sentinel attacks an AI agent with probes mapped to the OWASP Top 10 for Agentic Applications. It records exactly what the agent did as a standard trace, scores the agent's behaviour, and proves that its own scoring is reliable.

The targets under test are two versions of the same insurance-claims assistant for **Acme Assure**, a fictional insurer. Version A is built with the OpenAI Agents SDK and version B with Google ADK. Both run on the Gemini free tier.

See [`docs/PLAN.md`](docs/PLAN.md) for the full 8-week plan, the role-alignment research and the lesson map.

## Setup (once)

```bash
cd sentinel
python -m venv .venv
# macOS / Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
cp .env.example .env        # then paste your free Gemini key into .env
```

Python 3.10 or newer is required.

## How the lessons work

Each lesson has a **spec**: a test file in `tests/`. You type the code from the lesson, then run that lesson's tests:

```bash
pytest tests/test_lesson1a_schema.py -v
```

All tests green means the lesson is done. Then commit:

```bash
git add -A && git commit -m "Lesson 1A: trace schema"
```

A real commit history, one lesson per commit, is something recruiters actually look at, so push to GitHub from day one.

## Repo map

```
sentinel/                  # the auditor
  trace/schema.py          # L1  the trace contract (OTel GenAI-aligned)
  trace/otel.py            # L2  export to OpenTelemetry + tool manifest
  detectors/approval.py    # L1  first detectors
targets/                   # the agents under test
  claims_world/
    data/policies/*.md     # Acme Assure policy wording (RAG corpus)
    data/claims.json       # sandbox claims database
    tools.py               # L3  get_claim, search_policy, issue_payout ...
    retrieval.py           # L4  mini-RAG
  openai_agent/            # L5-6 Agent A + adapter
  adk_agent/               # L7-8 Agent B + adapter
  run.py                   # L9  run_target(name, input) -> SentinelTrace
tests/                     # one spec per lesson
docs/
  PLAN.md
  design/trace-schema.md   # your design doc (fill in after Lesson 2)
```

_All insurer names, policies and customers in this repo are fictional test data._
