import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[4] / "insumos-negocio" / "datos-sinteticos"


def load_json(filename: str) -> list[dict]:
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)


def get_case(case_id: str) -> dict:
    cases = load_json("casos.json")

    for case in cases:
        if case["case_id"] == case_id:
            return case

    raise ValueError(f"Case not found: {case_id}")


def get_transactions(transaction_refs: list[str]) -> dict:
    transactions = load_json("transacciones.json")
    indexed = {item["transaction_id"]: item for item in transactions}

    found = [indexed[ref] for ref in transaction_refs if ref in indexed]

    missing = [ref for ref in transaction_refs if ref not in indexed]

    return {
        "items": found,
        "missing_refs": missing,
        "complete": not missing,
    }


def get_evidence(evidence_refs: list[str]) -> dict:
    evidence = load_json("evidencias.json")
    indexed = {item["evidence_id"]: item for item in evidence}

    found = [indexed[ref] for ref in evidence_refs if ref in indexed]

    missing = [ref for ref in evidence_refs if ref not in indexed]

    suspicious = [
        item["evidence_id"]
        for item in found
        if item["trust_label"] == "instruccion_potencial"
    ]

    return {
        "items": found,
        "missing_refs": missing,
        "suspicious_refs": suspicious,
        "complete": not missing,
    }


def get_case_context(case_id: str) -> dict:
    case = get_case(case_id)
    claim = case["claim"]

    transactions = get_transactions(claim.get("transaction_refs", []))

    evidence = get_evidence(case.get("evidence_refs", []))

    return {
        "case": case,
        "claim": claim,
        "transactions": transactions,
        "evidence": evidence,
    }
