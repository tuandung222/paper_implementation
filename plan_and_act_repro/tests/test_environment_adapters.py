from __future__ import annotations

from dataclasses import dataclass

from plan_and_act.core.schemas import ExecutorAction
from plan_and_act.environments.factory import build_environment
from plan_and_act.environments.tooling import ToolCallingEnvironment
from plan_and_act.tools.base import ToolRegistry


@dataclass
class EchoTool:
    name: str = "echo"

    def run(self, arguments: dict) -> dict:
        return {"ok": True, "echo": arguments}


def test_factory_builds_supported_environments() -> None:
    simulator = build_environment("simulator")
    tool = build_environment("tool")

    assert simulator.name == "generic_simulator"
    assert tool.name == "tool_calling"


def test_tool_environment_executes_registered_tool() -> None:
    env = ToolCallingEnvironment(
        ToolRegistry({"echo": EchoTool()}),
        default_tool="echo",
    )

    obs0 = env.reset(goal="Test generic tool domain")
    assert "Registered tools" in obs0

    result = env.step(
        action=ExecutorAction(
            action_type="search",
            target="",
            arguments={"query": "hello"},
        ),
        step_count=1,
    )

    assert "Tool[echo]" in result.observation
    assert result.done is False
    assert result.success is False


def test_tool_environment_exit_action_finishes_episode() -> None:
    env = build_environment("tool")
    result = env.step(
        action=ExecutorAction(
            action_type="exit",
            is_final=True,
            final_answer="done",
        ),
        step_count=2,
    )

    assert result.done is True
    assert result.success is True
    assert result.final_answer == "done"
