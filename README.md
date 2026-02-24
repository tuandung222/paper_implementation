# paper_implementation

Monorepo for reproducing agent papers with clean, modular, research-oriented code.

## Repository Scope

Current workspaces:
1. Plan-and-Act reproduction framework: [`plan_and_act_repro/`](plan_and_act_repro/)
2. Manus-style 3-subagent scaffold: [`manus_3subagent_repro/`](manus_3subagent_repro/)
3. Orchestration DAG reproduction workspace: [`orchdag_repro/`](orchdag_repro/)

Primary active project in this repo is **Plan-and-Act**.

## Plan-and-Act Quick Navigation

Paper:
1. arXiv abstract: [2503.09572v3](https://arxiv.org/abs/2503.09572v3)
2. Downloaded PDF: [`plan_and_act_repro/paper_assets/2503.09572v3.pdf`](plan_and_act_repro/paper_assets/2503.09572v3.pdf)
3. Downloaded HTML: [`plan_and_act_repro/paper_assets/2503.09572v3.html`](plan_and_act_repro/paper_assets/2503.09572v3.html)

Start here:
1. Project README (detailed): [`plan_and_act_repro/README.md`](plan_and_act_repro/README.md)
2. Docs hub: [`plan_and_act_repro/docs/README.md`](plan_and_act_repro/docs/README.md)
3. Reading guide: [`plan_and_act_repro/docs/READING_GUIDE.md`](plan_and_act_repro/docs/READING_GUIDE.md)
4. Paper deep-dive review: [`plan_and_act_repro/docs/analysis/PLAN_AND_ACT_REVIEW.md`](plan_and_act_repro/docs/analysis/PLAN_AND_ACT_REVIEW.md)
5. Architecture visual guide: [`plan_and_act_repro/docs/architecture/AGENT_ARCHITECTURE_VISUAL_GUIDE.md`](plan_and_act_repro/docs/architecture/AGENT_ARCHITECTURE_VISUAL_GUIDE.md)
6. Reproduction plan: [`plan_and_act_repro/docs/plans/REPRODUCTION_PLAN.md`](plan_and_act_repro/docs/plans/REPRODUCTION_PLAN.md)
7. Training-data tracing plan: [`plan_and_act_repro/docs/plans/TRAINING_DATA_TRACING_PLAN.md`](plan_and_act_repro/docs/plans/TRAINING_DATA_TRACING_PLAN.md)

## Plan-and-Act Highlights in This Codebase

1. Planner-Executor-Replanner orchestration with LangGraph.
2. Structured JSON output + Pydantic validation at module boundaries.
3. Dynamic replanning flow with strict stop conditions.
4. Domain-agnostic adapters (`simulator`, `tool`) so framework is not browser-only.
5. Real no-key tools (search, URL fetch, calculator, GitHub contributor lookup).
6. Runtime tracing pipeline for trajectory collection and future training-data export.
7. Notebook demos for inspection and full LLM I/O monitoring.

## Quick Start

```bash
cd /Users/admin/TuanDung/paper_implementation/plan_and_act_repro
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
pip install nbformat nbclient jupyter ipykernel
cp .env.example .env
# set OPENAI_API_KEY in .env
```

Run no-key real tools demo:

```bash
plan-act-run demo-tools \
  --query "plan and act llm agents" \
  --url "https://arxiv.org/abs/2503.09572v3" \
  --expression "(42 * 13) / 7 + sqrt(81)"
```

Run GPT-4 integrated episode:

```bash
plan-act-run run-episode \
  --goal "Find the top contributor of openai/openai-python" \
  --environment tool \
  --dynamic-replanning \
  --use-cot \
  --trace
```

## Notes

1. Use [`plan_and_act_repro/README.md`](plan_and_act_repro/README.md) for full architecture, tracing, test, and troubleshooting details.
2. Never commit secrets (`.env`, API keys, trace files containing sensitive prompts).
