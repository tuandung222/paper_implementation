# Plan-and-Act Reading Guide

Use this page as the navigation hub when browsing on GitHub.

## Recommended Order

1. Project overview and quick start:
[`README.md`](README.md)
2. Reproduction roadmap and implementation phases:
[`REPRODUCTION_PLAN.md`](REPRODUCTION_PLAN.md)
3. Technical deep-dive review of the paper:
[`PLAN_AND_ACT_review.md`](PLAN_AND_ACT_review.md)
4. Interactive module inspection + real tool demo:
[`notebooks/01_plan_and_act_real_tool_demo.ipynb`](notebooks/01_plan_and_act_real_tool_demo.ipynb)

## Source Materials

- Paper PDF:
[`paper_assets/2503.09572v3.pdf`](paper_assets/2503.09572v3.pdf)
- Paper HTML:
[`paper_assets/2503.09572v3.html`](paper_assets/2503.09572v3.html)
- arXiv abstract page:
[https://arxiv.org/abs/2503.09572v3](https://arxiv.org/abs/2503.09572v3)

## Implementation Entry Points

- Main package:
[`src/plan_and_act/`](src/plan_and_act/)
- Workflow graph:
[`src/plan_and_act/graph/workflow.py`](src/plan_and_act/graph/workflow.py)
- Environment adapters:
[`src/plan_and_act/environments/`](src/plan_and_act/environments/)
- Tool implementations:
[`src/plan_and_act/tools/`](src/plan_and_act/tools/)
- CLI runner:
[`src/plan_and_act/eval/runner.py`](src/plan_and_act/eval/runner.py)
- Scripts:
[`scripts/`](scripts/)
- Tests:
[`tests/`](tests/)
