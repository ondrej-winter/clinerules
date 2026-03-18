# Skill: Bootstrap a Python Hexagonal Application

Use this skill when the user asks to initialise a new Python project that follows
hexagonal (ports & adapters) architecture.

## Prerequisites

- `uv` is installed on the machine (`brew install uv` / `pip install uv`).
- The user has told you `<app_name>` (the project / package name).
- The user has told you `<python_version>` (e.g. `3.13`).

## Steps

### 1 — Initialise the project with uv

```bash
uv init <app_name> --python <python_version>
cd <app_name>
```

### 2 — Create the hexagonal src/ layout

```
<app_name>/
├── src/
│   └── <app_name>/
│       ├── __init__.py
│       ├── domain/          # Pure domain: entities, value objects, domain events
│       │   └── __init__.py
│       ├── application/     # Use cases, application services, port interfaces
│       │   ├── __init__.py
│       │   └── ports/
│       │       └── __init__.py
│       └── adapters/        # Input & output adapter implementations
│           ├── __init__.py
│           ├── input/
│           │   └── __init__.py
│           └── output/
│               └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   └── __init__.py
│   └── integration/
│       └── __init__.py
├── pyproject.toml
└── README.md
```

Create every directory and `__init__.py` file listed above.

### 3 — Configure pyproject.toml

Replace or merge the generated `pyproject.toml` with the following structure (keep
any values `uv init` already set for `name`, `version`, `requires-python`):

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "<app_name>"
version = "0.1.0"
requires-python = ">= <python_version>"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8",
    "pytest-cov>=6",
    "mypy>=1.10",
    "ruff>=0.4",
]

[tool.hatch.build.targets.wheel]
packages = ["src/<app_name>"]

[tool.ruff]
line-length = 100
target-version = "py<python_version_nodot>"   # e.g. py313

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
ignore = []

[tool.mypy]
python_version = "<python_version>"
strict = true
files = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing"
```

> Replace `<python_version_nodot>` with the version without the dot (e.g. `313`).

### 4 — Install dev dependencies

```bash
uv sync --all-extras
```

### 5 — Set up ruff and pre-commit (optional but recommended)

```bash
uv add --dev pre-commit
uv run pre-commit install
```

Add a minimal `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0 # pin to latest stable
    hooks:
      - id: ruff
        args: ["--fix"]
      - id: ruff-format
```

### 6 — Verify the setup

```bash
uv run ruff check .
uv run mypy .
uv run pytest
```

All three commands must exit with code 0 before proceeding.

### 7 — Create a minimal README

Write a `README.md` that describes:

- What the application does.
- How to install dependencies (`uv sync --all-extras`).
- How to run quality checks (`ruff`, `mypy`, `pytest`).
- High-level architecture overview (domain / application / adapters).

## Hexagonal architecture conventions to follow

| Layer             | Directory                         | Rule                                                                   |
| ----------------- | --------------------------------- | ---------------------------------------------------------------------- |
| Domain            | `src/<app_name>/domain/`          | No imports from `application` or `adapters`. Pure Python only.         |
| Application       | `src/<app_name>/application/`     | Depends only on `domain`. Defines port interfaces (ABCs or Protocols). |
| Adapters (input)  | `src/<app_name>/adapters/input/`  | Calls into `application`. Never imports from `domain` directly.        |
| Adapters (output) | `src/<app_name>/adapters/output/` | Implements port interfaces from `application`.                         |

Enforce these rules via import linter (e.g. `import-linter`) or document them in
`ARCHITECTURE.md` at the root of the project.
