from __future__ import annotations

from pathlib import Path
from typing import Any

from plan_and_act.utils.io import load_yaml


class PromptTemplates:
    def __init__(self, config_dir: str = "configs/prompts") -> None:
        base = Path(config_dir)
        self.planner = load_yaml(base / "planner.yaml")
        self.executor = load_yaml(base / "executor.yaml")
        self.replanner = load_yaml(base / "replanner.yaml")
        self.cot = load_yaml(base / "cot.yaml")

    @staticmethod
    def format_user(template: str, payload: dict[str, Any]) -> str:
        return template.format(**payload)
