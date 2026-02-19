# Plan-and-Act Reproduction (arXiv:2503.09572v3)

Navigation:
- Reading hub: [`READING_GUIDE.md`](READING_GUIDE.md)
- Reproduction roadmap: [`REPRODUCTION_PLAN.md`](REPRODUCTION_PLAN.md)
- Paper deep-dive review: [`PLAN_AND_ACT_review.md`](PLAN_AND_ACT_review.md)
- Notebook demo: [`notebooks/01_plan_and_act_real_tool_demo.ipynb`](notebooks/01_plan_and_act_real_tool_demo.ipynb)
- Repository root: [`../README.md`](../README.md)

Research-friendly codebase to reproduce the main ideas in **Plan-and-Act**:
- Planner-Executor modular architecture
- Synthetic planning-data pipeline
- Dynamic replanning
- CoT-enhanced planning/execution
- Domain-agnostic environment adapters (not limited to browser/web)

## Quick Start

1. Create env and install:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

2. Configure API key:
```bash
cp .env.example .env
# set OPENAI_API_KEY in .env
```

3. Run baseline episode:
```bash
plan-act-run run-episode --goal "Follow the top contributor of this GitHub project" --environment simulator --dynamic-replanning
```

4. Run tool-calling domain episode:
```bash
plan-act-run run-episode --goal "Find top contributor of openai/openai-python" --environment tool --dynamic-replanning
```

## Project Layout

- `configs/`: model/data/eval/prompt configs
- `src/plan_and_act/`: source code
- `src/plan_and_act/environments/`: domain adapters (`simulator`, `tool`)
- `src/plan_and_act/tools/`: reusable external tools (e.g., GitHub API)
- `tests/`: unit tests for schema/graph transitions
- `data/`: raw/interim/processed/synthetic datasets
- `artifacts/`: run traces and reports
- `paper_assets/`: downloaded arXiv HTML/PDF

## Notes

- This scaffold starts with a deterministic environment simulator to validate workflow wiring.
- Replace simulator adapters with WebArena harness in later phases.
