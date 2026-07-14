# Report Templates

Use the template matching the learning mission, then enrich it with a diagram portfolio. Diagram placeholders are a floor, not a ceiling: add as many distinct SVG views as improve project understanding, including project-specific diagram types not named here. Keep the first screen useful to a newcomer and move evidence and implementation depth later.

## Contents

1. Evidence notation
2. Quick newcomer orientation
3. Whole-project takeover report
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

## 3. Global overall architecture

<Required linked or embedded polished SVG artifact>

Show the whole project's major technical and runtime shape. For a focused scope, keep the project whole visible and highlight the target's system, domain, runtime, data, and integration position.

Main takeaway and evidence for each important edge:

## 4. Business architecture

<Required linked or embedded polished SVG business-architecture artifact>

Show actors, outcomes, value streams, business domains and capabilities, core entities, and material policies or manual work. For a focused scope, keep the wider business model visible and highlight the target's capability, value-stage, or supporting-enabler position.

Additional diagram index and visual reading order:

1. <Diagram title> — <question it answers>
2. ...

## 5. Vocabulary and building blocks

| Term/component | Plain-language meaning | Why it matters | Evidence |
|---|---|---|---|

## 6. Representative golden path

- Trigger:
- Short call or data chain:
- State and side effects:
- Observable outcome:
- Important failure boundary:

<One or more polished SVG sequence, process, decision, state, data, or failure-path artifacts>

## 7. Developer starting point

| Need | Command, file, or symbol | Status | Notes |
|---|---|---|---|
| Configure | | Documented / Configured / Runtime-verified | |
| Build/start | | | |
| Test | | | |
| Debug/observe | | | |

## 8. Read next

1. <file or symbol> — <question it answers>
2. ...

## 9. Pitfalls, unknowns, and next exercise

- Misleading name or common misconception:
- Material unknown:
- Cheapest next check:
- Safe hands-on exercise:
```

## Whole-project takeover report

```markdown
# Project takeover: <project>

## 1. Executive snapshot and learning mission

- Scope, depth, audience, goal, and revision:
- What the system does:
- Primary actors and outcomes:
- Architecture style and deployable units:
- Critical dependencies and constraints:
- Coverage and confidence:
- Diagram index and recommended visual reading order:

## 2. Vocabulary and business model

<Glossary and core-entity lifecycle>

## 3. Global overall architecture

<Required polished SVG global overall architecture diagram>

Show actors and channels, owned system boundaries, major deployables and runtime services, shared platform, owned data, external systems, and major sync/async relationships. Summarize the main architectural shape, boundaries, and evidence below the diagram.

## 4. Business architecture and feature catalog

<Required polished SVG business architecture diagram>

Show actors and outcomes, value streams, business domains and capabilities, core entities, material policies or approvals, manual work, and major external business parties.

| Capability | Actor outcome | Feature/use case | Core entities | Implementing components | Confidence |
|---|---|---|---|---|---|

## 5. Project contents and repository map

<One or more SVG repository/content, workspace/package-dependency, and active/legacy-boundary diagrams>

| Area/path | Kind | Responsibility | Runtime/business role | Lifecycle status | Evidence |
|---|---|---|---|---|---|

Account for every first-party top-level area. Mark vendored, generated, example, test-only, experimental, legacy, and inactive content explicitly.

## 6. Component and runtime detail

<One or more SVG component, runtime, deployment, environment, event/job, and external-dependency diagrams>

| Component | Responsibility | Runtime/deployment | Owned data | Inbound | Outbound | Evidence |
|---|---|---|---|---|---|---|

## 7. Golden paths

### <critical path>

- Trigger and outcome:
- Call or data chain:
- State and side effects:
- Alternate and failure behavior:
- Evidence:

<A separate SVG process, sequence, decision, state, alternate-path, or failure/recovery view for each distinct critical path or phase>

## 8. Interfaces and dependencies

<SVG API/interface dependency, event topology, job topology, contract-compatibility, entity/data-model, ownership, and lineage diagrams as supported>

<Interface matrix>

## 9. Developer workflow

<SVG configure/build/run/test/debug, CI/CD, environment-transition, and observability-signal diagrams as supported>

- Configure and bootstrap:
- Build and start:
- Seed, migrate, and generate:
- Test layers and fastest trustworthy checks:
- Debug, logs, metrics, traces, and audit:
- Environment differences:

## 10. Security, reliability, and operations

<SVG trust-boundary, identity/permission, sensitive-data, failure/recovery, deployment, rollout, and rollback diagrams as supported>

- Trust boundaries and sensitive data:
- Authentication, authorization, and tenancy:
- Consistency, cache, jobs, events, retries, and recovery:
- Deployment, rollout, rollback, and manual intervention:

## 11. Ownership and evolution

<SVG ownership, evolution, migration, lifecycle-status, or change-hotspot diagrams as supported>

- Documented owners:
- Architectural decisions and compatibility constraints:
- Active, stable, legacy, experimental, and generated areas:
- Churn or migration signals:

## 12. Safe-change map

<SVG change-impact, regression-surface, verification, compatibility, migration, or rollback map>

<Task-to-code table>

## 13. Risks, conflicts, unknowns, and coverage

<SVG risk relationship, uncertainty boundary, or coverage map when it reveals useful structure>

<Risk table and coverage ledger>

## 14. Recommended reading and practice route

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
# Focused deep dive: <scope>

## 1. Scope boundary and location

- Target and scope type:
- Location: System > Domain > Service/package > Module > Entrypoint
- Included:
- Excluded:
- Necessary surrounding context:
- Depth, audience, and goal:
- Assumptions and confidence:

## 2. Global overall architecture position

<Required polished SVG global overall architecture with the target highlighted>

- Technical location: Project > system/domain > runtime/service/package > entrypoint/data/integration
- Important surrounding components and relationships:
- Evidence and unknowns:

## 3. Business architecture position

<Required polished SVG business architecture with the target highlighted>

- Business location: Actor/outcome > value stream > domain/capability > feature or supporting enabler
- Outcome or capabilities supported:
- Evidence and unknowns:

## 4. Purpose, vocabulary, and responsibilities

- Business or technical purpose:
- Actor/caller and observable outcome:
- Owned responsibilities and state:
- Responsibilities explicitly outside this boundary:
- Terms and status values:

## 5. Entry surfaces and neighbors

<SVG focused component/dependency/interface/event/job map>

| Surface | Operation/topic/route | Caller | Handler | Auth/validation | Evidence |
|---|---|---|---|---|---|

## 6. End-to-end behavior

- Happy path:
- Important alternate paths:
- Compact call or data chain:

<One or more SVG process, sequence, decision, alternate, failure, retry, compensation, or manual-intervention diagrams>

## 7. Detailed logic at requested depth

<SVG decision tree, state lifecycle, concurrency/transaction boundary, or rules map for each non-trivial area>

1. Preconditions and normalization
2. Authorization and feature gating
3. Decision branches and domain rules
4. State transitions and invariants
5. Persistence, transaction, cache, and consistency
6. Integrations, events, jobs, and side effects
7. Error, retry, rollback, compensation, and partial success

## 8. Data and interface contracts

<SVG entity relationship, data ownership, read/write, lineage, cache/consistency, API, event, and dependency diagrams as supported>

<Interface and owned-data tables>

## 9. Build, test, debug, and observe this scope

<SVG local workflow, test-layer, fixture/dependency, and observability-signal diagrams as supported>

- Local/development entrypoint:
- Relevant configuration:
- Tests proving behavior:
- Fixtures, mocks, or emulators:
- Logs, metrics, traces, and audit:
- Important uncovered paths:

## 10. Safe-change boundary

<SVG change-impact, regression, verification, rollout, and rollback map>

- Likely entry files and symbols:
- Invariants to preserve:
- Upstream callers and downstream consumers:
- Schemas, compatibility, migrations, and generated artifacts:
- Tests and telemetry to use for verification:
- Likely regression and rollback concerns:

## 11. Read next, risks, and parked discoveries

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

## Global overall architecture position

<Required polished SVG global overall architecture with the affected scope highlighted>

## Business architecture position

<Required polished SVG business architecture with the affected capability, value stage, or supporting enabler highlighted>

## Traced path

`trigger -> entrypoint -> orchestration -> domain/state -> integration -> outcome`

<One or more SVG focused component, sequence, decision, state, data, failure, and impact views>

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
- Include separate validated global overall architecture and business architecture SVGs in every report.
- In focused, task-led, and incident-led reports, highlight the target consistently in both baseline diagrams and state its technical and business locations.
- Keep technical/runtime nodes out of the business architecture unless they form a clearly labeled capability-to-system bridge.
- Account for every first-party top-level area in a whole-project takeover, while labeling sampled and uninspected implementation depth.
- Trace active registration instead of relying on file names.
- Include non-HTTP and asynchronous behavior when relevant.
- Identify upstream and downstream relative to an explicit boundary.
- Cover permissions, state, errors, transactions, side effects, tests, and observability at the selected depth.
- Distinguish documented, configured, and runtime-verified developer commands.
- Treat Git history as a secondary signal, not ownership proof.
- Include a safe-change and verification route when the goal involves modification or debugging.
- Deliver diagrams as validated, visually inspected SVG artifacts rather than Mermaid source.
- Treat the two baseline SVGs as the minimum, not the complete diagram set.
- Add diagrams across every evidence-backed project dimension that benefits from a distinct view; do not impose a fixed maximum or restrict output to diagram types named in the templates.
- Provide a diagram index and visual reading order when the portfolio is large.
- Split overloaded diagrams and remove redundant or decorative ones instead of reducing useful visual coverage.
- Keep diagrams, tables, terminology, call chains, and prose consistent.
- State coverage limits and the cheapest next learning step.
- Stop at the requested depth instead of emitting every template section mechanically.
