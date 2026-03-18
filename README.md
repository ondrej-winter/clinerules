# clinerules
Collection of curated clinerules.

Currently includes a Python hexagonal-architecture ruleset for Cline, focused on practical repository standards and development workflow guidance.

## `python/hexagonal/`

### Cline skills

Drop-in SKILL.md files that guide Cline through common development tasks:

| Skill | Path | Purpose |
|---|---|---|
| Bootstrap app | `python/hexagonal/.agents/skills/bootstrap-python-app/SKILL.md` | Initialise a Python app repo with `uv`, `ruff`, `mypy`, `pytest`, and a hexagonal `src/` layout |
| Add hexagonal feature | `python/hexagonal/.agents/skills/add-hexagonal-feature/SKILL.md` | Domain model → port interfaces → application service → unit tests |
| Add adapter | `python/hexagonal/.agents/skills/python-add-adapter/SKILL.md` | Add an input (HTTP, CLI, event) or output (DB, API client) adapter with layered testing guidance |
| Write ADR | `python/hexagonal/.agents/skills/write-adr/SKILL.md` | Scaffold a numbered Architecture Decision Record under `docs/adr/` |

### GitHub Actions workflow templates

Drop-in workflow files to copy into `.github/workflows/`:

| Workflow | Path | Trigger |
|---|---|---|
| CI | `workflows/ci.yml` | PR + push to `main` — runs ruff, mypy, pytest with 80% coverage gate |
| Release | `workflows/release.yml` | Tag push (`v*`) — builds and publishes to PyPI via OIDC trusted publishing |

### Ruleset topics covered

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
