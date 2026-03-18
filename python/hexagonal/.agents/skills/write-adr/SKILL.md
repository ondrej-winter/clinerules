# Skill: Write an Architecture Decision Record (ADR)

Use this skill when the user asks to document an architectural decision, record a
design choice, or create an ADR.

---

## Prerequisites

- An `docs/adr/` directory exists in the project (create it if not).
- ADRs are numbered sequentially: `0001`, `0002`, …

---

## Steps

### 1 — Determine the next ADR number

```bash
ls docs/adr/ | grep -E '^[0-9]{4}' | sort | tail -1
```

Increment by one to get the next number (e.g. if `0003-…` is last, use `0004`).

### 2 — Create the ADR file

File name format: `docs/adr/<NNNN>-<short-title-kebab-case>.md`

Example: `docs/adr/0004-use-sqlalchemy-for-persistence.md`

### 3 — Fill in the template

```markdown
# <NNNN>. <Short Title in Title Case>

Date: <YYYY-MM-DD>
Status: Proposed | Accepted | Deprecated | Superseded by [<NNNN>](…)

## Context

Describe the situation, forces, and constraints that make this decision
necessary. What problem are we solving? What are the trade-offs?

## Decision

State the decision clearly and concisely in one or two sentences.
Use active voice: "We will use X because Y."

## Consequences

### Positive
- …

### Negative / trade-offs
- …

### Neutral
- …

## Alternatives considered

| Option | Reason rejected |
|--------|----------------|
| … | … |
```

### 4 — Set the status

| Status | When to use |
|---|---|
| `Proposed` | Decision is under discussion. |
| `Accepted` | Decision is agreed and in effect. |
| `Deprecated` | Decision was once accepted but is no longer followed. |
| `Superseded by [NNNN](…)` | A newer ADR replaces this one. |

Default to `Accepted` unless the user explicitly says it is still being discussed.

### 5 — Update the ADR index (if one exists)

If `docs/adr/README.md` or `docs/adr/index.md` exists, append a row to the
decision log table:

```markdown
| [<NNNN>](./<NNNN>-<slug>.md) | <Short Title> | <Date> | Accepted |
```

---

## Good ADR practices

- Focus on **why**, not **what** — the code already shows what was built.
- Keep context factual; avoid post-hoc rationalisation.
- One decision per ADR; split if the scope creeps.
- Link to related ADRs, issues, or PRs for traceability.
- Never delete an ADR — deprecate or supersede it instead.
