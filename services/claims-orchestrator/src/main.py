"""CLI entry point for the claims orchestrator.

    python -m src.main                          # run the bundled sample claims
    python -m src.main --input claims.json      # run a file (object or array)
    python -m src.main --input claims.json --persist --json

Run it from ``services/claims-orchestrator``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .graph import LANGGRAPH_AVAILABLE, run_claim
from .nodes.audit import persist_audit_record
from .state import ClaimState

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = REPO_ROOT / "datasets" / "sample_claims.json"


def load_claims(path: Path) -> list[dict[str, Any]]:
    """Read a JSON file holding either one claim object or a list of them."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        return [payload]
    if isinstance(payload, list):
        return payload
    raise ValueError(f"{path}: expected a JSON object or array of claim objects")


def format_summary(state: ClaimState) -> str:
    rec = state.get("recommendation") or {}
    lines = [
        f"claim      {state.get('claim_id')}  ({state.get('claim_type')})",
        f"amount     {state.get('claimed_amount'):,.2f} {state.get('currency')}",
        f"complete   {state.get('is_complete')}"
        + (
            f"  missing: {', '.join(state.get('missing_documents', []))}"
            if state.get("missing_documents")
            else ""
        ),
        f"risk       {state.get('risk_score', 0.0):.2f}",
        f"decision   {rec.get('decision')}"
        f"  payout {rec.get('payout_amount', 0.0):,.2f} {rec.get('currency', '')}"
        f"  human_review={rec.get('requires_human_review')}",
    ]
    for finding in state.get("findings", []):
        lines.append(f"  - [{finding['severity']}] {finding['check']}: {finding['summary']}")
    for reason in rec.get("rationale", []):
        lines.append(f"  > {reason}")
    for error in state.get("errors", []):
        lines.append(f"  ! {error}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run claims through the orchestration graph.")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"JSON file with one claim or a list of claims (default: {DEFAULT_INPUT}).",
    )
    parser.add_argument("--persist", action="store_true", help="Write audit records to datasets/audit/.")
    parser.add_argument("--json", action="store_true", help="Print the audit records instead of a summary.")
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"input file not found: {args.input}", file=sys.stderr)
        return 2

    runtime = "langgraph" if LANGGRAPH_AVAILABLE else "sequential fallback (langgraph not installed)"
    print(f"runtime: {runtime}\n", file=sys.stderr)

    records: list[dict[str, Any]] = []
    for raw_claim in load_claims(args.input):
        state = run_claim(raw_claim)
        record = state.get("audit_record", {})
        records.append(record)

        if args.persist:
            path = persist_audit_record(record)
            print(f"wrote {path}", file=sys.stderr)
        if not args.json:
            print(format_summary(state))
            print("-" * 72)

    if args.json:
        print(json.dumps(records, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
