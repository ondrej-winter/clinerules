# Bootstrap Python Hexagonal Application Repository

## Purpose
Use this skill when asked to initialize a new Python application repository that should follow a modern, opinionated hexagonal-architecture baseline.

This skill is for **project bootstrap only**: establish the initial repository structure, tooling, documentation, and sample composition root so future work starts from a compliant baseline.

## When to use
- The user asks to create a new Python application repo.
- The project should follow hexagonal architecture.
- The user wants a modern Python toolchain with `uv`, `ruff`, `mypy`, and `pytest`.
- The repository does not yet have an agreed starter layout.

## Portability requirement
- Keep this skill usable as a drop-in asset in any repository.
- Do not depend on local repository paths, local folder names, or references to surrounding repo structure.
- Prefer placeholders such as `<package_name>`, `<app_name>`, and `<python_version>` over repository-specific names.

## Required defaults

### Tooling
- Use `uv` for dependency management, environment management, and command execution.
- Keep canonical tool configuration in `pyproject.toml`.
- Treat `uv.lock` as required whenever dependencies are added.
- Use:
  - `ruff` for formatting, linting, and import cleanup
  - `mypy` for type checking
  - `pytest` for tests
  - `pytest-asyncio` only when async code is present

### Architecture
- Follow hexagonal architecture with inward-pointing dependencies.
- Keep business logic isolated from frameworks, transport, and persistence.
- Use the standard layout:

```text
src/<package_name>/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── services/
│   └── exceptions.py
├── application/
│   ├── use_cases/
│   ├── ports/
│   └── dtos/
└── adapters/
    ├── input/
    └── output/

tests/
├── unit/
├── integration/
└── e2e/
```

### Coding and documentation
- Default to explicit type annotations on public functions, methods, ports, DTOs, and boundary types.
- Keep logging centralized; do not scatter global logging setup through feature modules.
- Use a module-level logger when a module emits logs: `LOGGER = logging.getLogger(__name__)`.
- Do not use `print()` in production code.
- Update `README.md` with setup, usage, commands, and any new environment variables.
- Add `docs/adr/` when architectural decisions are being captured from the start.

### Validation and safety
- End with the local quality gate:
  1. `uv run ruff check . --fix`
  2. `uv run ruff format .`
  3. `uv run ruff check .`
  4. `uv run mypy .`
  5. `uv run pytest`
- Never use inline interpreter heredocs such as `python - <<'PY'` or `uv run python - <<'PY'`.
- Prefer direct non-interactive CLI commands.

## Expected bootstrap deliverables
Create a minimal but usable repository baseline with:

1. `pyproject.toml`
2. `uv.lock` after dependency installation/sync
3. `README.md`
4. `src/<package_name>/` package skeleton
5. `tests/` skeleton mirroring the source layout
6. A composition root / entry point such as one of:
   - `src/<package_name>/cli.py`
   - `src/<package_name>/__main__.py`
   - `src/<package_name>/bootstrap.py`
7. Central logging/config bootstrap module when runtime wiring is needed
8. `.gitignore`
9. `docs/adr/` or `docs/` if architecture documentation is requested or implied

## Recommended initial file layout

```text
.
├── .gitignore
├── README.md
├── pyproject.toml
├── uv.lock
├── docs/
│   └── adr/
├── src/
│   └── <package_name>/
│       ├── __init__.py
│       ├── __main__.py
│       ├── bootstrap.py
│       ├── logging_config.py
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── exceptions.py
│       │   ├── entities/
│       │   ├── services/
│       │   └── value_objects/
│       ├── application/
│       │   ├── __init__.py
│       │   ├── dtos/
│       │   ├── ports/
│       │   └── use_cases/
│       └── adapters/
│           ├── __init__.py
│           ├── input/
│           └── output/
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

Keep this skeleton lean. Do not add placeholder files everywhere unless they clarify the intended architecture or are needed for imports, packaging, or tests.

## Bootstrap workflow

### 1. Clarify bootstrap inputs
Before generating files, confirm or infer:
- package name
- app/repo name
- Python version baseline
- whether the app is CLI-only, service-oriented, or library-like
- whether async support is required immediately

If the user does not specify these, choose sensible defaults and state them explicitly in the handoff.

### 2. Initialize tooling
- Create `pyproject.toml` with project metadata and tool configuration.
- Configure `ruff`, `mypy`, and `pytest` there.
- Add runtime and dev dependencies via `uv`.
- Generate `uv.lock`.

Recommended baseline dependencies:
- Runtime: keep minimal; only include what the bootstrap genuinely needs.
- Dev: `ruff`, `mypy`, `pytest`
- Async dev: `pytest-asyncio` only if async code is present

### 3. Create the hexagonal package layout
- Add domain, application, and adapter packages.
- Keep domain pure and free of framework imports.
- Define ports in `application/ports/`.
- Keep I/O and framework code inside adapters and bootstrap modules.

### 4. Create a minimal runnable path
Add a tiny but valid execution path so the repository is not only empty scaffolding. For example:
- a simple CLI adapter
- one application use case
- one output port protocol
- one stub adapter implementation
- bootstrap wiring that connects them

This starter path should prove the architecture, not introduce product complexity.

### 5. Create the test baseline
- Add unit tests first.
- Mirror the source layout under `tests/unit/`.
- Mock output ports in application tests.
- Avoid live I/O in the default suite.

Useful initial tests include:
- one domain behavior test
- one application use case orchestration test
- one adapter smoke/integration test only if there is real I/O wiring to validate

### 6. Document usage
Update `README.md` with:
- project purpose
- Python version
- `uv` setup steps
- install/sync commands
- run command(s)
- test/lint/type-check commands
- brief architecture overview

If you introduce architectural decisions beyond the obvious baseline, add an ADR stub with:
- Context
- Decision
- Consequences
- Alternatives

### 7. Validate before handoff
Run the full local quality gate in order:

```bash
uv run ruff check . --fix
uv run ruff format .
uv run ruff check .
uv run mypy .
uv run pytest
```

If a step fails, fix the root cause before proceeding.

## Implementation constraints
- Keep modules cohesive and small.
- Avoid catch-all modules like broad `utils.py` or `helpers.py`.
- Keep `__init__.py` lightweight.
- Do not let adapters import each other directly unless coordinated through application ports.
- Do not leak transport schemas, ORM models, or framework request/response objects into `domain/` or `application/`.
- Keep environment/config access in adapters or bootstrap modules.
- Use `raise ... from err` when translating exceptions.

## Handoff checklist
Before finishing, confirm that the bootstrap includes:
- a hexagonal source layout
- configured `uv`, `ruff`, `mypy`, and `pytest`
- tests that exercise the initial skeleton
- README setup and usage instructions
- dependency lockfile
- successful quality gate output, or a clear explanation of any user-approved exception

## Suggested output style when using this skill
When completing a bootstrap request:
- briefly state assumptions made
- summarize created files and architectural intent
- list commands run for validation
- call out any next sensible steps, such as adding the first real use case or HTTP adapter
