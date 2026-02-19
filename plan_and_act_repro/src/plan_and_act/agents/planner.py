from __future__ import annotations

from typing import Any

from plan_and_act.core.schemas import PlanStep, PlannerOutput
from plan_and_act.core.types import ModelConfig
from plan_and_act.prompts.templates import PromptTemplates
from plan_and_act.utils.llm import LLMClient


class PlannerAgent:
    def __init__(self, model_config: ModelConfig, prompts: PromptTemplates) -> None:
        self.model_config = model_config
        self.prompts = prompts
        self.llm = LLMClient()

    def plan(
        self,
        *,
        goal: str,
        observation: str,
        action_history: list[dict[str, Any]],
        use_cot: bool,
    ) -> PlannerOutput:
        if self.model_config.provider == "openai" and self.llm.enabled:
            return self._plan_with_openai(
                goal=goal,
                observation=observation,
                action_history=action_history,
                use_cot=use_cot,
            )
        return self._plan_heuristic(goal)

    def _plan_with_openai(
        self,
        *,
        goal: str,
        observation: str,
        action_history: list[dict[str, Any]],
        use_cot: bool,
    ) -> PlannerOutput:
        planner_cfg = self.prompts.planner
        cot_hint = self.prompts.cot.get("instruction", "") if use_cot else ""
        system_prompt = (
            planner_cfg["system"]
            + "\nOutput JSON schema: {\"goal\": str, \"steps\": [{\"step_id\": int, \"intent\": str, \"success_criteria\": str}]}"
            + ("\n" + cot_hint if cot_hint else "")
        )
        user_prompt = self.prompts.format_user(
            planner_cfg["user_template"],
            {
                "goal": goal,
                "observation": observation,
                "action_history": action_history,
            },
        )
        payload = self.llm.chat_json(
            model=self.model_config.model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=self.model_config.temperature,
        )
        return PlannerOutput.model_validate(payload)

    @staticmethod
    def _plan_heuristic(goal: str) -> PlannerOutput:
        steps = [
            PlanStep(
                step_id=1,
                intent=f"Inspect context and identify entities relevant to: {goal}",
                success_criteria="Relevant entities are identified",
            ),
            PlanStep(
                step_id=2,
                intent="Execute the key action to satisfy the goal and provide final answer",
                success_criteria="Task completed and final answer prepared",
            ),
        ]
        return PlannerOutput(goal=goal, steps=steps)
