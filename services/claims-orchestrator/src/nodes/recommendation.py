"""Recommendation: turn findings and risk into a decision for a human to sign off."""

from __future__ import annotations

from typing import Any

from ..state import ClaimState, Recommendation, audit_event
from .investigation import AUTO_APPROVE_LIMIT

# Risk at or above this score can never be auto-approved.
MANUAL_REVIEW_RISK = 0.40

# Risk at or above this score is recommended for denial.
DENIAL_RISK = 0.75


def recommendation(state: ClaimState) -> dict[str, Any]:
    """Decide approve / manual_review / deny, or ask for the missing documents."""
    amount = state.get("claimed_amount", 0.0)
    risk = state.get("risk_score", 0.0)
    findings = state.get("findings", [])
    currency = state.get("currency", "USD")

    # A file routed here straight from completeness never reached investigation.
    if not state.get("is_complete", False):
        missing = state.get("missing_documents", [])
        rec = Recommendation(
            decision="pending_information",
            payout_amount=0.0,
            currency=currency,
            confidence=1.0,
            rationale=[
                "Missing required documentation: " + (", ".join(missing) or "unspecified") + "."
            ],
            requires_human_review=False,
        )
        return {
            "recommendation": rec,
            "status": "recommended",
            "audit_trail": [
                audit_event(
                    "recommendation",
                    "decided",
                    decision=rec["decision"],
                    missing=missing,
                )
            ],
        }

    rationale: list[str] = []
    high_severity = [f for f in findings if f["severity"] == "high"]

    if risk >= DENIAL_RISK:
        decision = "deny"
        payout = 0.0
        rationale.append(
            f"Risk score {risk:.2f} is at or above the denial threshold {DENIAL_RISK:.2f}."
        )
    elif risk >= MANUAL_REVIEW_RISK or high_severity or amount > AUTO_APPROVE_LIMIT:
        decision = "manual_review"
        payout = amount
        if risk >= MANUAL_REVIEW_RISK:
            rationale.append(
                f"Risk score {risk:.2f} exceeds the auto-approval ceiling {MANUAL_REVIEW_RISK:.2f}."
            )
        if amount > AUTO_APPROVE_LIMIT:
            rationale.append(
                f"Amount {amount:,.2f} {currency} is above the auto-approval "
                f"limit {AUTO_APPROVE_LIMIT:,.2f} {currency}."
            )
    else:
        decision = "approve"
        payout = amount
        rationale.append(
            f"Low risk ({risk:.2f}), documentation complete, amount within the "
            f"auto-approval limit."
        )

    for finding in high_severity:
        rationale.append("[high] " + finding["summary"])

    rec = Recommendation(
        decision=decision,
        payout_amount=round(payout, 2),
        currency=currency,
        confidence=round(1.0 - risk, 2),
        rationale=rationale,
        requires_human_review=decision != "approve",
    )

    return {
        "recommendation": rec,
        "status": "recommended",
        "audit_trail": [
            audit_event(
                "recommendation",
                "decided",
                decision=decision,
                payout_amount=rec["payout_amount"],
                risk_score=risk,
            )
        ],
    }
