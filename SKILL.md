---
name: project-help
description: Rapidly understand an unfamiliar, large software project through evidence-backed architecture, business-capability, feature, interface, dependency, and implementation analysis. Use when taking over a codebase, preparing project onboarding or handover documentation, mapping system and business architecture, cataloging features and APIs, tracing upstream/downstream systems or data flows, explaining detailed interface logic, or deeply analyzing one specified feature while locating and highlighting it within the wider architecture.
---

# Project Help

Build a layered mental model of an unfamiliar project, from system context down to code branches. Keep every important claim traceable to repository evidence and keep inferred business meaning visibly separate from confirmed implementation facts.

## Resolve bundled resources portably

Use this skill unchanged in Codex and Claude Code:

- In Codex, resolve `scripts/` and `references/` relative to the directory containing this `SKILL.md`.
- In Claude Code, use `${CLAUDE_SKILL_DIR}` as the directory containing this `SKILL.md`.
- Never assume the user's current working directory is the skill directory.

## Apply the operating rules

- Work read-only unless the user explicitly asks for code or documentation changes.
- Read and obey repository instructions such as `AGENTS.md` before inspecting broadly.
- Inspect statically first. Do not install dependencies, start infrastructure, run migrations, call production services, or execute unfamiliar project scripts without authorization.
- Never expose secret values. Mention configuration key names and their roles only.
- Cite important claims with the narrowest useful evidence: file and line, symbol, route registration, schema, configuration, test, or project document.
- Label claims as **Confirmed**, **Inferred**, **Unknown**, or **Conflict**. Never turn naming conventions or comments into confirmed runtime behavior without checking wiring.
- Distinguish implemented behavior from intended business behavior. Code proves implementation; product documents, specifications, and domain owners may be needed to prove intent.
- Prefer targeted discovery with `rg`, manifests, route tables, dependency injection, schemas, and entrypoints over reading files sequentially.
- Keep the user updated during long repository investigations and deliver useful partial maps before exhaustive detail.

## Select the analysis mode

Choose one mode from the request. State the chosen scope and any assumptions before presenting findings.

### Full-project onboarding

Map the whole project in progressively deeper layers:

1. System context and repository boundaries
2. Deployable services, applications, packages, and shared infrastructure
3. Business domains, capabilities, actors, and major workflows
4. User-facing and machine-facing features
5. Interfaces, data stores, events, jobs, and upstream/downstream dependencies
6. Representative critical paths and implementation details
7. Risks, unknowns, and an efficient reading route for the new maintainer

For a very large project, prioritize breadth and representative critical paths first. Mark areas not yet sampled rather than implying complete coverage.

### Focused-feature deep dive

Analyze only the requested feature deeply, but first create or reuse a minimal whole-system context map. Locate the feature on that map and visually highlight it. Then trace its entrypoints, owners, call paths, data, integrations, state changes, errors, permissions, and tests.

If the feature name maps to several materially different flows, show the candidates and ask the user only when choosing one would change the result substantially. Otherwise make a scoped assumption and label it.

## Execute the discovery workflow

### 1. Establish scope and evidence sources

Identify:

- Repository root, monorepo/workspace boundaries, submodules, and generated or vendored areas
- User-requested depth, named feature, audience, and desired output format
- Available architecture records, product documents, API specifications, runbooks, issue links, tests, and deployment configuration
- Branch or revision being inspected when that matters

Use the inventory helper when it saves time:

In Codex, run:

```bash
python3 <resolved-skill-directory>/scripts/project_inventory.py <repository-root> --max-depth 5
```

In Claude Code, run:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/project_inventory.py" <repository-root> --max-depth 5
```

Treat the helper output as navigation hints, not conclusions. Read [report-templates.md](references/report-templates.md) before composing a final report.

### 2. Build the structural map

Inspect high-signal files first:

- Root documentation and repository instructions
- Workspace, package, dependency, build, and task-runner manifests
- Application entrypoints, route registration, dependency injection, plugin registration, and configuration loading
- Deployment, container, orchestration, infrastructure-as-code, and environment examples
- Database migrations, schemas, event definitions, API contracts, and generated-client boundaries
- Tests that demonstrate intended integration or business behavior

Identify each first-party component's responsibility, runtime form, owner boundary if evidenced, dependencies, data stores, and externally visible interfaces. Exclude generated and third-party code from architecture ownership while recording where it forms an integration boundary.

Verify that an apparent module is actually wired into a live entrypoint before calling it active. Note dead, experimental, legacy, or unreachable paths when evidence supports that distinction.

### 3. Reconstruct the business architecture

Start from actors and business outcomes, not folders. Map:

- Actors or personas
- Business domains and capabilities
- Core entities and their lifecycle
- Trigger-to-outcome workflows
- Policies, permissions, approvals, and business rules
- Failure, compensation, and manual-intervention paths

Connect each capability to the implementing UI, service, module, data store, and integration. When only code is available, describe the behavior as an inferred capability and explain the evidence behind the inference.

### 4. Catalog features

For each major feature, record:

- Actor and business goal
- Entry surface: UI route, API, event, scheduled job, CLI, import, or internal call
- Owning domain and component
- Happy path and important alternate paths
- Data read and written
- External side effects and downstream consumers
- Authentication, authorization, tenancy, and feature flags
- Tests or specifications that best explain the feature

Group features by business capability rather than by source directory alone.

### 5. Map interfaces and dependencies

Include all relevant interface types: HTTP, RPC, GraphQL, WebSocket, events and queues, scheduled jobs, webhooks, file exchange, database boundaries, storage, CLI, UI-to-backend calls, and public module contracts.

For each interface, trace:

- Provider, consumer, direction, protocol, operation or topic, and implementation entrypoint
- Request or message shape, response or output shape, and schema source
- Authentication, authorization, validation, defaults, and compatibility/version rules
- Idempotency, ordering, retries, timeout, rate limiting, pagination, and deduplication
- Transaction boundary, consistency model, cache behavior, side effects, and failure mapping
- Observability hooks and tests

Call a system **upstream** when it supplies a trigger or data to the analyzed flow; call it **downstream** when it receives commands, data, or side effects from that flow. Describe the direction explicitly when a relationship is bidirectional.

### 6. Trace detailed logic

Trace from the external trigger to the durable or observable outcome. Follow registration and runtime wiring, not filename similarity.

Record:

1. Preconditions and input normalization
2. Validation, authentication, authorization, tenancy, and flags
3. Orchestration and important decision branches
4. Domain state transitions and invariants
5. Persistence, transaction, locking, cache, and consistency behavior
6. Synchronous integrations and asynchronous publication
7. Error translation, retry, compensation, rollback, and partial-success behavior
8. Metrics, logs, traces, and audit records
9. Unit, integration, contract, and end-to-end coverage

For focused analysis, provide a compact call chain such as:

`route/event -> adapter -> application service -> domain rule -> repository/integration -> response/event`

Include exact symbols and evidence for every non-obvious hop. Mark dynamic dispatch, reflection, generated code, runtime configuration, or missing dependencies that prevent full confirmation.

### 7. Draw and validate the architecture

Read [diagram-patterns.md](references/diagram-patterns.md) before drawing.

Use Mermaid unless the user requests another format. Produce the smallest set that explains the system:

- System context diagram for actors and external systems
- Container/component diagram for services, modules, stores, and integrations
- Business flow or capability map
- Sequence diagram for a critical or requested feature
- State diagram only when lifecycle transitions are central

For a focused feature:

- Show enough surrounding context to establish its architectural location.
- Apply the `focus` class to every node owned by the feature.
- Keep neighboring components muted but readable.
- Label inbound and outbound boundaries.
- Add a short location statement such as `System > Domain > Service > Module > Entrypoint`.

Do not add an edge merely because a dependency seems likely. Mark inferred edges in the prose and use a dashed line only when the inference is useful and labeled.

### 8. Cross-check the model

Before delivering:

- Confirm entrypoints through route, job, event, plugin, or dependency-injection registration.
- Confirm interface shapes against schemas or serialization code, not controllers alone.
- Confirm data writes, side effects, and transaction boundaries in implementations.
- Check tests and configuration for alternate behavior, feature flags, and environment-specific wiring.
- Reconcile diagrams, tables, and prose so component names and relationship directions match.
- Ensure every architecture edge and major business claim has evidence or an uncertainty label.
- Separate current paths from legacy, unused, generated, example, and test-only paths.
- List material gaps and the exact artifact, runtime observation, or stakeholder answer needed to close each one.

## Deliver layered output

Answer inline by default. Create files in the project only when the user asks for persistent documentation.

For full-project onboarding, deliver:

1. Executive snapshot and scope
2. System and component architecture diagrams
3. Business capability and major workflow map
4. Feature catalog
5. Interface and upstream/downstream matrix
6. One or more critical-path deep dives
7. Data, runtime, security, and operational notes
8. Risks, conflicts, unknowns, and coverage limits
9. Evidence-backed recommended reading order

For a focused feature, deliver:

1. Feature location card and highlighted architecture map
2. Business purpose, actors, trigger, and outcome
3. Entrypoints and end-to-end call chain
4. Sequence or state diagram where useful
5. Interface, data, permissions, error, transaction, and side-effect details
6. Tests, observability, risks, unknowns, and change-impact boundary

Use concise summaries first and expandable detail afterward. Use local clickable file links when supported; otherwise cite `path:line` and symbol. Keep an evidence ledger for complex reports.

## Handle incomplete evidence

Use these labels consistently:

- **Confirmed**: Directly supported by active wiring, implementation, schema, test, or authoritative project document.
- **Inferred**: Best explanation of several clues, but runtime or business intent is not fully verified.
- **Unknown**: Required evidence is absent or inaccessible.
- **Conflict**: Code, configuration, tests, or documentation disagree.

For each important unknown, state why it matters and the cheapest next check. Never hide uncertainty behind a polished diagram.
