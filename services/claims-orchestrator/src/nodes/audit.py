"""Audit: assemble the record that closes the run and can be replayed later."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..state import ClaimState, audit_event, now_iso

# Default location for persisted audit records.
AUDIT_DIR = Path(__file__).resolve().parents[4] / "datasets" / "audit"

# Bumped whenever the decision policy changes, so old records stay explainable.
POLICY_VERSION = "phase1.0"


def build_audit_record(state: ClaimState) -> dict[str, Any]:
    """Flatten the final state into a self-contained, reviewable record."""
    return {
        "claim_id": state.get("claim_id", ""),
        "customer_id": state.get("customer_id", ""),
        "claim_type": state.get("claim_type", "unknown"),
        "claimed_amount": state.get("claimed_amount", 0.0),
        "currency": state.get("currency", "USD"),
        "incident_date": state.get("incident_date", ""),
        "closed_at": now_iso(),
        "policy_version": POLICY_VERSION,
        "completeness": {
            "required_documents": state.get("required_documents", []),
            "missing_documents": state.get("missing_documents", []),
            "is_complete": state.get("is_complete", False),
        },
        "investigation": {
            "risk_score": state.get("risk_score", 0.0),
            "findings": state.get("findings", []),
        },
        "recommendation": state.get("recommendation"),
        "errors": state.get("errors", []),
        # Trail from the earlier nodes; this node's own event is appended by the graph.
        "trail": state.get("audit_trail", []),
    }


def persist_audit_record(record: dict[str, Any], directory: Path = AUDIT_DIR) -> Path:
    """Write one record as JSON. Phase 2 replaces this with an append-only store."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{record.get('claim_id') or 'unknown'}.json"
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def audit(state: ClaimState) -> dict[str, Any]:
    """Close the claim by building its audit record."""
    record = build_audit_record(state)
    rec = record.get("recommendation") or {}
    return {
        "audit_record": record,
        "status": "closed",
        "audit_trail": [
            audit_event(
                "audit",
                "record_built",
                policy_version=POLICY_VERSION,
                decision=rec.get("decision"),
                event_count=len(record["trail"]) + 1,
            )
        ],
    }
