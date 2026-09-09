"""Investigation: run deterministic checks over the claim and score its risk."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from ..state import ClaimState, Finding, Severity, audit_event

# Weight each check contributes to the 0..1 risk score.
RISK_WEIGHTS: dict[str, float] = {
    "amount_threshold": 0.25,
    "reporting_delay": 0.20,
    "missing_incident_date": 0.10,
    "thin_description": 0.10,
    "no_supporting_evidence": 0.20,
    "high_value_no_police_report": 0.25,
}

# A claim reported later than this many days after the incident is a red flag.
MAX_REPORTING_DELAY_DAYS = 60

# Above this amount a claim can never be auto-approved.
AUTO_APPROVE_LIMIT = 1000.0

# Fraud claims at or above this amount require a police report.
POLICE_REPORT_THRESHOLD = 5000.0


def _parse_date(value: str) -> date | None:
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value, fmt).date()
        except (ValueError, TypeError):
            continue
    return None


def _finding(check: str, summary: str, severity: Severity, **evidence: Any) -> Finding:
    return Finding(check=check, summary=summary, severity=severity, evidence=evidence)


def investigation(state: ClaimState, today: date | None = None) -> dict[str, Any]:
    """Produce findings and a risk score. ``today`` is injectable for tests."""
    today = today or date.today()
    findings: list[Finding] = []

    amount = state.get("claimed_amount", 0.0)
    claim_type = state.get("claim_type", "unknown")
    description = state.get("description", "")
    documents = state.get("documents", [])

    if amount > AUTO_APPROVE_LIMIT:
        findings.append(
            _finding(
                "amount_threshold",
                "Claimed amount exceeds the auto-approval limit.",
                "medium",
                claimed_amount=amount,
                limit=AUTO_APPROVE_LIMIT,
            )
        )

    incident = _parse_date(state.get("incident_date", ""))
    if incident is None:
        findings.append(
            _finding(
                "missing_incident_date",
                "Incident date is absent or unparseable.",
                "low",
                raw_value=state.get("incident_date", ""),
            )
        )
    else:
        delay_days = (today - incident).days
        if delay_days > MAX_REPORTING_DELAY_DAYS:
            findings.append(
                _finding(
                    "reporting_delay",
                    "Claim was reported outside the reporting window allowed by policy.",
                    "high",
                    delay_days=delay_days,
                    max_allowed_days=MAX_REPORTING_DELAY_DAYS,
                )
            )

    word_count = len(description.split())
    if word_count < 10:
        findings.append(
            _finding(
                "thin_description",
                "Customer description is too short to assess the incident.",
                "low",
                word_count=word_count,
            )
        )

    provided = {doc["doc_type"] for doc in documents}
    if not (provided - {"id_document"}):
        findings.append(
            _finding(
                "no_supporting_evidence",
                "No evidentiary document beyond proof of identity was provided.",
                "medium",
                documents=sorted(provided),
            )
        )

    if (
        claim_type == "unauthorized_transaction"
        and amount >= POLICE_REPORT_THRESHOLD
        and "police_report" not in provided
    ):
        findings.append(
            _finding(
                "high_value_no_police_report",
                "High-value unauthorised-transaction claim without a police report.",
                "high",
                claimed_amount=amount,
                threshold=POLICE_REPORT_THRESHOLD,
            )
        )

    raw_score = sum(RISK_WEIGHTS.get(f["check"], 0.10) for f in findings)
    risk_score = round(min(raw_score, 1.0), 2)

    return {
        "findings": findings,
        "risk_score": risk_score,
        "status": "under_investigation",
        "audit_trail": [
            audit_event(
                "investigation",
                "checks_completed",
                checks_run=sorted(RISK_WEIGHTS),
                findings_raised=[f["check"] for f in findings],
                risk_score=risk_score,
            )
        ],
    }
