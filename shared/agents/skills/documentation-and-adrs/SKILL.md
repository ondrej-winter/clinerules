---
name: documentation-and-adrs
description: Create or update durable documentation, architecture decision records, API notes, runbooks, changelogs, and agent-facing context that explain decisions, usage, trade-offs, and validation evidence.
metadata:
  version: "1.1.0"
---

# Documentation and ADRs

Use this skill when a decision, behavior, interface, workflow, or operational
procedure needs durable context for future maintainers, users, or agents. The
goal is to document why something exists, how to use it safely, and what evidence
supports it.

Good documentation explains intent, constraints, trade-offs, and consequences.
It does not restate obvious code or create stale process noise.

## When to use this skill

Use this skill when:

- making an architectural, product, data, security, or workflow decision
- changing public or compatibility-sensitive interfaces
- shipping behavior that users, operators, or maintainers need to understand
- recording migration, deployment, rollback, or troubleshooting guidance
- updating project commands, setup, conventions, or agent instructions
- repeatedly explaining the same design or gotcha

Do not use this skill for throwaway prototypes, obvious comments, or documentation
that has no likely reader or maintenance owner.

## Steps

### 1. Identify the reader and purpose

Before writing, state:

- who needs the documentation
- what task or decision it supports
- what the reader already knows
- what can go wrong without the documentation
- where the documentation should live

Choose the smallest durable format that fits the need.

### 2. Choose the documentation type

Common types include:

- README or quick-start guide for project setup and common commands
- architecture decision record for significant decisions and trade-offs
- interface documentation for public APIs, commands, events, schemas, or modules
- runbook for operational procedures and incident recovery
- migration guide for moving from one behavior to another
- changelog or release note for shipped user-visible changes
- agent-facing rules or context for project conventions and constraints

### 3. Write ADRs for durable decisions

Use an ADR when a decision would be expensive to reverse or repeatedly debated.

Portable ADR shape:

```md
# ADR-<number>: <decision title>

## Status

<proposed | accepted | superseded | deprecated>

## Context

<constraints, forces, requirements, and problem statement>

## Decision

<chosen approach>

## Alternatives considered

- <alternative>: <why it was not chosen>

## Consequences

- <benefit, cost, risk, follow-up, or validation implication>
```

Do not delete old ADRs. If a decision changes, write a new ADR that supersedes or
deprecates the old one.

### 4. Document interfaces by contract

For public or cross-boundary interfaces, document:

- purpose and supported use cases
- inputs, outputs, side effects, and error behavior
- compatibility expectations
- examples that are minimal and portable
- validation, authentication, authorization, or operational constraints when
  relevant

Use the project’s preferred contract format, such as schema files, reference docs,
types, command help, examples, or generated documentation.

### 5. Comment intent, not obvious mechanics

Inline comments should explain non-obvious intent, constraints, or hazards.

Good comments answer:

- why this approach is necessary
- what invariant must be preserved
- what external constraint shaped the code
- what future maintainer should not simplify away

Avoid comments that restate syntax, preserve deleted code, or create TODOs with no
owner or timeframe.

### 6. Keep setup and workflow docs executable

For README, setup, or workflow docs, include:

- prerequisites
- installation or bootstrap steps
- common commands using placeholders when the skill is reusable, such as
  `<test_command>` or `<build_command>`
- validation expectations
- troubleshooting notes for common failures
- links to deeper docs when needed

Verify commands when possible, or clearly state when examples are illustrative.

### 7. Update docs with the change

Documentation should change with the behavior it describes.

Check whether the change affects:

- README or quick-start instructions
- ADRs or architecture overview
- public interface docs
- migration or deprecation notes
- changelog or release notes
- runbooks, alerts, dashboards, or troubleshooting guides
- agent rules, conventions, or repository navigation docs

### 8. Validate and prune

Before handoff:

- remove commented-out code and obsolete docs
- check links and referenced file names when practical
- confirm examples match current behavior
- keep docs concise enough to be maintained
- record validation evidence or skipped validation

## Red flags

- significant decision has no rationale
- docs explain what code already says but omit why
- public interface lacks contract, examples, or compatibility notes
- setup docs contain unverified commands or stale prerequisites
- TODO comments have no owner or follow-up path
- old decisions are deleted instead of superseded
- docs are updated separately from the behavior they describe

## Output checklist

- reader and purpose are explicit
- documentation type fits the need
- decisions capture context, alternatives, and consequences
- interface docs describe contract and compatibility
- inline comments explain intent rather than obvious mechanics
- setup or workflow commands are verified or marked as examples
- stale docs and commented-out code are removed
- validation evidence is documented before handoff
