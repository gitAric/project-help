# Report Templates

Select the smallest template that satisfies the learning mission. Keep the first screen useful to a newcomer and move evidence and implementation depth later.

## Contents

1. Evidence notation
2. Quick newcomer orientation
3. Full-project working-knowledge report
4. Focused-scope report
5. Task-led or incident-led report
6. Reusable tables
7. Completion checklist

## Evidence notation

Assign short evidence IDs in complex reports:

| ID | Status | Claim supported | Evidence |
|---|---|---|---|
| E1 | Confirmed | Example claim | `path/to/file.ext:line`, `SymbolName` |
| E2 | Inferred | Example inference | Clues from E1 and E3; runtime confirmation missing |

Use clickable absolute local file links when the client supports them. Otherwise use repository-relative `path:line` plus a symbol. Cite generated files only when the generated artifact itself controls runtime behavior; otherwise find its source.

## Quick newcomer orientation

```markdown
# Quick orientation: <project or scope>

## 1. Learning mission

- Scope:
- Depth: Quick orientation
- Audience and goal:
- Revision:
- Coverage and assumptions:

## 2. One-minute summary

- What it does and why it exists:
- Primary users or callers:
- Observable outcome:
- Architectural shape:
- Most important dependency or constraint:

## 3. System or scope map

<Linked or embedded polished SVG artifact>

Main takeaway and evidence for each important edge:

## 4. Vocabulary and building blocks

| Term/component | Plain-language meaning | Why it matters | Evidence |
|---|---|---|---|

## 5. Representative golden path

- Trigger:
- Short call or data chain:
- State and side effects:
- Observable outcome:
- Important failure boundary:

<Optional polished SVG sequence or flow artifact>

## 6. Developer starting point

| Need | Command, file, or symbol | Status | Notes |
|---|---|---|---|
| Configure | | Documented / Configured / Runtime-verified | |
| Build/start | | | |
| Test | | | |
| Debug/observe | | | |

## 7. Read next

1. <file or symbol> — <question it answers>
2. ...

## 8. Pitfalls, unknowns, and next exercise

- Misleading name or common misconception:
- Material unknown:
- Cheapest next check:
- Safe hands-on exercise:
```

## Full-project working-knowledge report

```markdown
# Project onboarding: <project>

## 1. Executive snapshot and learning mission

- Scope, depth, audience, goal, and revision:
- What the system does:
- Primary actors and outcomes:
- Architecture style and deployable units:
- Critical dependencies and constraints:
- Coverage and confidence:

## 2. Vocabulary and business model

<Glossary and core-entity lifecycle>

## 3. System context

<Polished SVG context diagram>

Key relationships and evidence:

## 4. Component and runtime architecture

<Polished SVG component/runtime diagram>

| Component | Responsibility | Runtime/deployment | Owned data | Inbound | Outbound | Evidence |
|---|---|---|---|---|---|---|

## 5. Business architecture and feature catalog

<Polished SVG capability or value-flow diagram>

| Capability | Actor outcome | Feature/use case | Core entities | Implementing components | Confidence |
|---|---|---|---|---|---|

## 6. Golden paths

### <critical path>

- Trigger and outcome:
- Call or data chain:
- State and side effects:
- Alternate and failure behavior:
- Evidence:

<Optional polished SVG sequence/state diagram>

## 7. Interfaces and dependencies

<Interface matrix>

## 8. Developer workflow

- Configure and bootstrap:
- Build and start:
- Seed, migrate, and generate:
- Test layers and fastest trustworthy checks:
- Debug, logs, metrics, traces, and audit:
- Environment differences:

## 9. Security, reliability, and operations

- Trust boundaries and sensitive data:
- Authentication, authorization, and tenancy:
- Consistency, cache, jobs, events, retries, and recovery:
- Deployment, rollout, rollback, and manual intervention:

## 10. Ownership and evolution

- Documented owners:
- Architectural decisions and compatibility constraints:
- Active, stable, legacy, experimental, and generated areas:
- Churn or migration signals:

## 11. Safe-change map

<Task-to-code table>

## 12. Risks, conflicts, unknowns, and coverage

<Risk table and coverage ledger>

## 13. Recommended reading and practice route

1. <file or symbol> — <what it teaches>
2. ...

- Safe exercise:
- Understanding check:
- Suggested next scope:

## Evidence ledger

<Evidence table>
```

## Focused-scope report

```markdown
# Focused orientation: <scope>

## 1. Scope boundary and location

- Target and scope type:
- Location: System > Domain > Service/package > Module > Entrypoint
- Included:
- Excluded:
- Necessary surrounding context:
- Depth, audience, and goal:
- Assumptions and confidence:

<Polished SVG highlighted scope map>

## 2. Purpose, vocabulary, and responsibilities

- Business or technical purpose:
- Actor/caller and observable outcome:
- Owned responsibilities and state:
- Responsibilities explicitly outside this boundary:
- Terms and status values:

## 3. Entry surfaces and neighbors

| Surface | Operation/topic/route | Caller | Handler | Auth/validation | Evidence |
|---|---|---|---|---|---|

## 4. End-to-end behavior

- Happy path:
- Important alternate paths:
- Compact call or data chain:

<Polished SVG sequence, state, or lineage diagram when useful>

## 5. Detailed logic at requested depth

1. Preconditions and normalization
2. Authorization and feature gating
3. Decision branches and domain rules
4. State transitions and invariants
5. Persistence, transaction, cache, and consistency
6. Integrations, events, jobs, and side effects
7. Error, retry, rollback, compensation, and partial success

## 6. Data and interface contracts

<Interface and owned-data tables>

## 7. Build, test, debug, and observe this scope

- Local/development entrypoint:
- Relevant configuration:
- Tests proving behavior:
- Fixtures, mocks, or emulators:
- Logs, metrics, traces, and audit:
- Important uncovered paths:

## 8. Safe-change boundary

- Likely entry files and symbols:
- Invariants to preserve:
- Upstream callers and downstream consumers:
- Schemas, compatibility, migrations, and generated artifacts:
- Tests and telemetry to use for verification:
- Likely regression and rollback concerns:

## 9. Read next, risks, and parked discoveries

- Reading route:
- Material risks and unknowns:
- Out-of-scope parking lot:
- Safe exercise or understanding check:

## Coverage and evidence ledger

<Coverage and evidence tables>
```

## Task-led or incident-led report

```markdown
# Trace: <change, behavior, bug, or alert>

## Answer first

- Current behavior or likely change location:
- Confidence:
- Most important caveat:

## Traced path

`trigger -> entrypoint -> orchestration -> domain/state -> integration -> outcome`

<Optional polished SVG focused map or sequence>

## Evidence and decision points

| Step | Symbol or contract | Behavior | Status | Evidence |
|---|---|---|---|---|

## Required context

- Owning boundary:
- Data and invariants:
- Upstream/downstream impact:
- Failure and observability:

## Safe next action

- Files/symbols to inspect or modify:
- Tests or runtime evidence needed:
- Compatibility, migration, or rollback concern:
- Remaining unknown:
```

## Reusable tables

### Interface matrix

| Direction | Provider | Consumer | Type | Operation/topic | Contract | Auth | Reliability/consistency | Implementation | Evidence |
|---|---|---|---|---|---|---|---|---|---|

Use `Inbound`, `Outbound`, or `Internal` relative to an explicit analyzed boundary. Spell out bidirectional relationships as two rows when contracts or failure behavior differ.

### Glossary

| Term | Plain-language meaning | Code representation | Caveat/conflict | Evidence |
|---|---|---|---|---|

### Business-to-code map

| Business capability | Feature/use case | Entry surface | Orchestration | Domain logic | Data/integration | Confidence |
|---|---|---|---|---|---|---|

### Task-to-code map

| Task | Start here | Likely change area | Invariant/contract | Tests | Telemetry/rollback |
|---|---|---|---|---|---|

### Developer workflow

| Need | Command/file/symbol | Status | Side effects or prerequisites | Evidence |
|---|---|---|---|---|

Status is `Documented`, `Configured`, or `Runtime-verified`.

### Ownership and evolution

| Area | Documented owner | Ownership evidence | Recent-change signal | Lifecycle status | Confidence |
|---|---|---|---|---|---|

### Coverage ledger

| Area or path | Coverage | Evidence sampled | Confidence | Not inspected / next check |
|---|---|---|---|---|

Use `Inspected`, `Sampled`, or `Not inspected`; never convert sample coverage into a percentage without a defensible denominator.

### Risk and unknowns

| Item | Status | Why it matters | Cheapest next check |
|---|---|---|---|

## Completion checklist

- State scope, depth, audience, goal, revision, and assumptions.
- Explain purpose and vocabulary before implementation detail.
- Put a focused scope on a minimal wider-system map.
- Trace active registration instead of relying on file names.
- Include non-HTTP and asynchronous behavior when relevant.
- Identify upstream and downstream relative to an explicit boundary.
- Cover permissions, state, errors, transactions, side effects, tests, and observability at the selected depth.
- Distinguish documented, configured, and runtime-verified developer commands.
- Treat Git history as a secondary signal, not ownership proof.
- Include a safe-change and verification route when the goal involves modification or debugging.
- Deliver diagrams as validated, visually inspected SVG artifacts rather than Mermaid source.
- Keep diagrams, tables, terminology, call chains, and prose consistent.
- State coverage limits and the cheapest next learning step.
- Stop at the requested depth instead of emitting every template section mechanically.
