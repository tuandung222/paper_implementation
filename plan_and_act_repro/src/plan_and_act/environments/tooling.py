from __future__ import annotations

import json

from plan_and_act.core.schemas import ExecutorAction
from plan_and_act.environments.base import EnvironmentAdapter, EnvironmentStepResult
from plan_and_act.tools.base import ToolRegistry


class ToolCallingEnvironment(EnvironmentAdapter):
    """Generic tool-calling environment for non-browser agent domains."""

    name = "tool_calling"

    def __init__(self, registry: ToolRegistry, *, default_tool: str | None = None) -> None:
        self.registry = registry
        self.default_tool = default_tool

    def reset(self, *, goal: str) -> str:
        registered = sorted(self.registry.tools.keys())
        return f"Tool environment initialized for goal: {goal}. Registered tools={registered}"

    def _resolve_tool_name(self, action: ExecutorAction) -> str | None:
        if action.target.startswith("tool:"):
            return action.target.split(":", 1)[1].strip() or None
        return self.default_tool

    def step(self, *, action: ExecutorAction, step_count: int) -> EnvironmentStepResult:
        if action.action_type == "exit":
            return EnvironmentStepResult(
                observation=f"Step {step_count}: Exit action requested.",
                done=True,
                success=True,
                final_answer=action.final_answer,
            )

        tool_name = self._resolve_tool_name(action)
        if not tool_name:
            return EnvironmentStepResult(
                observation=(
                    f"Step {step_count}: No tool selected for action_type='{action.action_type}'. "
                    f"Set target='tool:<name>' or configure a default tool."
                ),
            )

        result = self.registry.call(tool_name, action.arguments)
        observation = (
            f"Step {step_count}: Tool[{tool_name}] returned: {json.dumps(result, ensure_ascii=True)}"
        )
        notes: list[str] = [] if result.get("ok", False) else [f"Tool call failed: {result.get('error', 'unknown')}."]
        return EnvironmentStepResult(observation=observation, notes=notes)
