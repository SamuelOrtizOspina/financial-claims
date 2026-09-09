# Phase 1 — Claims Orchestrator Design

Status: draft · Scope: single-service, deterministic pipeline · Last updated: 2026-09-09

## 1. Objective

Triage inbound financial claims end to end without a human in the loop for the
mechanical steps, and hand a reviewer a decision that is already justified and
evidenced. Phase 1 deliberately uses **deterministic rules only** — no model
calls — so the decision boundary is fully auditable before any LLM is added.

Out of scope for Phase 1: LLM classification and extraction, document OCR,
external system lookups (core banking, KYC, card network), payment execution,
a persistent case store, and any UI.

## 2. Pipeline

```
                     ┌──────────────┐
   raw_claim ───────▶│    intake    │  normalise, classify, assign claim_id
                     └──────┬───────┘
                            ▼
                     ┌──────────────┐
                     │ completeness │  required docs per claim type
                     └──────┬───────┘
                 complete   │   incomplete
              ┌─────────────┴───────────────┐
              ▼                             │
      ┌───────────────┐                     │
      │ investigation │  checks, risk score │
      └───────┬───────┘                     │
              ▼                             ▼
                  ┌────────────────┐
                  │ recommendation │  decision + rationale
                  └───────┬────────┘
                          ▼
                    ┌──────────┐
                    │  audit   │  immutable record  ──▶ END
                    └──────────┘
```

An incomplete file skips investigation: there is nothing meaningful to assess
until the documents arrive, and scoring a partial file would produce a risk
number that looks authoritative but is not. It still passes through
`recommendation` (which emits `pending_information`) and `audit`, so **every
claim leaves the graph with a record** — no silent drops.

## 3. State contract

One `ClaimState` TypedDict ([state.py](../services/claims-orchestrator/src/state.py))
is threaded through the graph. Each node returns a *partial* dict containing
only the keys it owns; LangGraph merges them.

| Field | Owner | Notes |
|---|---|---|
| `raw_claim` | caller | untouched input payload |
| `claim_id`, `customer_id`, `claim_type`, `claimed_amount`, `currency`, `incident_date`, `description`, `documents` | intake | normalised, typed |
| `required_documents`, `missing_documents`, `is_complete` | completeness | drives routing |
| `findings`, `risk_score` | investigation | `risk_score` in `0.0..1.0` |
| `recommendation` | recommendation | decision, payout, confidence, rationale |
| `audit_record` | audit | flattened, self-contained |
| `audit_trail`, `errors` | all nodes | **accumulated** via `Annotated[list, operator.add]` |

Only `audit_trail` and `errors` accumulate. Everything else is last-write-wins,
and since each key has exactly one owning node there are no write conflicts.

## 4. Node responsibilities

**intake** — Coerces a loose payload into typed fields. Generates a `claim_id`
when absent, parses amounts out of formatted strings, normalises document
entries (plain strings or objects) to a single shape, and classifies the claim
type by keyword when the payload does not declare one. Missing `customer_id` or
a non-positive amount are recorded in `errors` rather than raised — a malformed
claim must still produce an audit record.

**completeness** — Compares documents on file against `REQUIRED_DOCUMENTS`, a
single table keyed by claim type so the policy is reviewable by the business in
one place. Claims at or above 5,000 additionally require proof of identity.

**investigation** — Runs six independent checks (amount above the auto-approval
limit, reporting delay beyond 60 days, missing incident date, thin description,
no evidence beyond ID, high-value fraud claim without a police report). Each
emits a `Finding` with severity and evidence; the weighted sum, capped at 1.0,
is the risk score. `today` is injectable so date-sensitive tests are stable.

**recommendation** — Maps risk and amount to a decision:

| Condition | Decision |
|---|---|
| documentation incomplete | `pending_information` |
| risk ≥ 0.75 | `deny` |
| risk ≥ 0.40, or any high-severity finding, or amount > 1,000 | `manual_review` |
| otherwise | `approve` |

Thresholds are module constants, not literals at the call site, so a policy
change is a one-line diff. `rationale` is a list of plain sentences naming the
threshold that fired — it is what the reviewer reads.

**audit** — Flattens the final state into a record carrying the inputs, both
intermediate results, the decision, the errors, and the full event trail,
stamped with `POLICY_VERSION`. The version stamp is what keeps an old record
explainable after the thresholds move.

## 5. Design decisions

- **Deterministic before probabilistic.** Every threshold is a named constant
  and every finding carries its evidence, so Phase 2 can swap in an LLM for
  classification and narrative and still diff its behaviour against this
  baseline.
- **No node raises on bad input.** Failures accumulate in `errors` and travel
  to the audit record. In claims handling, a lost claim is worse than a wrong
  recommendation a human can overturn.
- **Nothing is auto-denied on documentation alone.** A missing document is a
  request for information, never a rejection.
- **Auto-approval is narrow by construction** — complete file, risk below 0.40,
  no high-severity finding, amount at or below 1,000. Everything else reaches a
  human.
- **LangGraph optional at runtime.** `graph.py` compiles a real `StateGraph`
  when the package is installed and otherwise uses `run_sequential`, which
  applies the same reducer semantics. The fallback keeps the pipeline
  demonstrable and testable; it is not intended for production.

## 6. Datasets

`datasets/sample_claims.json` holds three claims chosen to exercise all three
terminal decisions: a clean low-value duplicate charge (`approve`), a
high-value fraud claim missing its police report (`pending_information`, and it
also verifies keyword classification since the payload declares no type), and a
stale high-value service claim (`manual_review`). Audit records are written to
`datasets/audit/`, which is git-ignored.

## 7. Open questions for Phase 2

1. Where does the case state live between the request for information and the
   customer's reply? Phase 1 has no persistence, so a resumed claim is a new run.
2. Duplicate detection needs claim history; there is no store to query yet.
3. Currency handling: thresholds are currently compared against the claim's own
   currency with no conversion.
4. `AUTO_APPROVE_LIMIT` and the risk thresholds are placeholders and need to be
   calibrated against historical outcomes before any production use.
5. Should the audit record be append-only and signed? Today it is a JSON file
   that a later run with the same `claim_id` will overwrite.
