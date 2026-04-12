---
name: write-adr
description: Create an Architecture Decision Record with the next sequential number, a clear title, and documented consequences.
---

# Write an Architecture Decision Record (ADR)

Use this skill when the user asks to document an architectural decision,
capture a design choice, or create an ADR.

## Goal

Create a new ADR in the ADR directory with the next sequential number, a clear
title, and a concise record of the decision and its consequences.

## Steps

### 1. Locate the ADR directory

Use the repository's ADR directory. If none exists, use `<adr_directory>` and
create it.

### 2. Determine the next ADR number

Inspect the files in the ADR directory, find the highest four-digit prefix, and
increment it by one.

- If no ADRs exist yet, start with `0001`.
- Example: if `0003-...` is the latest ADR, use `0004`.

### 3. Create the ADR file

Use this file name format:

`<adr_directory>/<NNNN>-<short-title-kebab-case>.md`

Example:

`<adr_directory>/0004-standardize-api-error-format.md`

### 4. Fill in the ADR template

Use today's date for the Date field.

```markdown
# <NNNN>. <Short Title in Title Case>

Date: <YYYY-MM-DD>
Status: Proposed | Accepted | Deprecated | Superseded by [NNNN](./<NNNN>-<slug>.md)

## Context

Describe the situation, constraints, and trade-offs that make this decision
necessary.

## Decision

State the decision clearly in one or two sentences. Prefer active voice, for
example: "We will use X because Y."

## Consequences

List the consequences. Use subsections such as Positive, Negative, and Neutral
when helpful. For simple decisions, a flat list is fine.

- ...

## Alternatives considered

Include this section when meaningful alternatives were evaluated. Omit it when
the decision follows an obvious convention with no real alternatives.

| Option | Reason rejected |
| ------ | --------------- |
| ...    | ...             |
```

### 5. Set the status

Choose the status that matches the user's intent:

| Status                                     | Use when                                                  |
| ------------------------------------------ | --------------------------------------------------------- |
| `Proposed`                                 | The decision is still under discussion.                   |
| `Accepted`                                 | The decision has been agreed and is in effect.            |
| `Deprecated`                               | The decision was once accepted but is no longer followed. |
| `Superseded by [NNNN](./<NNNN>-<slug>.md)` | A newer ADR replaces it.                                  |

If the user does not specify a status, default to `Accepted`.

### 6. Update the ADR index if one exists

If an ADR index file such as `README.md` or `index.md` exists in the ADR
directory and already contains a table, append an entry such as:

```markdown
| [<NNNN>](./<NNNN>-<slug>.md) | <Short Title> | <Date> | <Status> |
```

If no ADR index file exists, create one with a header such as:

```markdown
# Architecture Decision Records

| ADR                          | Title         | Date   | Status   |
| ---------------------------- | ------------- | ------ | -------- |
| [<NNNN>](./<NNNN>-<slug>.md) | <Short Title> | <Date> | <Status> |
```

## Good ADR practices

- Focus on why, not implementation details.
- Keep the context factual and specific.
- Record one decision per ADR.
- Link related ADRs, issues, or PRs when helpful.
- Do not delete old ADRs; deprecate or supersede them.
