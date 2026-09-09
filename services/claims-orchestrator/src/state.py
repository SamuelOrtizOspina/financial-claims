"""Shared state contract for the claims orchestration graph.

Every node receives the full ``ClaimState`` and returns a *partial* dict with
only the keys it changed. LangGraph merges those partials into the state.

``audit_trail`` is the exception: it is annotated with ``operator.add`` so
appends from different nodes accumulate instead of overwriting each other.
"""

from __future__ import annotations

import operator
from datetime import datetime, timezone
from typing import Annotated, Any, Literal, TypedDict

ClaimStatus = Literal[
    "received",
    "incomplete",
    "under_investigation",
    "recommended",
    "closed",
]

ClaimType = Literal[
    "unauthorized_transaction",
    "billing_error",
    "service_not_rendered",
    "duplicate_charge",
    "unknown",
]

Decision = Literal["approve", "partial_approve", "deny", "manual_review", "pending_information"]

Severity = Literal["info", "low", "medium", "high"]


class Document(TypedDict):
    """A supporting document attached to the claim."""

    doc_type: str
    ref: str
    received_at: str


class Finding(TypedDict):
    """A single observation produced by the investigation node."""

    check: str
    summary: str
    severity: Severity
    evidence: dict[str, Any]


class Recommendation(TypedDict):
    decision: Decision
    payout_amount: float
    currency: str
    confidence: float
    rationale: list[str]
    requires_human_review: bool


class AuditEvent(TypedDict):
    ts: str
    node: str
    action: str
    detail: dict[str, Any]


class ClaimState(TypedDict, total=False):
    """State threaded through the whole graph."""

    # --- input -------------------------------------------------------------
    raw_claim: dict[str, Any]

    # --- set by intake -----------------------------------------------------
    claim_id: str
    customer_id: str
    claim_type: ClaimType
    claimed_amount: float
    currency: str
    incident_date: str
    description: str
    documents: list[Document]
    status: ClaimStatus

    # --- set by completeness ----------------------------------------------
    required_documents: list[str]
    missing_documents: list[str]
    is_complete: bool

    # --- set by investigation ----------------------------------------------
    findings: list[Finding]
    risk_score: float

    # --- set by recommendation ---------------------------------------------
    recommendation: Recommendation

    # --- set by audit --------------------------------------------------------
    audit_record: dict[str, Any]

    # --- accumulated across every node ---------------------------------------
    audit_trail: Annotated[list[AuditEvent], operator.add]
    errors: Annotated[list[str], operator.add]


def now_iso() -> str:
    """UTC timestamp used for every audit event."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def audit_event(node: str, action: str, **detail: Any) -> AuditEvent:
    """Build one audit-trail entry. Nodes return ``{"audit_trail": [event]}``."""
    return AuditEvent(ts=now_iso(), node=node, action=action, detail=detail)


def new_state(raw_claim: dict[str, Any]) -> ClaimState:
    """Seed state for a graph run."""
    return ClaimState(raw_claim=raw_claim, audit_trail=[], errors=[])
