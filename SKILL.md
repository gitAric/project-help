---
name: project-help
description: Comprehensively analyze unfamiliar software projects for takeover or handover through evidence-backed project-content, global overall architecture, business architecture, code, runtime, developer-workflow, ownership, and change-impact analysis with a diagram-rich SVG report. Also deeply analyze one named domain, service, package, module, feature, API, event, job, data entity, workflow, directory, change, or incident while locating it in mandatory global overall and business architecture SVGs and adding as many useful focused views as the evidence supports. Use when receiving a codebase, learning a whole project, preparing handover material, understanding one bounded function, tracing upstream/downstream behavior, finding where and how to make a safe change, or producing polished SVG architecture and flow diagrams.
---

# Project Help

Build a useful mental model of an unfamiliar project from purpose and vocabulary down to executable paths and code branches. Optimize for a newcomer becoming productive, not for producing the largest possible report. Keep important claims traceable to repository evidence and keep inferred business meaning separate from confirmed implementation facts.

## Fulfill the project-takeover contract

Treat the primary job as helping a person receive and take responsibility for a project. Support two modes:

- **Whole-project takeover** is the default. Analyze the complete first-party breadth: project purpose and contents, repository boundaries, business model and capabilities, global and runtime architecture, data and interfaces, critical workflows, developer workflow, security and operations, ownership and evolution, risks, and safe-change routes. Inspect every first-party top-level area and major capability; use representative deep traces for critical paths and state any uninspected depth explicitly.
- **Focused-function deep dive** applies when the user names one domain, service, module, feature, API, event, job, entity, workflow, directory, change, or incident. Analyze only that target in implementation detail after building enough whole-project context to locate it accurately. Do not expand unrelated internals.

Every mode has two non-optional baseline outputs:

1. A **global overall architecture SVG**. For focused work, highlight the target's system, domain, runtime, data, and integration position while keeping the surrounding project legible.
2. A separate **business architecture SVG**. For focused work, highlight the target's actor outcome, value-stream stage, business domain, capability, or supporting-enabler position.

If evidence is incomplete, still produce both evidence-backed partial views and label missing relationships or business intent as unknown in the report. Never invent content to make a diagram look complete, and never omit either baseline diagram. Reuse a validated baseline from the same project revision on follow-up requests, but update the scope highlight and evidence when needed.

Use a diagram-rich explanation by default. The two baselines are the minimum, not the target count. Continue creating separate SVG views whenever another view teaches a distinct, evidence-backed relationship, sequence, lifecycle, boundary, mapping, or impact. Do not impose an arbitrary maximum or limit the portfolio to diagram types named in this skill. Split concerns into more clear diagrams instead of compressing them into one crowded image; avoid only diagrams that are redundant, decorative, or unsupported.

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

Do not treat every focused request as a feature. Preserve the user's actual boundary. For a focused scope, still build both whole-project baseline maps at global granularity; after locating the target, inspect only the surrounding implementation context needed to explain it.

### Depth

- **Quick orientation**: purpose, vocabulary, location, major components, one golden path, developer entrypoints, and a short reading route.
- **Working knowledge**: important variants, data, interfaces, permissions, tests, operations, and common change points.
- **Implementation deep dive**: decision branches, invariants, transactions, concurrency, errors, retries, generated or dynamic behavior, and change-impact boundaries.

Default to working knowledge across the whole project for an open-ended takeover request and implementation deep dive for a named function. Use quick orientation only when the user explicitly requests a brief overview or when staging a large report before continuing to the contracted depth.

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

### Whole-project takeover

Cover the full first-party breadth, then move to representative depth:

1. Purpose, actors, outcomes, vocabulary, and repository boundaries
2. Project-content map: every first-party top-level application, service, package, library, infrastructure, schema, documentation, generated boundary, and legacy or experimental area
3. Global overall architecture: actors and channels, system boundaries, deployable units, shared platform, data stores, external systems, and major synchronous or asynchronous relationships
4. Business architecture: actor outcomes, value streams, business domains and capabilities, core entities, policies, approvals, manual work, and the capability-to-system bridge
5. Runtime topology, data ownership, interfaces, events, jobs, deployment, and trust boundaries
6. Developer workflow: configure, build, run, test, debug, migrate, generate, and observe
7. Representative and critical golden paths from trigger to observable outcome
8. Ownership evidence, evolution signals, active versus legacy areas, and operational risks
9. Safe-change map, recommended reading route, and practical newcomer exercises

Produce the two baseline SVGs before detailed appendices. Do not merge them because they answer different takeover questions. At quick depth, simplify both while keeping evidence and coverage boundaries explicit.

For a large project, deliver a quick orientation first and continue toward the requested takeover depth. Survey every first-party top-level area and major capability; sample representative implementation paths only after the full breadth is accounted for. Mark sampled and uninspected depth rather than implying file-by-file exhaustiveness.

### Focused-scope orientation or deep dive

Start with a scope boundary card that names what is included, excluded, assumed, and adjacent. Build or reuse both whole-project baseline diagrams, highlight the selected scope in each, and state its two locations explicitly:

- Technical location: `Project -> system/domain -> runtime/service/package -> entrypoint/data/integration`
- Business location: `Actor/outcome -> value stream -> domain/capability -> feature or supporting enabler`

If the target is purely technical, place it as a supporting enabler beneath the business capabilities it serves and label weak or absent business evidence. Then analyze only the target at the requested depth.

At quick depth, explain purpose, location, responsibilities, neighbors, entry surfaces, core vocabulary, and what to read first. At working or deep depth, trace call paths, data, state, integrations, errors, permissions, tests, observability, and change impact.

If the scope name maps to materially different candidates, show the candidates and ask only when choosing one would substantially change the result. Otherwise choose the best-supported interpretation and label it.

### Task-led or incident-led orientation

When the request starts from a proposed change, bug, alert, user action, or question such as “where would I change X?” or “why does Y happen?”, lead with the answer, then include the two baseline diagrams with the affected scope highlighted. Trace outward only as far as needed beyond those global locators. Return the entrypoint, current behavior, owned state, upstream and downstream effects, likely modification boundary, regression surface, and verification route.

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

### 3. Reconstruct the global overall architecture

Inspect high-signal files first:

- Root documentation, repository instructions, workspace and dependency manifests
- Application entrypoints, route or event registration, dependency injection, plugin registration, and configuration loading
- Deployment, container, orchestration, infrastructure-as-code, and environment examples
- Database migrations, schemas, event definitions, API contracts, generated-client boundaries, and feature flags
- Tests demonstrating integration or business behavior

Build the model from the outside in: actors and access channels, product or system boundaries, major first-party deployables and runtime services, shared platform or infrastructure, owned data stores, external systems, and the main synchronous, asynchronous, data, deployment, and trust-boundary relationships. Keep it global: group internals by meaningful boundary instead of turning every package into a node.

For each first-party component, identify responsibility, runtime form, boundary, dependencies, data ownership, trust boundary, and externally visible interfaces. Verify that an apparent module is wired into a live entrypoint before calling it active. Separate current, legacy, experimental, example, generated, and test-only paths. Render the confirmed global model as a standalone SVG before drilling into lower-level component maps; highlight the selected target when the mission is focused.

### 4. Reconstruct business architecture and golden paths

Start from actors and outcomes rather than folders. Map capabilities, policies, approvals, core entities and lifecycles, happy paths, alternate paths, failure and compensation paths, and manual intervention.

Organize the business view as actor or stakeholder -> value stream -> business domain and capability -> outcome. Show the core entities that move through the value stream and the policies, approvals, or manual steps that materially shape it. Do not substitute services, repositories, or directory names for business capabilities.

Connect each capability to its UI, service, module, data, integration, and tests in accompanying prose or a business-to-code table. When only code is available, describe business meaning as inferred and cite the evidence. Render this model as a second standalone SVG, separate from the global overall architecture; highlight the selected target's business position when the mission is focused.

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

Read [diagram-patterns.md](references/diagram-patterns.md) before drawing. Deliver the mandatory baselines and any additional useful diagrams as standalone `.svg` artifacts rather than Mermaid source.

- Always start with two separate baseline diagrams: **global overall architecture** and **business architecture**. They are mandatory for whole-project, focused-function, task-led, and incident-led work.
- For focused work, keep both diagrams global enough to show the project whole, mute unrelated detail, and highlight the target consistently in each view. The global diagram must show its technical position; the business diagram must show its capability, value-stream, or supporting-enabler position.
- Reuse same-revision baseline diagrams when trustworthy, but regenerate or update them when the project revision, scope mapping, or evidence changed.
- After the baselines, build a broad diagram portfolio. Consider repository/project structure, system context, domain and capability decomposition, component/runtime topology, deployment, interfaces and dependencies, event/job topology, core entity model, data ownership and lineage, value streams, critical process flows, call sequences, state lifecycles, decisions, permissions and trust boundaries, failure/recovery paths, developer workflow, build/test/deploy pipelines, observability, ownership/evolution, and change-impact or rollback maps.
- Treat that portfolio as open-ended. Invent a project-specific view when it explains an important relationship better than the named patterns. Do not stop because a type is absent from the list or unsupported by the helper.
- For whole-project takeover, create diagrams across each evidence-backed category that materially contributes to the full picture. For focused work, add multiple target-level views for call flow, state, data, interfaces, asynchronous behavior, failure paths, tests/operations, and change impact whenever those dimensions exist.
- Prefer `scripts/render_svg.py` for flow and sequence diagrams so spacing, typography, arrows, colors, accessibility metadata, and legends stay consistent.
- Author SVG directly when the helper cannot express the required visual; never skip a useful diagram merely because the renderer has no named type. Keep it self-contained, use a `viewBox`, embed styles, avoid external assets and `foreignObject`, and include `<title>` and `<desc>`.
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

Every delivery includes this baseline in order:

1. Mission and one-minute summary
2. Polished global overall architecture SVG
3. Polished business architecture SVG
4. Explicit technical and business location of any selected scope

Then include a diagram index or short visual reading route and continue with as many distinct SVG views as the evidence supports.

For a whole-project takeover, continue with diagram-backed project contents, core vocabulary and business model, component/runtime detail, critical golden paths, data and interfaces, developer workflow, security and operations, ownership and evolution, safe-change routes, risks, coverage, reading route, and exercises.

For a focused scope, follow the mandatory baseline with multiple useful target-level SVGs and the scope boundary, purpose, responsibilities, neighbors, entry surfaces, call or data flow, state, contracts, tests, operations, safe-change boundary, and next reading route at implementation depth unless the user requested less.

For task-led or incident-led work, lead with the answer, then supply both highlighted baseline diagrams, the traced path, and only the additional architecture context required to justify it.

When useful, include two or three short understanding checks or hands-on exercises that can be completed safely without production access. Do not turn the report into a quiz unless the user wants one.

## Handle incomplete evidence

Use these labels consistently:

- **Confirmed**: Directly supported by active wiring, implementation, schema, test, or authoritative project document.
- **Inferred**: Best explanation of several clues, but runtime behavior, ownership, or business intent is not fully verified.
- **Unknown**: Required evidence is absent or inaccessible.
- **Conflict**: Code, configuration, tests, or documentation disagree.

For each material unknown, state why it matters and the cheapest artifact, runtime observation, or stakeholder answer needed to close it. Never hide uncertainty behind a polished diagram.
