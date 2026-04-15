# clinerules

Collection of curated clinerules.

Currently includes a Python hexagonal-architecture ruleset for Cline, focused on practical repository standards and development workflow guidance.

## Repository tools

- `tools/tokens/repo_token_map.py`: Scans `shared/` and `python/` recursively and writes one tree-style Markdown token map at `tools/tokens/repo-token-map.md`.
- `tools/sync-shared/sync_shared.py`: Copies shared repository assets into their configured target locations and can verify whether derived targets have drifted from their shared sources. It supports file and directory sources, multiple targets per source, cleanup of all configured targets, and a non-mutating drift check.
- `tools/validate_repo.py`: Validates repository-specific conventions for skill frontmatter and repository inventory path references.

Current sync behavior is configured in the script manifest. One source can fan out to multiple repo-relative targets, and directory sources are copied recursively.

Useful commands:

```bash
uv run tools/sync-shared/sync_shared.py sync
uv run tools/sync-shared/sync_shared.py check
uv run tools/sync-shared/sync_shared.py delete
uv run tools/sync-shared/sync_shared.py reset
```

Make targets:

```bash
make sync
make sync-delete
make sync-reset
make tokens
make update
python3 tools/validate_repo.py
```

## Repository-specific inventory

This section is repo-specific. Paths below describe where assets live in this repository.

### `python/hexagonal/`

#### Cline skills

Drop-in SKILL.md files that guide Cline through common development tasks:

| Skill                 | Path                                                             | Purpose                                                                                          |
| --------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Bootstrap app         | `python/hexagonal/agents/skills/bootstrap-python-app/SKILL.md`   | Initialise a Python app repo with `uv`, `ruff`, `mypy`, `pytest`, and a hexagonal `src/` layout  |
| Add hexagonal feature | `python/hexagonal/agents/skills/add-hexagonal-feature/SKILL.md`  | Domain model → application boundaries → application service → unit tests                         |
| Add port              | `python/hexagonal/agents/skills/python-add-port/SKILL.md`        | Define a focused input or output port contract in the application layer                          |
| Add adapter           | `python/hexagonal/agents/skills/python-add-adapter/SKILL.md`     | Add an input (HTTP, CLI, event) or output (DB, API client) adapter with layered testing guidance |
| Update project docs   | `python/hexagonal/agents/skills/update-project-docs/SKILL.md`    | Update README, changelog-style notes, and related project-facing docs after a change             |
| Split Python module   | `python/hexagonal/agents/skills/split-python-module/SKILL.md`    | Split a growing module or package while preserving boundaries and intentional imports             |
| Add observability     | `python/hexagonal/agents/skills/add-observability/SKILL.md`      | Add profiling, metrics, tracing, and operational notes to meaningful workflows                    |
| Write docstrings      | `python/hexagonal/agents/skills/write-python-docstrings/SKILL.md`| Write concise Google-style docstrings and inline comments where they add value                    |
| Write ADR             | `python/hexagonal/agents/skills/write-adr/SKILL.md`              | Scaffold a numbered Architecture Decision Record under `docs/adr/`                               |
| Format Python code    | `python/hexagonal/agents/skills/format-python-code/SKILL.md`     | Run `ruff` formatting and safe auto-fixes                                                        |
| Lint Python code      | `python/hexagonal/agents/skills/lint-python-code/SKILL.md`       | Run `ruff` linting and `mypy` type checking                                                      |
| Write pytest tests    | `python/hexagonal/agents/skills/write-pytest-tests/SKILL.md`     | Write or refactor Python tests in clear, pytest-native style                                     |
| Run Python tests      | `python/hexagonal/agents/skills/run-python-tests/SKILL.md`       | Run the Python test suite with `pytest`                                                          |
| Local quality gate    | `python/hexagonal/agents/skills/run-local-quality-gate/SKILL.md` | Orchestrate formatting, linting, type checking, and tests                                        |

#### Ruleset topics covered

- Core coding standards
- Architecture guardrails
- Testing standards
- Docs and ADR guidance
- Module structure conventions
- Performance and observability guidance
- Repo navigation workflow
- PR and commit hygiene
- Tooling and CI expectations
- Documentation standards
- Logging conventions
- Command execution safety
