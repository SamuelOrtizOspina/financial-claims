# financial-claims

Agentic pipeline that triages financial claims: it normalises the intake,
checks the documentation is complete, investigates the file, recommends a
decision, and closes with an audit record.

Phase 1 is **deterministic** — rules and thresholds only, no model calls — so
the decision boundary is fully auditable before an LLM is introduced. See
[docs/phase1_design.md](docs/phase1_design.md) for the design and rationale.

## Layout

```
services/claims-orchestrator/
  src/
    main.py       CLI entry point
    state.py      ClaimState contract shared by every node
    graph.py      pipeline wiring (LangGraph, with a dependency-free fallback)
    nodes/
      intake.py           normalise and classify the payload
      completeness.py     required documents per claim type + routing
      investigation.py    checks and risk score
      recommendation.py   decision, payout, rationale
      audit.py            final record
docs/phase1_design.md
datasets/sample_claims.json
```

## Pipeline

```
intake -> completeness -> [investigation ->] recommendation -> audit
```

A claim missing required documents skips investigation and is recommended as
`pending_information`. Every path still ends at `audit`, so no claim leaves the
graph without a record.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows;  source .venv/bin/activate on Unix
pip install -r services/claims-orchestrator/requirements.txt
```

`langgraph` is the intended runtime. Without it, `graph.py` falls back to
`run_sequential`, which applies the same state-merge semantics — useful for a
quick run, not for production.

## Run

From `services/claims-orchestrator`:

```bash
python -m src.main                              # bundled sample claims
python -m src.main --input path/to/claims.json  # one claim object or an array
python -m src.main --persist                    # write records to datasets/audit/
python -m src.main --json                       # emit the audit records
```

Example output:

```
claim      CLM-0003  (service_not_rendered)
amount     1,750.00 EUR
complete   True
risk       0.55
decision   manual_review  payout 1,750.00 EUR  human_review=True
  - [medium] amount_threshold: Claimed amount exceeds the auto-approval limit.
  - [high] reporting_delay: Claim was reported outside the reporting window allowed by policy.
  > Risk score 0.55 exceeds the auto-approval ceiling 0.40.
```

## Decision policy

| Condition | Decision |
|---|---|
| documentation incomplete | `pending_information` |
| risk ≥ 0.75 | `deny` |
| risk ≥ 0.40, or any high-severity finding, or amount > 1,000 | `manual_review` |
| otherwise | `approve` |

Thresholds live as named constants in
[investigation.py](services/claims-orchestrator/src/nodes/investigation.py) and
[recommendation.py](services/claims-orchestrator/src/nodes/recommendation.py).
They are placeholders and need calibration against historical outcomes before
any production use.

## Input format

```json
{
  "claim_id": "CLM-0001",
  "customer_id": "CUS-4417",
  "claim_type": "duplicate_charge",
  "claimed_amount": 240.5,
  "currency": "USD",
  "incident_date": "2026-08-30",
  "description": "Charged twice for the same subscription...",
  "documents": [
    { "doc_type": "transaction_statement", "ref": "stmt-0001.pdf", "received_at": "2026-09-01" }
  ]
}
```

`claim_id`, `claim_type` and `currency` are optional: intake generates an id,
infers the type from the description, and defaults the currency to USD.
