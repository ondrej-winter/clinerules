# Tooling & CI Conventions (Python)

Use the repository's documented runner or wrapper for local quality commands. Prefer a single project entry point such as `make qa`, `uv run`, `poetry run`, `hatch run`, `tox`, or `nox` when available.

## Local Quality Gate (must pass before creating PR)
Run this workflow at the end of each coding session when code has been changed, and always before handoff.

When validating changes, use this order with the project's standard command wrappers:

1. **Format + Auto-fix**
   - Run the configured formatter/import tools

2. **Lint (no auto-fixes)**
   - Run the configured linter(s)

3. **Type check**
   - Run the configured type checker against the repository's documented paths

4. **Tests**
   - Run the focused impacted tests first, then the full required suite

5. **Optional repository gates**
   - Coverage thresholds
   - Security/static-analysis checks
   - Dependency/license audits
   - Docs build or examples smoke tests

Examples when the repository uses Ruff, Mypy, and Pytest directly:
- `ruff format .`
- `ruff check . --fix`
- `ruff check .`
- `mypy <configured paths>`
- `pytest`

## Expectations
- Generated code MUST satisfy the configured formatter/linter/type/test gates with zero unapproved failures.
- Code MUST be formatted with the repository's configured formatter.
- If you change behavior, you MUST add/adjust tests and run the relevant impacted suites.
- Do not disable lint rules unless explicitly requested; prefer refactoring.
- CI failures must be fixed at the root cause.

## Usage clarifications
- Run the full quality gate before handoff, even if only a single file changed.
- If a change impacts only a subset of tests, run that subset first,
  but still complete the full required suite before handoff.
- In monorepos, run the scoped gates required by the affected package/service plus any impacted shared gates.
- Keep local and CI entry points aligned; if CI uses a wrapper command, prefer the same wrapper locally.
- For flaky or slow tests, document the reason and mitigation in the handoff notes.
- If any step fails, address the underlying issue rather than proceeding to the next step.

## Architecture validation
- If a change crosses layers, include tests that prove boundary adherence (ports invoked, adapters wired).
- Document any intentional rule exceptions in the PR description and handoff notes.
