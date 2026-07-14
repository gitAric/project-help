# Project Help

A portable Agent Skill for comprehensively receiving and taking over unfamiliar software projects through evidence-backed project-content, business, architecture, runtime, code, operations, and implementation analysis.

[English](README.md) | [简体中文](README-zh.md)

## What this skill does

`project-help` helps Codex or Claude Code:

- Perform a complete project-takeover analysis by default, accounting for project contents, business model, architecture, runtime, data, interfaces, workflows, development, operations, ownership, risks, and safe-change routes.
- Deeply analyze only one named domain, service, module, feature, API, event, job, entity, workflow, directory, change, or incident when the user provides a focused target.
- Always draw a global overall architecture SVG showing actors and channels, system boundaries, major runtimes, platform services, owned data, external systems, and principal relationships.
- Always draw a separate business architecture SVG showing actor outcomes, value streams, domains and capabilities, core entities, policies, approvals, and manual work.
- Highlight a focused target's technical position in the global architecture and its capability, value-stream, or supporting-enabler position in the business architecture.
- Connect purpose, vocabulary, business capabilities, runtime architecture, code, data, interfaces, tests, operations, and ownership evidence.
- Reconstruct the developer loop for configuring, building, running, testing, debugging, migrating, generating, and observing the relevant area.
- Map where a safe change would begin, what it could affect, and how to verify it.
- Produce a diagram-rich SVG report with no fixed maximum: add repository, context, capability, runtime, deployment, dependency, event, data, sequence, state, security, developer-workflow, ownership, and change-impact views, plus any project-specific diagram that improves understanding.
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
Use $project-help to perform a complete project-takeover analysis for a backend engineer. Cover project contents, business, global and runtime architecture, data, interfaces, critical workflows, developer workflow, operations, ownership, risks, and safe-change routes. Produce separate global overall architecture and business architecture SVGs, then add as many distinct, useful SVG views as the evidence supports; do not limit the diagrams to a predefined list.
```

Or ask naturally and let Codex select the skill when relevant:

```text
Explain how this project is structured, what its main business capabilities are, and how its systems interact.
```

For a focused scope:

```text
Use $project-help to deeply analyze the checkout function only. Still produce the global overall architecture and business architecture SVGs, highlighting checkout's position in both, then add detailed SVG views for its calls, state, data, dependencies, failures, tests, operations, and change impact wherever supported.
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
/project-help Perform a complete project-takeover analysis for a backend engineer. Cover project contents, business, global and runtime architecture, data, interfaces, critical workflows, developer workflow, operations, ownership, risks, and safe-change routes. Produce separate global overall architecture and business architecture SVGs, then add as many distinct, useful SVG views as the evidence supports; do not limit the diagrams to a predefined list.
```

Or ask naturally and let Claude select the skill when relevant:

```text
Explain how this project is structured, what its main business capabilities are, and how its systems interact.
```

For a focused scope:

```text
/project-help Deeply analyze the checkout function only. Still produce the global overall architecture and business architecture SVGs, highlighting checkout's position in both, then add detailed SVG views for its calls, state, data, dependencies, failures, tests, operations, and change impact wherever supported.
```

## Human workflow

1. Define the takeover mission: omit the scope for a complete project analysis, or name one function for a focused deep dive. You can also state the recipient's role and practical goal. If omitted, the agent assumes whole-project working knowledge for a general maintainer.
2. Invoke the skill with `$project-help` in Codex or `/project-help` in Claude Code. A reusable request format is:

   ```text
   Help a <role> engineer take over <the whole project / one named function> for <learn / modify / debug / operate / review>. For a named function, analyze only that function in detail. Always produce global overall and business architecture SVGs, highlight the function's position in both, and add as many other distinct SVG views as improve understanding without limiting them to a predefined list.
   ```

3. Review the mission card and takeover snapshot first. Correct any misunderstood boundary, role, terminology, or goal before the deeper report continues.
4. Review the evidence, not only the explanation. Check cited files and treat **Confirmed**, **Inferred**, **Unknown**, and **Conflict** as different confidence levels. Use the SVG diagrams as maps back to the supporting evidence.
5. Treat the two baseline SVGs as the beginning of the visual report. Expect additional diagrams for every useful project or function dimension, and use the diagram index to review them in order. For focused work, verify that the selected function is highlighted consistently across all relevant views.
6. Authorize runtime or state-changing actions separately. The skill starts with read-only static inspection; starting services, installing dependencies, running migrations, calling production systems, or changing project files requires explicit permission.
7. Decide whether the result should remain in the conversation or become persistent onboarding material. The agent should not add reports or diagrams to the analyzed repository unless you ask it to.

## Agent workflow

1. Load the skill instructions from `SKILL.md`, then read repository-level instructions such as `AGENTS.md` or `CLAUDE.md` and only the bundled references needed for this request.
2. Route the request as whole-project takeover or focused-function deep dive, then state scope, depth, audience, goal, assumptions, exclusions, and revision in a compact mission card.
3. Establish the evidence boundary. For whole-project takeover, account for every first-party top-level area and major capability; for focused work, inspect enough project breadth to place the target correctly, then keep unrelated implementation detail out of scope.
4. Reconstruct two separate baseline models for every request: the global technical/operational architecture and the business value/capability architecture. In focused mode, highlight the target consistently in both and state its technical and business locations.
5. Continue by mode. Whole-project takeover covers project contents, business, runtime, data, interfaces, critical paths, developer workflow, operations, ownership, risks, and change readiness. Focused mode traces only the named function through entrypoints, runtime wiring, business rules, data and state, interfaces, permissions, errors, retries, tests, observability, and change impact.
6. Build a broad, open-ended SVG portfolio rather than stopping at the named examples. Create a separate diagram whenever it adds a distinct relationship, sequence, lifecycle, boundary, mapping, or impact; split dense diagrams, then validate and visually inspect every file.
7. Cross-check prose, diagrams, call paths, relationship directions, and coverage. Label material claims as **Confirmed**, **Inferred**, **Unknown**, or **Conflict**; never expose secrets or hide uninspected areas.
8. Deliver progressively: mission and snapshot, mandatory baselines, a diagram index and visual reading route, then the diagram-backed whole-project coverage or focused detail. State remaining unknowns and coverage limits. Keep output inline or temporary unless persistent files were requested.

## SVG diagram output

Every analysis starts with two distinct baseline SVG artifacts: a global overall architecture diagram and a business architecture diagram. It then produces as many additional, non-redundant SVGs as the evidence supports. The catalog is deliberately open-ended: repository structure, runtime, deployment, dependencies, events, data models, lineage, sequences, decisions, state, security, developer workflow, observability, ownership, evolution, risk, and change impact are examples rather than limits. Each SVG should answer one clear question; large portfolios include a diagram index and reading order.
