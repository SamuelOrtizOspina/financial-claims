from langgraph.graph import END, START, StateGraph
from src.nodes.investigation import investigation_node
from src.state import ClaimState

builder = StateGraph(ClaimState)

builder.add_node("investigation", investigation_node)

builder.add_edge(START, "investigation")
builder.add_edge("investigation", END)

graph = builder.compile()


def route_after_completeness(state: ClaimState) -> str:
    if state.get("errors"):
        return "failed"

    if state.get("missing_evidence"):
        return "awaiting_information"

    if state.get("classification_confidence", 1.0) < 0.70:
        return "awaiting_information"

    return "investigating"


def route_after_investigation(state: ClaimState) -> str:
    if state.get("errors"):
        return "failed"

    if state.get("missing_evidence"):
        return "awaiting_information"

    risk = state.get("risk_assessment")

    if risk and risk.get("severity") in {"media", "alta"}:
        return "awaiting_human_review"

    suspicious = any(
        item.get("trust_label") == "instruccion_potencial"
        for item in state.get("evidence", [])
    )

    if suspicious:
        return "awaiting_human_review"

    return "awaiting_human_review"
