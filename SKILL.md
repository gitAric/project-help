---
name: project-help
description: Rapidly onboard newcomers to unfamiliar software projects or orient them to one bounded area through evidence-backed system, business, code, runtime, developer-workflow, ownership, and change-impact analysis. Use when taking over a codebase; learning a whole repository; understanding one domain, service, package, module, feature, API, event, job, data entity, workflow, or directory; preparing handover material; tracing upstream/downstream behavior; finding where and how to make a safe change; or producing clear, polished SVG architecture and flow diagrams.
---

# Project Help

Build a useful mental model of an unfamiliar project from purpose and vocabulary down to executable paths and code branches. Optimize for a newcomer becoming productive, not for producing the largest possible report. Keep important claims traceable to repository evidence and keep inferred business meaning separate from confirmed implementation facts.

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
- Cite important claims with the narrowest useful evidence: file and line, symbol, active registration, schema, configuration, test, or authoritative project document.
- Label claims as **Confirmed**, **Inferred**, **Unknown**, or **Conflict**. Never turn naming, comments, folder structure, or recent authorship into confirmed runtime behavior or ownership without checking wiring or authoritative evidence.
- Distinguish implemented behavior from intended business behavior. Code proves implementation; product documents, specifications, and domain owners may be needed to prove intent.
- Prefer targeted discovery with `rg`, manifests, registration points, schemas, tests, and entrypoints over reading files sequentially.
- Keep the user updated during long investigations and deliver useful partial maps before exhaustive detail.
- Protect the newcomer from overload. Explain unfamiliar terms on first use, summarize before drilling down, and omit detail that does not advance the requested learning goal.

## Configure the learning mission

Derive four dimensions from the request and state them in a compact mission card. Make a reasonable labeled assumption when a dimension is omitted.

### Scope

- **Whole project**: repository, workspace, product, or system.
- **Focused scope**: business domain, service, application, package, module, feature, API, route, event, queue, scheduled job, CLI, data entity, workflow, directory, or named change area.

Do not treat every focused request as a feature. Preserve the user's actual boundary. For a focused scope, build only the minimum wider-system context needed to locate and explain it.

### Depth

- **Quick orientation**: purpose, vocabulary, location, major components, one golden path, developer entrypoints, and a short reading route.
- **Working knowledge**: important variants, data, interfaces, permissions, tests, operations, and common change points.
- **Implementation deep dive**: decision branches, invariants, transactions, concurrency, errors, retries, generated or dynamic behavior, and change-impact boundaries.

Default to quick orientation for an open-ended newcomer request and working knowledge for a named scope. Use deep-dive detail only when requested or needed to answer the stated goal.

### Audience

Adapt emphasis for backend, frontend, mobile, data, QA, SRE/platform, security, product/business, or mixed audiences. If no role is given, use a general software-maintainer lens.

### Goal

Classify the desired outcome as one or more of:

- orient and learn;
- prepare to modify or extend;
- debug or explain observed behavior;
- operate or support;
- review architecture, risk, or ownership;
- prepare onboarding or handover material.

Read [onboarding-playbook.md](references/onboarding-playbook.md) when tailoring depth, role, a focused boundary, a learning path, or a hands-on onboarding plan.

## Select the exploration shape

### Whole-project onboarding

Move from breadth to representative depth:

1. Purpose, actors, outcomes, vocabulary, and repository boundaries
2. Deployable applications, services, packages, shared infrastructure, and external systems
3. Business domains, capabilities, core entities, and major workflows
4. Runtime topology, data ownership, interfaces, events, jobs, and trust boundaries
5. Developer workflow: configure, build, run, test, debug, migrate, generate, and observe
6. One or more representative golden paths from trigger to observable outcome
7. Ownership evidence, evolution signals, active versus legacy areas, and operational risks
8. Safe-change map, recommended reading route, and practical newcomer exercises

For a large project, deliver a quick orientation first. Sample representative critical paths and mark unsampled areas rather than implying complete coverage.

### Focused-scope orientation or deep dive

Start with a scope boundary card that names what is included, excluded, assumed, and adjacent. Locate the scope on a minimal whole-system map, then analyze only the requested depth.

At quick depth, explain purpose, location, responsibilities, neighbors, entry surfaces, core vocabulary, and what to read first. At working or deep depth, trace call paths, data, state, integrations, errors, permissions, tests, observability, and change impact.

If the scope name maps to materially different candidates, show the candidates and ask only when choosing one would substantially change the result. Otherwise choose the best-supported interpretation and label it.

### Task-led or incident-led orientation

When the request starts from a proposed change, bug, alert, user action, or question such as “where would I change X?” or “why does Y happen?”, trace outward only as far as needed to build the required context. Return the entrypoint, current behavior, owned state, upstream and downstream effects, likely modification boundary, regression surface, and verification route.

## Execute the discovery workflow

### 1. Establish scope and evidence sources

Identify:

- Repository root, monorepo/workspace boundaries, submodules, generated or vendored areas, and the inspected revision
- Scope, depth, audience, goal, desired output, and any time or file budget
- Architecture records, product documents, API specifications, runbooks, issue links, tests, deployment configuration, and local-development guidance
- Evidence gaps that may require runtime observation or a domain-owner answer

Use the inventory helper when it saves time:

```bash
python3 <resolved-skill-directory>/scripts/project_inventory.py <repository-root> --max-depth 5
```

For a bounded directory, add `--focus-path <repository-relative-path>`. In Claude Code, replace `<resolved-skill-directory>` with `${CLAUDE_SKILL_DIR}`.

Treat helper output as navigation hints, not conclusions. Read [report-templates.md](references/report-templates.md) before composing a report.

### 2. Build a newcomer-first mental model

Answer these questions before exposing implementation detail:

- What problem does the system or selected scope solve, for whom, and with what observable outcome?
- Which domain terms, acronyms, entities, and status values must be understood first?
- What are the few major building blocks, and why are their boundaries meaningful?
- What is the representative trigger-to-outcome path?
- Where should a newcomer start reading, running, testing, and asking questions?

Create a small glossary. Distinguish domain language from framework terminology and repository-specific names. Call out misleading names, overloaded terms, and code-versus-documentation conflicts.

### 3. Build the structural and runtime map

Inspect high-signal files first:

- Root documentation, repository instructions, workspace and dependency manifests
- Application entrypoints, route or event registration, dependency injection, plugin registration, and configuration loading
- Deployment, container, orchestration, infrastructure-as-code, and environment examples
- Database migrations, schemas, event definitions, API contracts, generated-client boundaries, and feature flags
- Tests demonstrating integration or business behavior

For each first-party component, identify responsibility, runtime form, boundary, dependencies, data ownership, trust boundary, and externally visible interfaces. Verify that an apparent module is wired into a live entrypoint before calling it active. Separate current, legacy, experimental, example, generated, and test-only paths.

### 4. Reconstruct business architecture and golden paths

Start from actors and outcomes rather than folders. Map capabilities, policies, approvals, core entities and lifecycles, happy paths, alternate paths, failure and compensation paths, and manual intervention.

Connect each capability to its UI, service, module, data, integration, and tests. When only code is available, describe business meaning as inferred and cite the evidence.

### 5. Reconstruct the developer workflow

Find the documented or configured path to:

- bootstrap dependencies and configuration;
- build and start relevant components;
- seed, migrate, or generate data and code;
- run unit, integration, contract, and end-to-end tests;
- debug locally and inspect logs, metrics, traces, and audit records;
- use fixtures, mocks, emulators, or local dependencies.

Label commands as **Documented**, **Configured**, or **Runtime-verified**. Do not claim a command works merely because it exists, and do not execute it without authorization when it may mutate state or start infrastructure.

### 6. Catalog capabilities, features, and interfaces

For each relevant capability or feature, record actor and goal, entry surface, owner component, happy and alternate paths, data read and written, external effects, permissions, tenancy, flags, and explanatory tests.

For each relevant interface, trace provider, consumer, direction, protocol, operation or topic, schema source, authentication, validation, compatibility, idempotency, ordering, retry, timeout, rate limiting, transaction boundary, consistency, cache behavior, side effects, observability, and tests.

Call a system **upstream** when it supplies a trigger or data to the analyzed boundary and **downstream** when it receives a command, data, or side effect. State the reference boundary explicitly.

### 7. Trace detailed logic where needed

Follow registration and runtime wiring from the external trigger to the durable or observable outcome:

`route/event/job -> adapter -> application orchestration -> domain rule -> repository/integration -> response/event/state`

Record input normalization, authentication and authorization, flags, decision branches, state transitions, invariants, persistence, transactions, locking, cache, sync and async boundaries, errors, retries, compensation, partial success, observability, and test coverage at the selected depth.

Include exact symbols for non-obvious hops. Mark dynamic dispatch, reflection, generated code, runtime configuration, or unavailable dependencies that prevent confirmation.

### 8. Add ownership, evolution, and change-readiness

Use CODEOWNERS, ownership documents, package metadata, and team records as primary ownership evidence. Use Git history only as a secondary signal for recently changed or stable areas; do not equate authorship with ownership.

When useful, identify architectural decision records, compatibility constraints, migration paths, churn hotspots, legacy seams, and areas where tests or observability are weak.

For a proposed change, produce a task-to-code map: likely entry files and symbols, invariants to preserve, contracts and consumers affected, migrations or generated artifacts involved, tests to run, telemetry to watch, and rollback or compatibility concerns. Keep this hypothetical unless the user asks for implementation.

### 9. Produce polished SVG diagrams

Read [diagram-patterns.md](references/diagram-patterns.md) before drawing. When a diagram materially improves understanding, deliver a standalone `.svg` artifact rather than Mermaid source.

- Use the smallest diagram set that answers the learning goal: context, component/runtime, capability/value flow, focused-scope map, sequence, state, data lineage, or deployment.
- Prefer `scripts/render_svg.py` for flow and sequence diagrams so spacing, typography, arrows, colors, accessibility metadata, and legends stay consistent.
- Author SVG directly only when the helper cannot express the required visual. Keep it self-contained, use a `viewBox`, embed styles, avoid external assets and `foreignObject`, and include `<title>` and `<desc>`.
- Use solid edges for confirmed relationships and dashed edges only for useful, labeled inferences. Highlight the selected scope with one restrained accent color and mute surrounding context.
- Keep labels short, place edges behind nodes, avoid crossings, split overloaded diagrams, and put evidence citations in prose below the graphic.
- Validate every SVG with `scripts/validate_svg.py`. Render or visually inspect it when the environment supports image viewing, then fix clipping, overlap, weak contrast, tiny text, awkward whitespace, or unclear flow before delivery.
- If the user did not request files in the repository, write SVGs to a safe temporary or artifact directory and attach or link them. Do not leave generated diagrams in the analyzed repository without permission.

### 10. Cross-check and stage delivery

Before delivering:

- Confirm active entrypoints, interface shapes, state writes, side effects, transaction boundaries, flags, and environment-specific wiring.
- Reconcile diagrams, tables, call chains, terminology, and relationship directions.
- Maintain a coverage ledger showing inspected, sampled, and uninspected areas.
- State what the newcomer should now understand, what remains unknown, and the cheapest next learning step.
- Deliver quick orientation before deeper appendices. Stop at the requested depth instead of expanding every available dimension.

## Deliver role-appropriate output

Answer inline by default. Create persistent onboarding files in the project only when requested. Use the matching structure from [report-templates.md](references/report-templates.md).

For a quick newcomer orientation, prioritize:

1. Mission and one-minute summary
2. Polished SVG context map
3. Core vocabulary and building blocks
4. One golden path
5. Developer start/test/debug path
6. First reading route, common pitfalls, and next exercises

For full-project working knowledge, add business capabilities, interfaces, data, security, operations, ownership/evolution, feature catalog, critical paths, task-to-code map, coverage, risks, and evidence ledger.

For a focused scope, deliver the scope boundary and location first, then purpose, responsibilities, neighbors, entry surfaces, call or data flow, state, contracts, tests, operations, safe-change boundary, and next reading route at the selected depth.

For task-led or incident-led work, lead with the answer and traced path, then supply only the architecture context required to justify it.

When useful, include two or three short understanding checks or hands-on exercises that can be completed safely without production access. Do not turn the report into a quiz unless the user wants one.

## Handle incomplete evidence

Use these labels consistently:

- **Confirmed**: Directly supported by active wiring, implementation, schema, test, or authoritative project document.
- **Inferred**: Best explanation of several clues, but runtime behavior, ownership, or business intent is not fully verified.
- **Unknown**: Required evidence is absent or inaccessible.
- **Conflict**: Code, configuration, tests, or documentation disagree.

For each material unknown, state why it matters and the cheapest artifact, runtime observation, or stakeholder answer needed to close it. Never hide uncertainty behind a polished diagram.
