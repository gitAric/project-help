# Report Templates

Use the full-project template for onboarding and the focused template for one feature. Keep the first screen concise; move evidence and implementation depth later.

## Contents

1. Evidence notation
2. Full-project onboarding report
3. Focused-feature report
4. Reusable tables
5. Completion checklist

## Evidence notation

Assign short evidence IDs in complex reports:

| ID | Status | Claim supported | Evidence |
|---|---|---|---|
| E1 | Confirmed | Example claim | `path/to/file.ext:line`, `SymbolName` |
| E2 | Inferred | Example inference | Clues from E1 and E3; runtime confirmation missing |

Use clickable absolute local file links when the client supports them. Otherwise use repository-relative `path:line` plus a symbol. Cite generated files only when the generated artifact itself controls runtime behavior; otherwise find its source.

## Full-project onboarding report

```markdown
# Project onboarding: <project>

## 1. Executive snapshot

- Scope and revision:
- What the system does:
- Primary actors and outcomes:
- Architecture style and deployable units:
- Critical dependencies:
- Coverage and confidence:

## 2. System context

<Mermaid context diagram>

Key relationships and evidence:

## 3. Component and runtime architecture

<Mermaid component diagram>

| Component | Responsibility | Runtime/deployment | Data | Inbound | Outbound | Evidence |
|---|---|---|---|---|---|---|

## 4. Business architecture

<Capability or value-flow diagram>

| Domain/capability | Actor outcome | Core entities | Implementing components | Confidence |
|---|---|---|---|---|

## 5. Feature catalog

| Capability | Feature | Actor/trigger | Happy-path outcome | Owner component | Important variants | Evidence |
|---|---|---|---|---|---|---|

## 6. Interfaces and dependencies

<Interface matrix>

## 7. Critical paths

### <critical path>

- Trigger and outcome:
- Call chain:
- State and side effects:
- Failure behavior:
- Evidence:

## 8. Data, security, and operations

- Data ownership and consistency:
- Authentication/authorization/tenancy:
- Jobs, events, retries, and recovery:
- Logs, metrics, traces, and audit:
- Deployment and environment differences:

## 9. Risks, conflicts, and unknowns

| Item | Status | Why it matters | Cheapest next check |
|---|---|---|---|

## 10. Recommended reading route

1. <file or symbol> — <what it teaches>
2. ...

## Evidence ledger

<Evidence table>
```

## Focused-feature report

```markdown
# Feature deep dive: <feature>

## 1. Location card

- Location: System > Domain > Service/package > Module > Entrypoint
- Business purpose:
- Primary actor or caller:
- Trigger and observable outcome:
- Architectural owner:
- Confidence and scope:

<Highlighted Mermaid architecture map>

## 2. Entry surfaces and boundaries

| Surface | Operation/topic/route | Caller | Handler | Auth/validation | Evidence |
|---|---|---|---|---|---|

## 3. End-to-end behavior

- Happy path:
- Alternate paths:
- Call chain:

<Sequence diagram>

## 4. Detailed logic

1. Preconditions and normalization
2. Authorization and feature gating
3. Decision branches and domain rules
4. State transitions and invariants
5. Persistence, transaction, cache, and consistency
6. Integrations, events, jobs, and side effects
7. Error, retry, rollback, compensation, and partial success

## 5. Data and interface contracts

<Interface table>

## 6. Tests and observability

- Tests proving behavior:
- Logs, metrics, traces, and audit:
- Important uncovered paths:

## 7. Change-impact boundary

- Directly owned code:
- Upstream callers:
- Downstream consumers:
- Schemas/contracts requiring compatibility:
- Likely regression areas:

## 8. Risks and unknowns

| Item | Status | Why it matters | Cheapest next check |
|---|---|---|---|

## Evidence ledger

<Evidence table>
```

## Reusable tables

### Interface matrix

| Direction | Provider | Consumer | Type | Operation/topic | Contract | Auth | Reliability/consistency | Implementation | Evidence |
|---|---|---|---|---|---|---|---|---|---|

Use `Inbound`, `Outbound`, or `Internal` relative to the analyzed system or focused feature. Spell out bidirectional relationships as two rows when their contracts or failure behavior differ.

### Detailed interface logic

| Concern | Finding | Status | Evidence |
|---|---|---|---|
| Input and defaults | | | |
| Validation | | | |
| Authentication/authorization | | | |
| Idempotency/deduplication | | | |
| Transaction/consistency | | | |
| Timeout/retry/rate limit | | | |
| Errors and compatibility | | | |
| Side effects and events | | | |
| Observability | | | |

### Business-to-code map

| Business capability | Feature/use case | Entry surface | Orchestration | Domain logic | Data/integration | Confidence |
|---|---|---|---|---|---|---|

## Completion checklist

- Put the requested feature on a wider architecture map.
- Separate confirmed facts from inference and unknowns.
- Trace active registration instead of relying on file names.
- Include non-HTTP interfaces and asynchronous behavior.
- Identify upstream and downstream relative to an explicit boundary.
- Cover permissions, errors, state, transactions, side effects, and tests at the requested depth.
- Keep diagrams, tables, call chains, and prose consistent.
- State coverage limits; do not equate sampled paths with full-project completeness.
