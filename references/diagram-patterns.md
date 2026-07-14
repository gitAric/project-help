# SVG Diagram Patterns

Create diagrams as polished, standalone SVG artifacts. Use them to reduce cognitive load and clarify relationships, not to decorate a report. Split a crowded model into several purposeful views.

## Contents

1. Diagram selection
2. Diagram-rich portfolio
3. Global overall architecture
4. Business architecture
5. Visual system
6. Composition rules
7. Semantic rules
8. Rendering workflow
9. Flow specification
10. Sequence specification
11. Direct-SVG fallback
12. Quality checklist

## Diagram selection

Build a broad set of focused views that answers the current learning goal from multiple useful angles:

| Question | Preferred diagram |
|---|---|
| What is the whole system's end-to-end technical and operational shape? | Global overall architecture |
| How does the organization create value through this product or system? | Business architecture |
| What content exists in the repository and how is it organized? | Repository/project structure map |
| Who uses the system and which external systems surround it? | System context |
| What runs, stores data, and communicates? | Component/runtime map |
| Where does a focused scope live? | Highlighted focused-scope map |
| How does value move through business capabilities? | Capability or value-flow map |
| What happens from trigger to observable outcome? | Sequence or process flow |
| How does an entity or workflow change state? | State lifecycle |
| Which entities relate, and which boundary owns them? | Entity/data model |
| Where does data originate, transform, and land? | Data lineage |
| Which APIs, events, jobs, or packages depend on one another? | Interface or dependency map |
| How do events, queues, workers, and schedules coordinate? | Event/job topology |
| How is software deployed across environments? | Deployment topology |
| Where are trust, permission, tenancy, and sensitive-data boundaries? | Security/trust-boundary map |
| How do build, test, release, debug, and observe steps connect? | Developer workflow or delivery pipeline |
| Who owns which areas, and where is the system evolving? | Ownership/evolution map |
| What will a change affect, how is it verified, and how can it roll back? | Change-impact/verification map |
| How does the system fail, recover, compensate, or require intervention? | Failure/recovery map |

For every `project-help` analysis, use a global overall architecture plus a separate business architecture as the mandatory baseline. Continue with separate diagrams for each evidence-backed perspective or critical path that teaches a distinct idea. Never collapse the global technical view and business view into one overloaded canvas.

## Diagram-rich portfolio

Prefer visual explanation throughout the report. The selection table is a starting point, not a closed catalog. There is no fixed maximum diagram count: continue while each new SVG answers a different question or makes a relationship materially easier to understand.

For whole-project takeover, seek useful views across these families:

- **Project shape**: repository/content tree, workspace/package dependencies, generated or legacy boundaries, active versus inactive areas.
- **Business**: ecosystem, stakeholder outcomes, domains, capability decomposition, value streams, policies, manual steps, core-entity lifecycles, business-to-code mapping.
- **Runtime**: system context, components, processes, deployment, environment differences, sync/async topology, external dependencies.
- **Data and contracts**: entity relationships, ownership, read/write paths, lineage, APIs, events, jobs, compatibility and consistency boundaries.
- **Behavior**: critical workflows, call sequences, decisions, state machines, alternate paths, failures, retries, compensation and recovery.
- **Delivery and operations**: configure/build/run/test/debug flow, CI/CD, observability signal flow, incident handling, rollout and rollback.
- **People and change**: ownership, architectural evolution, migration seams, task-to-code impact, regression surface and verification route.

For focused-function deep dives, keep both project-wide baselines and add separate target-level views for each relevant dimension. A typical portfolio may include target context, call sequence, state lifecycle, data ownership/lineage, interface or event dependencies, failure/retry flow, test and observability path, and change-impact map.

Create project-specific diagram types when needed. A plugin graph, rules-decision tree, feature-flag matrix, cache-coherency view, tenancy map, migration timeline, or any other evidence-backed visual is valid even when it is absent from this guide.

More diagrams must not mean denser diagrams. Keep one teaching purpose per SVG, split crowded phases or boundaries, and avoid duplicate views that merely restyle the same relationships. When the portfolio is large, provide a numbered diagram index and recommended visual reading order.

## Global overall architecture

Answer: “What are the major parts of the entire system, where do they run or store state, and how do they connect?” Build this view from the outside in:

1. Actors and access channels
2. Product, system, trust, and environment boundaries
3. Major first-party applications, services, workers, and shared platform capabilities
4. Authoritative data stores, caches, event infrastructure, and externally owned state
5. External systems and the main synchronous, asynchronous, batch, and data relationships
6. Deployment or runtime grouping when it changes how the system is understood or operated

Keep the view global. Group lower-level modules inside five to nine meaningful nodes instead of drawing every repository package. Show direction and label protocols or events when known. Identify owned data and external dependencies visually. Verify active registration or deployment wiring before calling a component current.

Recommended composition: actors and channels on the left, owned system boundaries in the center, data near its owner, and external systems on the right. Put shared platform or asynchronous infrastructure in a lower lane. Use nested group boxes for product, domain, runtime, environment, or trust boundaries, but avoid more than two visible nesting levels.

For focused analysis, keep this as a whole-project view and highlight every node or boundary owned by the selected scope with the focus treatment. Mute unrelated internals, retain the upstream, downstream, data, and external relationships needed to establish position, and state the path from project boundary to target in prose below the SVG.

## Business architecture

Answer: “For whom does the business create which outcomes, through which capabilities and value flow?” Keep this view understandable without reading the source tree:

1. Primary actors, customers, operators, and stakeholders
2. Desired actor and business outcomes
3. End-to-end value streams or major business journeys
4. Business domains and capabilities that enable each value stage
5. Core business entities and lifecycle handoffs
6. Policies, approvals, risk controls, manual work, and external business parties when material
7. A lightweight capability-to-system bridge in prose or a table, rather than replacing capabilities with services

Use business language in node titles. Repository folders, controllers, databases, and service names belong in the global/component view unless they are also recognized business concepts. Arrange the main value stream left-to-right, place cross-cutting capabilities in a supporting lane, and use entity names in subtitles when they clarify what moves between stages.

Do not infer business intent from naming alone. Product documents, specifications, tests, user-visible behavior, schemas, and domain-owner evidence may support the model; label code-only interpretations as inferred.

For focused analysis, highlight the business capability or value-stream stage implemented by the target. If the target is technical infrastructure, show it in a supporting-enabler lane connected to the capabilities it serves. Do not force a direct customer outcome when evidence supports only an enabling role.

## Visual system

Use a restrained light theme with strong hierarchy:

| Role | Treatment |
|---|---|
| Canvas | Cool off-white `#F7F9FC` |
| Primary system | Blue tint and blue border |
| Focused scope | Warm orange tint, thicker border, subtle shadow |
| Data/store | Green tint |
| External actor/system | Violet tint |
| Neighboring context | White or neutral gray |
| Risk/failure | Red only when the risk itself is the subject |
| Confirmed edge | Solid slate line |
| Inferred edge | Dashed muted line and explicit label |

Use system fonts such as Inter, `ui-sans-serif`, or `system-ui`. Keep titles about 28–32 px, node titles 16–19 px, body labels 13–16 px, and never use text below 12 px. Maintain WCAG-friendly contrast.

Use one accent color for focus. Do not assign arbitrary colors to every service. Color must communicate role, scope, or evidence status.

## Composition rules

- Use a descriptive title that states the diagram's teaching purpose.
- Use a short subtitle to explain the boundary or highlighted scope.
- Keep five to nine primary nodes in one view. Group related internals inside a labeled boundary.
- Arrange the dominant flow left-to-right or top-to-bottom and keep it consistent.
- Place edges behind nodes. Prefer orthogonal routes and avoid crossings.
- Leave at least one label-width of space between connected nodes.
- Keep labels short. Move detailed evidence, exceptions, and payload fields into prose or tables.
- Align nodes to an 8 px grid with consistent sizes, padding, corner radii, and gaps.
- Use whitespace to show boundaries and reading order; avoid large unexplained empty areas.
- Highlight every node owned by a focused scope and mute surrounding context without making it unreadable.
- Add a small legend only when styling carries meaning that is not obvious.
- Split context, runtime, sequence, state, and deployment concerns instead of combining them into one oversized canvas.

## Semantic rules

- Draw an edge only when active wiring, a contract, a schema, a test, or authoritative documentation supports it.
- Use arrow direction from trigger/producer/provider toward handler/consumer/side effect, and state the reference boundary in accompanying prose.
- Label protocol, operation, topic, event, command, or data when known.
- Use solid edges for confirmed relationships and dashed edges only for useful, labeled inferences.
- Distinguish synchronous calls, asynchronous publication, data access, and human/manual action when that distinction matters.
- Mark owned state separately from cached, replicated, or externally owned data.
- For lifecycle diagrams, show only states and transitions confirmed by code, schema, or authoritative documents. Explain guards and irreversible transitions outside the graphic.
- Put evidence citations directly below the SVG instead of inside nodes.

## Rendering workflow

Prefer the bundled renderer for consistent flow and sequence diagrams. It uses only the Python standard library.

```bash
python3 <skill-dir>/scripts/render_svg.py <diagram-spec.json> --output <diagram.svg>
python3 <skill-dir>/scripts/validate_svg.py --strict <diagram.svg>
```

In Claude Code, use `${CLAUDE_SKILL_DIR}` for `<skill-dir>`.

The renderer supports two diagram types:

- `flow`: context, component, capability, state, lineage, and deployment views with explicit node geometry.
- `sequence`: participants are spaced automatically and messages are rendered in order.

Render an example to inspect the theme:

```bash
python3 <skill-dir>/scripts/render_svg.py --example flow --output /tmp/project-help-flow.svg
python3 <skill-dir>/scripts/render_svg.py --example sequence --output /tmp/project-help-sequence.svg
python3 <skill-dir>/scripts/render_svg.py --example overall-architecture --output /tmp/project-help-overall-architecture.svg
python3 <skill-dir>/scripts/render_svg.py --example business-architecture --output /tmp/project-help-business-architecture.svg
```

The two architecture examples deliberately highlight the same `Checkout` focus: once in the technical whole-system view and once in the business capability/value-stream view.

Use a safe temporary or artifact directory unless the user explicitly requests repository files.
Use `--display-scale 0.5` when a compact default display size is helpful; the full `viewBox` and vector quality are preserved.

## Flow specification

Create a JSON specification like:

```json
{
  "type": "flow",
  "title": "Checkout in system context",
  "subtitle": "Focused scope highlighted; surrounding context muted",
  "width": 1440,
  "height": 900,
  "groups": [
    {"id": "commerce", "label": "Commerce domain", "x": 300, "y": 150, "width": 800, "height": 600}
  ],
  "nodes": [
    {"id": "user", "label": "Customer", "kind": "actor", "tone": "external", "x": 60, "y": 350, "width": 190, "height": 118},
    {"id": "checkout", "label": "Checkout", "subtitle": "Selected scope", "kind": "feature", "tone": "focus", "focus": true, "x": 430, "y": 340, "width": 220, "height": 132},
    {"id": "orders", "label": "Order store", "kind": "data", "tone": "data", "x": 820, "y": 350, "width": 190, "height": 118}
  ],
  "edges": [
    {"from": "user", "to": "checkout", "label": "Submit order", "style": "emphasis"},
    {"from": "checkout", "to": "orders", "label": "Persist", "style": "confirmed"}
  ]
}
```

Node tones: `primary`, `focus`, `data`, `external`, `neutral`, and `risk`. Edge styles: `confirmed`, `inferred`, `emphasis`, and `risk`.

The renderer chooses anchors and orthogonal paths automatically. Override with `from_side` and `to_side` (`left`, `right`, `top`, `bottom`) or provide explicit `points` when avoiding a crossing.

## Sequence specification

Create a JSON specification like:

```json
{
  "type": "sequence",
  "title": "Golden path: submit an order",
  "subtitle": "Trigger to durable and observable outcomes",
  "participants": [
    {"id": "caller", "label": "Customer", "tone": "external"},
    {"id": "api", "label": "Order API", "tone": "primary"},
    {"id": "domain", "label": "Order domain", "tone": "focus"},
    {"id": "store", "label": "Order store", "tone": "data"}
  ],
  "messages": [
    {"from": "caller", "to": "api", "label": "Submit order", "style": "emphasis"},
    {"from": "api", "to": "domain", "label": "Validate and create"},
    {"from": "domain", "to": "store", "label": "Persist state"},
    {"from": "store", "to": "domain", "label": "Commit result", "style": "response"}
  ]
}
```

Keep sequence diagrams to eight or fewer participants. Split by phase when the interaction becomes wider or longer than a newcomer can scan easily.

## Direct-SVG fallback

Author SVG directly when the helper cannot express the required layout. Keep it self-contained and portable:

- Set `xmlns`, `viewBox`, `width`, `height`, `role="img"`, and `aria-labelledby` on the root.
- Include `<title>` and `<desc>`.
- Embed CSS in `<style>` and arrowheads, gradients, or shadows in `<defs>`.
- Use only vector primitives and text. Avoid external images, scripts, `foreignObject`, remote fonts, and external stylesheets.
- Wrap long labels with `<tspan>` and preserve minimum font sizes.
- Reuse the visual tokens and semantic conventions in this guide.
- Run `validate_svg.py` after every revision.

## Quality checklist

Before delivery, confirm:

- The title, scope, reading direction, and main takeaway are apparent within a few seconds.
- No nodes, labels, arrows, or shadows are clipped.
- No labels overlap edges or nodes, and no important edge crosses another edge.
- Focus styling is visible but restrained; context remains legible.
- Solid and dashed edges match the evidence ledger.
- Text is readable at normal display size and contrast is sufficient.
- The SVG opens without network access and contains no external dependencies.
- `validate_svg.py --strict` passes.
- A rendered visual inspection has been performed when the environment supports it.
- Diagram names, directions, and claims match the report and evidence below it.
