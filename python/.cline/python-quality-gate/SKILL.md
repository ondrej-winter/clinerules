# Skill: Python Quality Gate

Run after any Python code change to verify the codebase is clean.

```bash
uv run ruff check . --fix
uv run mypy .
uv run pytest --cov --cov-report=term-missing
```

All three commands must pass with no errors before the task is considered complete.
