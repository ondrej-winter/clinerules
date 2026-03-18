# Skill: Run Quality Checks

Use this skill when the user asks to run quality checks, linting, type-checking,
or tests on a Python hexagonal project managed with `uv`.

---

## Steps

### 1 — Lint and auto-fix with ruff

```bash
uv run ruff check . --fix
uv run ruff format .
```

If `--fix` introduces changes, stage them so the user can review.

### 2 — Type-check with mypy

```bash
uv run mypy .
```

- Interpret each error: show the file, line, and a plain-English explanation.
- Do **not** suppress errors with `# type: ignore` without first attempting a
  proper fix.
- Common patterns to fix:
  - Missing return type → add annotation.
  - `None` not handled → add `Optional[…]` or an explicit guard.
  - Untyped third-party library → add a `py.typed` stub or add to
    `[[tool.mypy.overrides]]` with `ignore_missing_imports = true`.

### 3 — Run tests with coverage

```bash
uv run pytest --cov --cov-report=term-missing
```

- If any test fails, stop and report the failure to the user before continuing.
- If coverage drops below the project threshold, flag it prominently.

### 4 — Report summary

After all three steps complete, produce a short summary:

```
✅ ruff   – 0 errors, 0 warnings
✅ mypy   – Success: no issues found
✅ pytest – X passed, Y% coverage
```

Or flag failures clearly:

```
❌ mypy   – 3 errors (see above)
```

---

## When checks fail

- Fix issues in the smallest possible diff.
- Re-run the failing check before moving on.
- Never mark a check as passing without actually running it.
