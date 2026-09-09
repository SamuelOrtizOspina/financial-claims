"""Completeness: check that the documents required for the claim type are present."""

from __future__ import annotations

from typing import Any

from ..state import ClaimState, ClaimType, audit_event

# Documentation policy per claim type. Kept as a single table so the requirement
# set stays auditable and easy to review with the business.
REQUIRED_DOCUMENTS: dict[ClaimType, tuple[str, ...]] = {
    "unauthorized_transaction": ("id_document", "transaction_statement", "police_report"),
    "duplicate_charge": ("transaction_statement",),
    "billing_error": ("transaction_statement", "invoice"),
    "service_not_rendered": ("invoice", "contract"),
    "unknown": ("id_document", "transaction_statement"),
}

# Claims at or above this amount always need proof of identity.
HIGH_VALUE_THRESHOLD = 5000.0


def completeness(state: ClaimState) -> dict[str, Any]:
    """Compare the documents on file against the policy for this claim type."""
    claim_type: ClaimType = state.get("claim_type", "unknown")
    required = list(REQUIRED_DOCUMENTS.get(claim_type, REQUIRED_DOCUMENTS["unknown"]))

    if state.get("claimed_amount", 0.0) >= HIGH_VALUE_THRESHOLD and "id_document" not in required:
        required.append("id_document")

    provided = {doc["doc_type"] for doc in state.get("documents", [])}
    missing = [doc_type for doc_type in required if doc_type not in provided]
    is_complete = not missing

    return {
        "required_documents": required,
        "missing_documents": missing,
        "is_complete": is_complete,
        "status": "under_investigation" if is_complete else "incomplete",
        "audit_trail": [
            audit_event(
                "completeness",
                "documents_checked",
                required=required,
                provided=sorted(provided),
                missing=missing,
                is_complete=is_complete,
            )
        ],
    }


def route_after_completeness(state: ClaimState) -> str:
    """Conditional edge: investigate a complete file, otherwise close it as pending."""
    return "investigation" if state.get("is_complete") else "recommendation"
