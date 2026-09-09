"""Intake: normalise an incoming claim payload into structured state."""

from __future__ import annotations

import re
import uuid
from typing import Any

from ..state import ClaimState, ClaimType, Document, audit_event

# Keyword heuristics used to classify a claim when the payload does not
# declare a type. Phase 2 replaces this with an LLM classifier.
_TYPE_KEYWORDS: dict[ClaimType, tuple[str, ...]] = {
    "unauthorized_transaction": ("unauthorized", "no reconozco", "fraud", "stolen", "robo"),
    "duplicate_charge": ("duplicate", "twice", "duplicado", "cobro doble"),
    "billing_error": ("wrong amount", "overcharged", "monto incorrecto", "billing"),
    "service_not_rendered": ("not delivered", "never received", "no recibi", "not rendered"),
}


def _classify(declared: str | None, description: str) -> ClaimType:
    if declared in _TYPE_KEYWORDS:
        return declared  # type: ignore[return-value]
    haystack = description.lower()
    for claim_type, keywords in _TYPE_KEYWORDS.items():
        if any(kw in haystack for kw in keywords):
            return claim_type
    return "unknown"


def _parse_amount(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = re.sub(r"[^\d.\-]", "", str(value or "0"))
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _normalise_documents(raw: Any) -> list[Document]:
    documents: list[Document] = []
    for item in raw or []:
        if isinstance(item, str):
            documents.append(Document(doc_type=item.strip().lower(), ref="", received_at=""))
        elif isinstance(item, dict):
            documents.append(
                Document(
                    doc_type=str(item.get("doc_type", "unknown")).strip().lower(),
                    ref=str(item.get("ref", "")),
                    received_at=str(item.get("received_at", "")),
                )
            )
    return documents


def intake(state: ClaimState) -> dict[str, Any]:
    """Validate and normalise ``raw_claim`` into the typed fields of the state."""
    raw = state.get("raw_claim") or {}
    errors: list[str] = []

    claim_id = str(raw.get("claim_id") or f"CLM-{uuid.uuid4().hex[:10].upper()}")
    customer_id = str(raw.get("customer_id") or "")
    if not customer_id:
        errors.append("intake: missing customer_id")

    description = str(raw.get("description") or "")
    claim_type = _classify(raw.get("claim_type"), description)
    amount = _parse_amount(raw.get("claimed_amount"))
    if amount <= 0:
        errors.append("intake: claimed_amount is missing or not positive")

    documents = _normalise_documents(raw.get("documents"))

    return {
        "claim_id": claim_id,
        "customer_id": customer_id,
        "claim_type": claim_type,
        "claimed_amount": amount,
        "currency": str(raw.get("currency") or "USD").upper(),
        "incident_date": str(raw.get("incident_date") or ""),
        "description": description,
        "documents": documents,
        "status": "received",
        "errors": errors,
        "audit_trail": [
            audit_event(
                "intake",
                "claim_normalised",
                claim_id=claim_id,
                claim_type=claim_type,
                claimed_amount=amount,
                document_count=len(documents),
            )
        ],
    }
