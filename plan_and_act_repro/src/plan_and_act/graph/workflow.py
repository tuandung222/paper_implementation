from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph

from plan_and_act.agents.executor import ExecutorAgent
from plan_and_act.agents.planner import PlannerAgent
from plan_and_act.agents.replanner import ReplannerAgent
from plan_and_act.core.schemas import PlanStep
from plan_and_act.core.state import PlanActState
from plan_and_act.environments.base import EnvironmentAdapter
from plan_and_act.environments.simulator import GenericSimulatorEnvironment
from plan_and_act.graph.transitions import route_after_executor


def planner_node(state: PlanActState, planner: PlannerAgent) -> dict[str, Any]:
    output = planner.plan(
        goal=state["goal"],
        observation=state["observation"],
        action_history=state["action_history"],
        use_cot=state["use_cot"],
    )
    return {
        "plan": [step.model_dump() for step in output.steps],
        "current_step_idx": 0,
        "needs_replan": False,
    }


def executor_node(
    state: PlanActState,
    executor: ExecutorAgent,
    environment: EnvironmentAdapter,
) -> dict[str, Any]:
    if state["done"]:
        return {}

    step_count = state["step_count"]
    max_steps = state["max_steps"]
    current_idx = state["current_step_idx"]
    plan = state["plan"]

    if step_count >= max_steps:
        return {
            "done": True,
            "success": False,
            "final_answer": "Stopped: max steps reached.",
            "notes": state["notes"] + ["Reached max step budget."],
        }

    if not plan or current_idx >= len(plan):
        if not state["dynamic_replanning"]:
            return {
                "done": True,
                "success": False,
                "final_answer": "Stopped: plan exhausted while dynamic replanning is disabled.",
                "notes": state["notes"] + ["Plan exhausted and replanning is disabled."],
            }
        return {
            "needs_replan": True,
            "notes": state["notes"] + ["No remaining plan steps; requesting replanning."],
        }

    current_step = PlanStep.model_validate(plan[current_idx])
    action = executor.act(
        goal=state["goal"],
        current_step=current_step,
        observation=state["observation"],
        step_index=current_idx,
        total_steps=len(plan),
        use_cot=state["use_cot"],
    )

    new_step_count = step_count + 1
    new_action_history = state["action_history"] + [action.model_dump()]
    env_result = environment.step(action=action, step_count=new_step_count)
    new_observation = env_result.observation

    done = bool(action.is_final or env_result.done)
    success = bool(action.is_final or env_result.success)
    final_answer = action.final_answer or env_result.final_answer or state["final_answer"]

    needs_replan = bool(state["dynamic_replanning"] and not done)
    notes = state["notes"] + env_result.notes

    return {
        "latest_action": action.model_dump(),
        "action_history": new_action_history,
        "observation": new_observation,
        "step_count": new_step_count,
        "current_step_idx": current_idx + 1,
        "done": done,
        "success": success,
        "final_answer": final_answer,
        "needs_replan": needs_replan,
        "notes": notes,
    }


def replanner_node(state: PlanActState, replanner: ReplannerAgent) -> dict[str, Any]:
    output = replanner.replan(
        goal=state["goal"],
        previous_plan=state["plan"],
        action_history=state["action_history"],
        observation=state["observation"],
        use_cot=state["use_cot"],
    )
    return {
        "plan": [step.model_dump() for step in output.steps],
        "current_step_idx": 0,
        "needs_replan": False,
        "notes": state["notes"] + ["Replanned based on latest observation."],
    }


def build_workflow(
    planner: PlannerAgent,
    executor: ExecutorAgent,
    replanner: ReplannerAgent,
    environment: EnvironmentAdapter | None = None,
):
    environment_adapter = environment or GenericSimulatorEnvironment()
    graph = StateGraph(PlanActState)

    graph.add_node("planner", lambda s: planner_node(s, planner))
    graph.add_node("executor", lambda s: executor_node(s, executor, environment_adapter))
    graph.add_node("replanner", lambda s: replanner_node(s, replanner))

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "executor")

    graph.add_conditional_edges(
        "executor",
        route_after_executor,
        {
            "end": END,
            "replan": "replanner",
            "continue": "executor",
        },
    )
    graph.add_edge("replanner", "executor")

    return graph.compile()
