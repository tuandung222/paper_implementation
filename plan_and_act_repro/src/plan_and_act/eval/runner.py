from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any

import typer
from dotenv import load_dotenv
from rich import print

from plan_and_act.agents.executor import ExecutorAgent
from plan_and_act.agents.planner import PlannerAgent
from plan_and_act.agents.replanner import ReplannerAgent
from plan_and_act.core.schemas import EpisodeArtifact
from plan_and_act.core.state import build_initial_state
from plan_and_act.core.types import ModelConfig, RuntimeConfig
from plan_and_act.eval.metrics import compute_episode_metrics
from plan_and_act.graph.workflow import build_workflow
from plan_and_act.prompts.templates import PromptTemplates
from plan_and_act.utils.io import load_yaml, write_json
from plan_and_act.utils.seeding import set_seed

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """Run Plan-and-Act experiments and evaluations."""


def _load_runtime_config(path: str) -> RuntimeConfig:
    return RuntimeConfig.model_validate(load_yaml(path))


def _load_model_configs(path: str) -> dict[str, ModelConfig]:
    data = load_yaml(path)
    return {
        "planner": ModelConfig.model_validate(data.get("planner", {})),
        "executor": ModelConfig.model_validate(data.get("executor", {})),
        "replanner": ModelConfig.model_validate(data.get("replanner", {})),
    }


@app.command("run-episode")
def run_episode(
    goal: str = typer.Option(..., help="User goal/instruction."),
    base_config: str = typer.Option("configs/base.yaml", help="Path to base runtime config."),
    model_config: str = typer.Option("configs/models.yaml", help="Path to model config."),
    dynamic_replanning: bool = typer.Option(True, help="Enable replanning after each action."),
    use_cot: bool = typer.Option(False, help="Enable CoT hints in prompts."),
) -> None:
    load_dotenv()
    runtime_cfg = _load_runtime_config(base_config)
    model_cfgs = _load_model_configs(model_config)

    runtime_cfg = runtime_cfg.model_copy(
        update={
            "dynamic_replanning": dynamic_replanning,
            "use_cot": use_cot,
        }
    )

    set_seed(runtime_cfg.seed)

    prompts = PromptTemplates(config_dir="configs/prompts")
    planner = PlannerAgent(model_cfgs["planner"], prompts)
    executor = ExecutorAgent(model_cfgs["executor"], prompts)
    replanner = ReplannerAgent(model_cfgs["replanner"], prompts)

    workflow = build_workflow(planner, executor, replanner)

    initial_state = build_initial_state(
        goal=goal,
        max_steps=runtime_cfg.max_steps,
        dynamic_replanning=runtime_cfg.dynamic_replanning,
        use_cot=runtime_cfg.use_cot,
    )

    final_state: dict[str, Any] = workflow.invoke(initial_state)
    metrics = compute_episode_metrics(final_state)

    run_id = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    artifact = EpisodeArtifact(
        run_id=run_id,
        goal=goal,
        success=bool(final_state.get("success", False)),
        step_count=int(final_state.get("step_count", 0)),
        final_answer=str(final_state.get("final_answer", "")),
        action_history=list(final_state.get("action_history", [])),
        notes=list(final_state.get("notes", [])),
    )

    if runtime_cfg.save_artifacts:
        out_dir = Path(runtime_cfg.artifact_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        write_json(out_dir / f"episode_{run_id}.json", {
            "config": runtime_cfg.model_dump(),
            "model": {
                "planner": model_cfgs["planner"].model_dump(),
                "executor": model_cfgs["executor"].model_dump(),
                "replanner": model_cfgs["replanner"].model_dump(),
            },
            "metrics": metrics,
            "final_state": final_state,
            "artifact": artifact.model_dump(),
        })

    print("[bold green]Episode finished[/bold green]")
    print({
        "success": artifact.success,
        "step_count": artifact.step_count,
        "final_answer": artifact.final_answer,
        "metrics": metrics,
        "used_openai_key": bool(os.getenv("OPENAI_API_KEY", "").strip()),
    })


def run_cli() -> None:
    app()


if __name__ == "__main__":
    run_cli()
