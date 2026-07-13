# SVG Diagram Patterns

Create diagrams as polished, standalone SVG artifacts. Use them to reduce cognitive load and clarify relationships, not to decorate a report. Split a crowded model into several purposeful views.

## Contents

1. Diagram selection
2. Visual system
3. Composition rules
4. Semantic rules
5. Rendering workflow
6. Flow specification
7. Sequence specification
8. Direct-SVG fallback
9. Quality checklist

## Diagram selection

Choose the smallest set that answers the current learning goal:

| Question | Preferred diagram |
|---|---|
| Who uses the system and which external systems surround it? | System context |
| What runs, stores data, and communicates? | Component/runtime map |
| Where does a focused scope live? | Highlighted focused-scope map |
| How does value move through business capabilities? | Capability or value-flow map |
| What happens from trigger to observable outcome? | Sequence or process flow |
| How does an entity or workflow change state? | State lifecycle |
| Where does data originate, transform, and land? | Data lineage |
| How is software deployed across environments? | Deployment topology |

Use a system context plus one representative golden path for quick onboarding. Add more diagrams only when they teach a distinct idea.

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
```

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
