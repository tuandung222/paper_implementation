# Plan-and-Act Reproduction (arXiv:2503.09572v3)

Research-friendly codebase to reproduce the main ideas in **Plan-and-Act**:
- Planner-Executor modular architecture
- Synthetic planning-data pipeline
- Dynamic replanning
- CoT-enhanced planning/execution

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
plan-act-run run-episode --goal "Follow the top contributor of this GitHub project" --dynamic-replanning
```

## Project Layout

- `configs/`: model/data/eval/prompt configs
- `src/plan_and_act/`: source code
- `tests/`: unit tests for schema/graph transitions
- `data/`: raw/interim/processed/synthetic datasets
- `artifacts/`: run traces and reports
- `paper_assets/`: downloaded arXiv HTML/PDF

## Notes

- This scaffold starts with a deterministic environment simulator to validate workflow wiring.
- Replace simulator adapters with WebArena harness in later phases.
