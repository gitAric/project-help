# Diagram Patterns

Use these patterns as starting points. Replace placeholders with project terminology and omit diagrams that do not add explanatory value.

## Contents

1. Diagram rules
2. System context
3. Focused component map
4. Business capability map
5. Feature sequence
6. State lifecycle

## Diagram rules

- Quote Mermaid labels that contain spaces, punctuation, or parentheses.
- Use stable domain names consistently across diagrams and report tables.
- Show direction on every integration and label the protocol, operation, topic, or data when known.
- Keep infrastructure and business components visually distinct.
- Use solid edges for confirmed relationships. Use dashed edges only for useful, explicitly labeled inferences.
- Put evidence citations in prose immediately below a diagram; do not crowd source paths into nodes.
- Add a legend when using focus or inferred styling.
- Validate that Mermaid parses before delivery when a renderer is available.

## System context

```mermaid
flowchart LR
    actor["Primary actor"]
    upstream["Upstream system"]
    system["Project system"]
    downstream["Downstream system"]

    actor -->|"business action"| system
    upstream -->|"trigger / input"| system
    system -->|"command / event / data"| downstream

    classDef actor fill:#E8F0FE,stroke:#2563EB,color:#172554
    classDef system fill:#ECFDF5,stroke:#059669,color:#064E3B
    classDef external fill:#F8FAFC,stroke:#64748B,color:#0F172A
    class actor actor
    class system system
    class upstream,downstream external
```

Below the diagram, list the evidence for each edge and mark any inferred direction.

## Focused component map

Use this pattern whenever the user requests one feature or module. The orange nodes show exactly where the requested feature lives in the wider system.

```mermaid
flowchart LR
    user["User / caller"]

    subgraph product["Product system"]
        gateway["Gateway / UI"]
        neighbor["Neighboring capability"]

        subgraph domain["Owning business domain"]
            entry["Feature entrypoint"]
            logic["Feature application/domain logic"]
            data[("Feature data")]
        end
    end

    external["External downstream"]

    user --> gateway
    gateway -->|"operation"| entry
    entry --> logic
    logic --> data
    logic -->|"side effect"| external
    neighbor -.->|"inferred or optional"| logic

    classDef focus fill:#FFF3E0,stroke:#E65100,stroke-width:3px,color:#7F2D00
    classDef context fill:#F8FAFC,stroke:#94A3B8,color:#334155
    classDef external fill:#EEF2FF,stroke:#6366F1,color:#312E81
    class entry,logic,data focus
    class gateway,neighbor context
    class user,external external
```

Add a location statement after the diagram:

`Product system > Owning domain > Service/package > Feature module > Entrypoint`

## Business capability map

```mermaid
flowchart TB
    outcome["Business outcome"]

    subgraph capabilities["Business capabilities"]
        intake["Intake"]
        decision["Decision / policy"]
        fulfillment["Fulfillment"]
        support["Support / reconciliation"]
    end

    outcome --> intake
    intake --> decision
    decision --> fulfillment
    fulfillment --> support
```

Map each capability to implementing components in a table below the diagram. Do not derive capability boundaries solely from folders.

## Feature sequence

```mermaid
sequenceDiagram
    autonumber
    actor Caller
    participant Entry as "UI / API / Event adapter"
    participant App as "Application service"
    participant Domain as "Domain logic"
    participant Store as "Data store"
    participant Downstream as "Downstream system"

    Caller->>Entry: Trigger with input
    Entry->>Entry: Authenticate and validate
    Entry->>App: Normalized command
    App->>Domain: Apply business rule
    Domain->>Store: Read or persist state
    Store-->>Domain: Result
    alt External side effect required
        App->>Downstream: Command / event
        Downstream-->>App: Result / acknowledgement
    else No external side effect
        App->>App: Complete locally
    end
    App-->>Entry: Outcome or domain error
    Entry-->>Caller: Response / acknowledgement
```

Replace generic steps with verified behavior. Include timeout, retry, transaction, or async boundaries only when supported by evidence.

## State lifecycle

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted: submit
    Submitted --> Approved: approve
    Submitted --> Rejected: reject
    Approved --> Completed: fulfill
    Rejected --> Draft: revise
    Completed --> [*]
```

Use a state diagram only when state and transitions are explicit in code, schemas, or authoritative documentation. Note guards, side effects, and irreversible transitions in prose.
