"""Wiring of the claims pipeline.

    intake -> completeness -> [investigation -> recommendation | recommendation] -> audit

A claim missing required documentation skips investigation and goes straight to
``recommendation``, which emits a ``pending_information`` decision. Every path
ends at ``audit`` so no claim ever leaves the graph without a record.

LangGraph is the intended runtime. When it is not installed the module falls
back to :func:`run_sequential`, a small runner with the same merge semantics, so
the pipeline stays demonstrable before the dependency is provisioned.
"""

from __future__ import annotations

from typing import Any, Callable

from .nodes import (
    audit,
    completeness,
    intake,
    investigation,
    recommendation,
    route_after_completeness,
)
from .state import ClaimState, new_state

try:  # pragma: no cover - exercised only by which packages are installed
    from langgraph.graph import END, StateGraph

    LANGGRAPH_AVAILABLE = True
except ImportError:  # pragma: no cover
    END = "__end__"
    StateGraph = None  # type: ignore[assignment]
    LANGGRAPH_AVAILABLE = False


NODES: dict[str, Callable[[ClaimState], dict[str, Any]]] = {
    "intake": intake,
    "completeness": completeness,
    "investigation": investigation,
    "recommendation": recommendation,
    "audit": audit,
}

# Keys accumulated across nodes rather than overwritten, matching the
# ``Annotated[..., operator.add]`` reducers declared in state.py.
_APPEND_KEYS = ("audit_trail", "errors")


def build_graph():
    """Compile the LangGraph ``StateGraph``. Requires ``langgraph`` to be installed."""
    if not LANGGRAPH_AVAILABLE:
        raise RuntimeError(
            "langgraph is not installed. Run `pip install -r requirements.txt`, "
            "or use run_sequential() for a dependency-free run."
        )

    builder = StateGraph(ClaimState)
    for name, fn in NODES.items():
        builder.add_node(name, fn)

    builder.set_entry_point("intake")
    builder.add_edge("intake", "completeness")
    builder.add_conditional_edges(
        "completeness",
        route_after_completeness,
        {"investigation": "investigation", "recommendation": "recommendation"},
    )
    builder.add_edge("investigation", "recommendation")
    builder.add_edge("recommendation", "audit")
    builder.add_edge("audit", END)

    return builder.compile()


def _merge(state: ClaimState, update: dict[str, Any]) -> ClaimState:
    """Apply one node's partial update using the state's reducer semantics."""
    for key, value in update.items():
        if key in _APPEND_KEYS:
            state[key] = list(state.get(key, [])) + list(value)  # type: ignore[literal-required]
        else:
            state[key] = value  # type: ignore[literal-required]
    return state


def run_sequential(raw_claim: dict[str, Any]) -> ClaimState:
    """Run the same pipeline without LangGraph. Used as a fallback and in tests."""
    state = new_state(raw_claim)

    state = _merge(state, intake(state))
    state = _merge(state, completeness(state))
    if route_after_completeness(state) == "investigation":
        state = _merge(state, investigation(state))
    state = _merge(state, recommendation(state))
    state = _merge(state, audit(state))

    return state


def run_claim(raw_claim: dict[str, Any]) -> ClaimState:
    """Process one claim, preferring LangGraph when it is available."""
    if LANGGRAPH_AVAILABLE:
        return build_graph().invoke(new_state(raw_claim))
    return run_sequential(raw_claim)
