# Project Help

A portable Agent Skill for understanding unfamiliar software projects through evidence-backed architecture, business capability, feature, interface, dependency, and implementation analysis.

[English](README.md) | [简体中文](README-zh.md)

## What this skill does

`project-help` helps Codex or Claude Code:

- Adapt onboarding by scope, depth, newcomer role, and practical goal.
- Explain a whole project or only one domain, service, module, feature, API, event, job, entity, workflow, directory, change, or incident.
- Connect purpose, vocabulary, business capabilities, runtime architecture, code, data, interfaces, tests, operations, and ownership evidence.
- Reconstruct the developer loop for configuring, building, running, testing, debugging, migrating, generating, and observing the relevant area.
- Map where a safe change would begin, what it could affect, and how to verify it.
- Produce polished, accessible SVG context, component, flow, sequence, state, lineage, and deployment diagrams.
- Separate confirmed facts from inferences, unknowns, conflicts, and uninspected areas.

## Install for Codex

Install the skill for your user account so it is available in every project:

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/gitAric/project-help.git "$HOME/.agents/skills/project-help"
```

For project-only installation, place this repository at:

```text
<repository-root>/.agents/skills/project-help
```

Codex detects newly installed skills automatically. If the skill does not appear, restart Codex. See the [official Codex Skills documentation](https://developers.openai.com/codex/skills).

## Use with Codex

Invoke it explicitly:

```text
Use $project-help to give a backend newcomer a quick orientation to this repository, including its vocabulary, system map, golden path, developer workflow, and first reading route.
```

Or ask naturally and let Codex select the skill when relevant:

```text
Explain how this project is structured, what its main business capabilities are, and how its systems interact.
```

For a focused scope:

```text
Use $project-help to build working knowledge of the checkout area only. Show its minimal system context, entrypoints, data and call flow, tests, operations, and safe-change boundary. Deliver diagrams as SVG.
```

## Install for Claude Code

Install the skill for your user account so it is available in every project:

```bash
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/gitAric/project-help.git "$HOME/.claude/skills/project-help"
```

For project-only installation, place this repository at:

```text
<repository-root>/.claude/skills/project-help
```

If Claude Code was already running before the top-level skills directory was created, restart it. See the [official Claude Code Skills documentation](https://code.claude.com/docs/en/skills).

## Use with Claude Code

Invoke it explicitly:

```text
/project-help Give a backend newcomer a quick orientation to this repository, including its vocabulary, system map, golden path, developer workflow, and first reading route.
```

Or ask naturally and let Claude select the skill when relevant:

```text
Explain how this project is structured, what its main business capabilities are, and how its systems interact.
```

For a focused scope:

```text
/project-help Build working knowledge of the checkout area only. Show its minimal system context, entrypoints, data and call flow, tests, operations, and safe-change boundary. Deliver diagrams as SVG.
```

## Human workflow

1. Define the learning mission: name the scope, desired depth, newcomer role, and practical goal. The scope can be the whole project or one domain, service, module, feature, API, event, job, entity, workflow, directory, change, or incident. If you omit a dimension, the agent will state a reasonable assumption.
2. Invoke the skill with `$project-help` in Codex or `/project-help` in Claude Code. A reusable request format is:

   ```text
   Help a <role> newcomer understand <scope> at <quick orientation / working knowledge / implementation deep dive> depth for <learn / modify / debug / operate / review>. Include <desired outputs>; keep <items> out of scope. Deliver useful diagrams as SVG.
   ```

3. Review the mission card and quick orientation first. Correct any misunderstood boundary, role, terminology, or goal before requesting more depth.
4. Review the evidence, not only the explanation. Check cited files and treat **Confirmed**, **Inferred**, **Unknown**, and **Conflict** as different confidence levels. Use the SVG diagrams as maps back to the supporting evidence.
5. Choose the next layer only when useful: ask for a golden-path trace, one focused area, developer workflow, safe-change map, incident path, interface contract, state transition, test route, or hands-on exercise.
6. Authorize runtime or state-changing actions separately. The skill starts with read-only static inspection; starting services, installing dependencies, running migrations, calling production systems, or changing project files requires explicit permission.
7. Decide whether the result should remain in the conversation or become persistent onboarding material. The agent should not add reports or diagrams to the analyzed repository unless you ask it to.

## Agent workflow

1. Load the skill instructions from `SKILL.md`, then read repository-level instructions such as `AGENTS.md` or `CLAUDE.md` and only the bundled references needed for this request.
2. Route the request by scope, depth, audience, and goal. State a compact mission card, including assumptions, exclusions, adjacent context, and any time or file budget.
3. Establish the evidence boundary: identify the repository root and revision, generated or vendored areas, authoritative documents, manifests, active registration points, schemas, tests, and evidence gaps. Inspect statically and read-only first.
4. Build the newcomer-first mental model before implementation detail: purpose, actors, observable outcomes, core vocabulary, meaningful components, one representative golden path, and the first reading or running route.
5. Trace only to the requested depth. When relevant, connect runtime wiring, business rules, data and state, interfaces, permissions, errors, retries, tests, observability, ownership evidence, and change impact. Verify that apparent modules are actively wired before describing them as current behavior.
6. Create the smallest diagram set that materially improves understanding. Produce standalone, self-contained SVG files, follow `references/diagram-patterns.md`, validate every file with `scripts/validate_svg.py`, and visually inspect it for clarity, spacing, contrast, and accurate direction.
7. Cross-check prose, diagrams, call paths, relationship directions, and coverage. Label material claims as **Confirmed**, **Inferred**, **Unknown**, or **Conflict**; never expose secrets or hide uninspected areas.
8. Deliver progressively: lead with the answer or quick orientation, append deeper evidence only as needed, state remaining unknowns and the cheapest next learning step, and stop at the requested depth. Keep output inline or temporary unless persistent files were requested.

## SVG diagram output

When a diagram materially improves understanding, the skill produces a standalone SVG artifact rather than Mermaid source. The bundled renderer provides a consistent visual system for flow and sequence diagrams, and the validator checks portability, accessibility metadata, internal references, and basic readability before delivery.
