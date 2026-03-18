# Skill: Write an Architecture Decision Record (ADR)

Use this skill when the user asks to document an architectural decision,
capture a design choice, or create an ADR.

## Goal

Create a new ADR in `docs/adr/` with the next sequential number, a clear title,
and a concise explanation of the decision and its consequences.

## Steps

### 1. Ensure the ADR directory exists

Use `docs/adr/`. Create it if it does not already exist.

### 2. Determine the next ADR number

Inspect the existing files in `docs/adr/`, find the highest four-digit prefix,
and increment it by one.

- If no ADRs exist yet, start with `0001`.
- Example: if `0003-...` is the latest ADR, use `0004`.

### 3. Create the ADR file

Use this file name format:

`docs/adr/<NNNN>-<short-title-kebab-case>.md`

Example:

`docs/adr/0004-standardize-api-error-format.md`

### 4. Fill in the ADR template

```markdown
# <NNNN>. <Short Title in Title Case>

Date: <YYYY-MM-DD>
Status: Proposed | Accepted | Deprecated | Superseded by [<NNNN>](./<NNNN>-<slug>.md)

## Context

Describe the situation, constraints, and trade-offs that make this decision
necessary.

## Decision

State the decision clearly in one or two sentences.
Prefer active voice, for example: "We will use X because Y."

## Consequences

### Positive

- ...

### Negative / trade-offs

- ...

### Neutral

- ...

## Alternatives considered

| Option | Reason rejected |
| ------ | --------------- |
| ...    | ...             |
```

### 5. Set the status

Use the status that matches the user's intent:

| Status                                     | Use when                                                  |
| ------------------------------------------ | --------------------------------------------------------- |
| `Proposed`                                 | The decision is still under discussion.                   |
| `Accepted`                                 | The decision has been agreed and is in effect.            |
| `Deprecated`                               | The decision was once accepted but is no longer followed. |
| `Superseded by [NNNN](./<NNNN>-<slug>.md)` | A newer ADR replaces this one.                            |

If the user does not specify a status, default to `Accepted` for a documented
current decision.

### 6. Update the ADR index if one exists

If `docs/adr/README.md` or `docs/adr/index.md` exists, append an entry such as:

```markdown
| [<NNNN>](./<NNNN>-<slug>.md) | <Short Title> | <Date> | <Status> |
```

## Good ADR practices

- Focus on why, not implementation detail.
- Keep the context factual and specific.
- Record one decision per ADR.
- Link related ADRs, issues, or PRs when helpful.
- Do not delete old ADRs; deprecate or supersede them.
