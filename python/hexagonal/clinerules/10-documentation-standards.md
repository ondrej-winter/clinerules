# Documentation standards: clear, concise, useful

Use these rules to keep documentation helpful without being verbose.

This file governs documentation written inside source code. Requirements for README updates, ADRs, and changelog notes live in `04-docs-and-adr.md`.

## Documentation principles
- Prefer concise explanations of contracts, invariants, side effects, and intent.
- Docstrings should add information that names and type hints do not already make obvious.
- Choose one docstring style for the repository (Google, NumPy, or reStructuredText) and use it consistently.
- Public APIs and non-obvious behavior deserve better documentation than trivial private helpers.

## Module docstrings
- Use a short summary for public modules or modules with non-obvious responsibilities.
- Add a short paragraph only when callers need context, invariants, or usage constraints.
- Keep module docstrings free of change logs, feature lists, and ADR-style rationale.

## Class docstrings
- Describe the class responsibility and key invariants/lifecycle expectations when they are not obvious.
- Keep implementation details out unless consumers must know them.
- Small private data holders may omit docstrings when names and types are already sufficient.

## Function and method docstrings
- Document public callables and any private callable with non-obvious behavior, side effects, concurrency rules, or tricky contracts.
- Start with a short summary sentence.
- Document **Args**, **Returns**, **Raises**, **Yields**, or **Examples** only when they add real value for callers.
- Call out side effects, blocking/async behavior, idempotency, and important invariants when relevant.
- Avoid duplicating type hints in prose unless clarification is needed.

## Inline comments
- Use sparingly for non-obvious logic only.
- Explain **why**, not **what**.
- Prefer self-documenting code (clear names, simple logic) over explanatory noise.
- Tag temporary workarounds with an issue/reference when possible.

## What NOT to document in code
- ❌ Feature lists → belongs in README
- ❌ Architecture patterns → belongs in ADRs
- ❌ Performance claims → belongs in benchmarks/docs
- ❌ Marketing language ("rich", "powerful", "advanced")
- ❌ Redundant restatements of type hints or parameter names
