from src.state import ClaimState
from src.tools.local_tools import (
    get_evidence,
    get_transactions,
)


def investigation_node(state: ClaimState) -> dict:
    claim = state["claim"]

    transaction_result = get_transactions(claim.get("transaction_refs", []))

    evidence_result = get_evidence(state.get("evidence_refs", []))

    return {
        "evidence": evidence_result["items"],
        "missing_evidence": (
            transaction_result["missing_refs"] + evidence_result["missing_refs"]
        ),
        "errors": [],
        "status": "investigating",
    }
