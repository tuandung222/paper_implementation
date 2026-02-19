from __future__ import annotations

from plan_and_act.environments.base import EnvironmentAdapter
from plan_and_act.environments.simulator import GenericSimulatorEnvironment
from plan_and_act.environments.tooling import ToolCallingEnvironment
from plan_and_act.tools.base import ToolRegistry
from plan_and_act.tools.github import GitHubTopContributorTool


def build_environment(kind: str) -> EnvironmentAdapter:
    normalized = kind.strip().lower()

    if normalized == "simulator":
        return GenericSimulatorEnvironment()

    if normalized == "tool":
        registry = ToolRegistry(
            tools={
                GitHubTopContributorTool.name: GitHubTopContributorTool(),
            }
        )
        return ToolCallingEnvironment(
            registry,
            default_tool=GitHubTopContributorTool.name,
        )

    raise ValueError(f"Unsupported environment kind: '{kind}'. Expected one of: simulator, tool")
