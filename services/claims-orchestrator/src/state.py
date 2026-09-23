from typing import TypedDict


class ClaimState(TypedDict, total=False):
    claim: dict
    customer_context: dict
    evidence: list[dict]
    evidence_refs: list[str]
    transactions: list[dict]
    missing_evidence: list[str]
    contradictions: list[str]
    policy_findings: list[dict]
    risk_assessment: dict | None
    recommendation: dict | None
    status: str
    errors: list[dict]
    audit: list[dict]
