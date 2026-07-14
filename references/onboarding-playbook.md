# Project Takeover and Focused-Function Playbook

Use this playbook to tailor a complete project takeover or one focused-function deep dive to the recipient's scope, depth, role, and practical goal. Keep the output progressive: establish the whole-project technical and business maps first, then expose the implementation detail required by the selected mode.

## Contents

1. Mission router
2. Learning journey
3. Capability model
4. Audience lenses
5. Focused-scope rules
6. Practical learning and continuity
7. Completion signals

## Mission router

Classify a request across four dimensions:

| Dimension | Values | Default |
|---|---|---|
| Scope | Whole project; domain; service; app; package; module; feature; API; event; job; entity; workflow; directory; change area | Whole project unless a bounded target is named |
| Depth | Quick orientation; working knowledge; implementation deep dive | Working knowledge for whole-project takeover; implementation deep dive for named scope |
| Audience | General maintainer; backend; frontend/mobile; data; QA; SRE/platform; security; product/business | General maintainer |
| Goal | Learn; modify; debug; operate; review; hand over | Learn |

State the chosen configuration in a compact mission card. Do not ask the user to choose values that can be inferred safely from the request.

## Learning journey

Move through these stages and stop when the requested depth is satisfied.

### Stage 1: Landmarks

Establish:

- the system's purpose, actors, and observable outcomes;
- repository and deployable boundaries;
- five to nine major building blocks;
- the selected scope's location;
- the first files and symbols worth reading.

For every mission, turn these landmarks into a global overall architecture SVG covering actors and channels, owned boundaries, major runtimes, shared platform, data stores, external systems, and principal relationships. Highlight the target when the mission is focused.

### Stage 2: Language and business model

Explain:

- domain terms, acronyms, overloaded names, and important status values;
- core entities and lifecycles;
- major capabilities, policies, approvals, and business rules;
- the difference between intended behavior and confirmed implementation.

For every mission, turn this model into a separate business architecture SVG covering actors and outcomes, value streams, domains and capabilities, core entities, policies, approvals, and material manual work. Highlight the target's capability, value-stage, or supporting-enabler position when the mission is focused. Do not use the technical architecture as a substitute.

### Stage 3: Golden paths

Trace every distinct critical trigger-to-outcome flow required by the selected mode. Use a separate SVG sequence or process view for each important path or phase, and add alternate, failure, compensation, and manual-intervention diagrams when evidence supports them. Prefer several clear diagrams over one shallow or overloaded flow.

### Stage 4: Runtime and data

Connect services, processes, stores, caches, events, jobs, external systems, trust boundaries, configuration, and deployment environments. Explain data ownership and consistency in practical terms.

Turn distinct runtime and data questions into separate component, deployment, interface, event/job, entity, ownership, lineage, state, and trust-boundary SVGs instead of relying only on prose.

### Stage 5: Developer loop

Show how a newcomer can configure, build, run, test, debug, migrate, generate, and observe the relevant area. Distinguish documented, configured, and runtime-verified commands.

Visualize the development and delivery loop, test layers, environment transitions, or observability signal path whenever they contain multiple dependent steps.

### Stage 6: Safe change readiness

Map common tasks to entrypoints, invariants, contracts, data changes, generated artifacts, tests, telemetry, and compatibility or rollback concerns.

Produce change-impact, verification, migration, rollout, or rollback SVGs for important change classes rather than leaving the relationships only in a checklist.

### Stage 7: Independent navigation

Provide a reading route, search anchors, likely domain-owner evidence, safe exercises, and next questions so the newcomer can continue without relying on a full rescan.

## Capability model

Cover every capability category for a whole-project takeover. For a focused-function deep dive, select only the detail that advances the target while retaining both mandatory project-wide baseline maps.

### System comprehension

- Global overall architecture: actors, channels, system/runtime boundaries, platform, data, external systems, and main relationships
- Business architecture: outcomes, value streams, domains, capabilities, entities, policies, and manual work
- System context and repository boundaries
- Component and runtime topology
- Business capability and value-flow map
- Core entity lifecycle and data ownership
- Interface, event, job, and external-dependency map

### Code navigation

- Entrypoint and registration discovery
- Business-to-code mapping
- Call-chain and state-transition tracing
- Generated, dynamic, legacy, experimental, and unreachable path detection
- Task-to-code and likely regression mapping

### Developer productivity

- Bootstrap, build, run, test, debug, migrate, and generate workflow
- Fixture, mock, emulator, seed, and local-dependency discovery
- Configuration key and environment-difference map
- Test pyramid and fastest trustworthy verification route
- Logs, metrics, traces, audits, and local diagnostic entrypoints

### Team and evolution awareness

- CODEOWNERS or documented team ownership
- Architectural decisions and compatibility constraints
- Git history as a secondary signal for churn and stability
- Migration seams, deprecation paths, and likely legacy hotspots
- Known risks, conflicts, missing tests, and observability gaps

### Learning support

- Layered explanations and first-use definitions
- Glossary and misleading-name warnings
- Recommended reading route with a purpose for each stop
- Safe hands-on exercises and understanding checks
- Coverage ledger and a reusable continuation map

### Diagram-rich communication

- Treat the mandatory global overall and business architecture SVGs as the beginning of the visual explanation.
- Add as many distinct, evidence-backed SVG views as help the recipient navigate the project; do not use a fixed diagram quota.
- Use separate views for repository shape, business capabilities, runtime, data, interfaces, workflows, state, deployment, security, delivery, observability, ownership, and change impact when relevant.
- Invent a project-specific diagram when established types do not express an important relationship.
- Provide a diagram index and visual reading order for large portfolios.
- Split dense diagrams and reject redundant or decorative images, not useful additional views.

## Audience lenses

Use the audience lens to reorder emphasis, not to hide cross-cutting facts that materially affect the scope.

| Audience | Lead with | Include next |
|---|---|---|
| Backend | Service boundaries, domain logic, data, APIs/events | Transactions, failures, tests, observability |
| Frontend/mobile | Routes/screens, state, API clients, auth, analytics | Error states, caching, feature flags, test setup |
| Data | Producers, schemas, lineage, freshness, quality | Jobs, backfills, contracts, access and retention |
| QA | User journeys, variants, boundary conditions | Fixtures, environments, automation layers, observability |
| SRE/platform | Deployment topology, dependencies, configuration | SLO signals, failure modes, recovery, capacity and rollout |
| Security | Trust boundaries, identities, permissions, secrets flow | Validation, audit, sensitive data, dependency exposure |
| Product/business | Actors, outcomes, capabilities, policies, lifecycle | Constraints, variants, manual operations, confidence labels |
| General maintainer | Purpose, vocabulary, architecture, golden path | Developer loop, safe change map, operations |

## Focused-scope rules

Start every focused analysis with:

```text
Target:
Scope type:
Location:
Included:
Excluded:
Necessary surrounding context:
Depth:
Audience and goal:
Assumptions:
```

Apply these boundaries:

- Always include the global overall architecture with the target's technical position highlighted.
- Always include the business architecture with the target's value-stream, capability, or supporting-enabler position highlighted.
- After those two global locators, show one implementation level above the target and only the neighboring components that exchange data, control, or side effects with it.
- Do not catalog unrelated features or interfaces.
- Follow a dependency outside the boundary only when it affects behavior, reliability, security, data, or change impact.
- Record out-of-scope discoveries in a short parking-lot list rather than expanding the report.
- For a directory target, verify runtime ownership through registration and callers instead of treating the folder as the architectural boundary.
- For an entity target, trace lifecycle, writers, readers, invariants, events, retention, and migrations.
- For an API, event, or job target, trace both producer/caller and consumer/side-effect boundaries.
- For a proposed change, distinguish confirmed current impact from likely impact requiring implementation review.

## Practical learning and continuity

### Reading route

For each recommended file or symbol, state:

- why to read it;
- what question it answers;
- what prerequisite concept is needed;
- whether it is authoritative, representative, generated, legacy, or test-only.

### Hands-on exercises

Offer safe exercises such as:

- locate and explain the registration of one route or event;
- follow one request through a test and implementation;
- identify where one entity is created, updated, and emitted;
- run an already documented read-only inspection or approved test;
- predict the impact of a small hypothetical change and compare it with the task-to-code map.

Do not propose production access, destructive commands, migrations, deployments, or broad environment changes as onboarding exercises.

### Understanding checks

Use two or three checks only when helpful:

- “Which component owns this state, and which components only consume it?”
- “What is the observable outcome of the golden path?”
- “Which contract or invariant would make this proposed change risky?”

### Continuation map

For long-running onboarding, retain or create on request:

- confirmed glossary;
- architecture and scope map versions;
- evidence and coverage ledger;
- explored critical paths;
- parked questions and cheapest next checks;
- next recommended scope.

Update incrementally instead of rescanning the whole repository after every follow-up.

## Completion signals

A newcomer-oriented result is complete at the selected depth when the user can answer:

1. What does this system or scope do, and for whom?
2. What is the global technical and operational shape, and how do the major parts connect?
3. What value streams and business capabilities produce the important outcomes?
4. Where does the selected scope live, and what does it depend on?
5. What are its core concepts, state, and representative flow?
6. How is it built, tested, debugged, and observed?
7. Where would a common change begin, what could it affect, and how would it be verified?
8. Which claims are confirmed, which are inferred, and what remains unexplored?
9. Which diagram should they consult for project structure, business, runtime, data, behavior, operations, and change impact?

Do not require implementation-level detail to satisfy a quick-orientation mission.
