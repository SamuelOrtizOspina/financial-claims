from .state import ClaimState

ALLOWED_TRANSITIONS = {
    "received": {"classifying", "failed"},
    "classifying": {
        "awaiting_information",
        "investigating",
        "failed",
    },
    "awaiting_information": {
        "classifying",
        "failed",
    },
    "investigating": {
        "awaiting_human_review",
        "escalated",
        "failed",
    },
    "awaiting_human_review": {
        "approved",
        "rejected",
        "awaiting_information",
        "escalated",
        "failed",
    },
}


def validate_transition(
    current_status: str,
    next_status: str,
) -> None:
    allowed = ALLOWED_TRANSITIONS.get(current_status, set())

    if next_status not in allowed:
        raise ValueError(f"Invalid transition: {current_status} -> {next_status}")


def transition(state: ClaimState, next_status: str) -> dict:
    current_status = state["status"]

    validate_transition(current_status, next_status)

    audit_event = {
        "event_type": "status.changed",
        "from_status": current_status,
        "to_status": next_status,
        "actor": "graph",
    }

    return {
        "status": next_status,
        "audit": state.get("audit", []) + [audit_event],
    }
