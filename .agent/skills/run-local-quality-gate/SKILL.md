---
name: run-local-quality-gate
description: Discover and run the project's local formatting, linting, static analysis, test, and build checks before handoff.
metadata:
  version: "1.0.0"
---

# Run Local Quality Gate

Use this skill when work is ready for validation or when the user asks to run the
project's local quality checks. Discover and use the commands already defined by
the project rather than inventing a new toolchain.

## Steps

### 1. Discover the project commands

Inspect the repository for documented or configured checks, such as:

- README or contributor instructions
- package, build, task, or make files
- continuous integration configuration
- pre-commit or hook configuration
- test, lint, format, type-check, static-analysis, or build scripts

Prefer documented aggregate commands when they exist.

### 2. Decide the validation sequence

Use a sequence that gives fast feedback and avoids hiding failures. A typical
order is:

1. formatting or safe auto-fixes
2. linting or style checks
3. type checking or static analysis
4. focused tests for touched behavior
5. broader test suite
6. build, packaging, documentation, or integration checks when relevant

If a project documents a different required order, follow the project order.

### 3. Run safe auto-fixes deliberately

Only run auto-fix commands that are established in the project. After auto-fixes,
inspect the resulting changes and ensure they are related to the task.

Do not use ad hoc flags to bypass the project's configured rules in the final
validation run.

### 4. Stop on failures and fix root causes

When a step fails:

- read the failure output before rerunning
- identify whether the failure is caused by the current change or existing drift
- fix the underlying issue when it is in scope
- rerun the failing command after the fix
- avoid moving to later checks when earlier failures invalidate the result

If a failure is unrelated or cannot be fixed within scope, report it clearly with
the command and relevant output.

### 5. Run the final gate before handoff

Before handoff, run the broadest practical project-approved quality gate. If the
full gate is expensive or unavailable, run the strongest available subset and
state the limitation.

### 6. Summarize validation results

Record the commands that passed, failed, or were skipped. Include enough detail
for the next maintainer to reproduce the result.

## Output checklist

- project-defined commands were discovered before running checks
- safe auto-fixes were inspected
- failures were fixed or explicitly reported
- final validation command set is documented
- no checks were bypassed with unsupported flags in the final run
