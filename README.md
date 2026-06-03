# clinerules

Collection of reusable Cline rules, skills, workflows, and supporting
maintenance tools.

The repository currently includes a Python hexagonal-architecture ruleset focused
on practical repository standards, development workflow guidance, and drop-in
portable assets that can be copied into other projects.

## Maintenance workflow

Reusable content should remain self-contained and free of local repository
assumptions unless a section is clearly marked as repo-specific. Keep generated
outputs and synced assets aligned before handoff.

Typical maintenance flow:

1. Edit reusable assets under the relevant source directory.
2. Run `make sync` or `make sync-reset` when shared sources should be copied to
   derived targets.
3. Run `make tokens` after changes under reusable content roots that should be
   reflected in the token map.
4. Run `make validate` before handoff.

## Repository tools

- `tools/tokens/repo_token_map.py`: Scans `shared/` and `python/` recursively and writes one tree-style Markdown token map at `tools/tokens/repo-token-map.md`.
- `tools/sync-shared/sync_shared.py`: Copies shared repository assets into their configured target locations and can verify whether derived targets have drifted from their shared sources. It supports file and directory sources, multiple targets per source, cleanup of all configured targets, and a non-mutating drift check.
- `tools/validate_repo.py`: Validates repository-specific conventions for skill frontmatter, skill names, plain Markdown formatting, reusable-asset portability, and repository inventory path references.

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
make format
make compile
make validate
make update
python3 tools/validate_repo.py
```

Run `make validate` before handoff to check synced assets, repository
conventions, reusable-asset portability, and Python script syntax. Run
`make tokens` after changes under `shared/` or `python/` that should be reflected
in the token map.

## Repository-specific inventory

This section is repo-specific. Paths below describe where assets live in this repository.

### `shared/agents/skills/`

Portable, language-agnostic SKILL.md files for common development and planning
workflows:

| Skill                      | Path                                                       | Purpose                                                                                            |
| -------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Add observability          | `shared/agents/skills/add-observability/SKILL.md`          | Add logs, metrics, traces, profiling, and operational notes without unsupported performance claims |
| Author Agent Skill         | `shared/agents/skills/author-agent-skill/SKILL.md`         | Create, update, or review Agent Skill directories and SKILL.md files                               |
| Interview Me               | `shared/agents/skills/interview-me/SKILL.md`               | Interview users one question at a time to confirm intent before planning or implementation         |
| Review implementation plan | `shared/agents/skills/review-implementation-plan/SKILL.md` | Review plans for scope, ambiguity, sequencing, dependencies, risks, validation, and handoff        |
| Run local quality gate     | `shared/agents/skills/run-local-quality-gate/SKILL.md`     | Discover and run project-defined formatting, linting, static analysis, tests, and build checks     |
| Update project docs        | `shared/agents/skills/update-project-docs/SKILL.md`        | Update project-facing documentation after behavior, configuration, operation, or workflow changes  |
| Write ADR                  | `shared/agents/skills/write-adr/SKILL.md`                  | Create a numbered Architecture Decision Record with context, decision, and consequences            |

The shared `write-adr`, `add-observability`, `using-agent-skills`,
`planning-and-task-breakdown`, `incremental-implementation`,
`test-driven-development`, `debugging-and-error-recovery`,
`code-review-and-quality`, `code-simplification`, `api-and-interface-design`,
`security-and-hardening`, and `source-driven-development` skills are synced into
the Python hexagonal skill catalog. The shared `author-agent-skill`,
`interview-me`, `review-implementation-plan`, and `update-project-docs` skills
are synced into both the Python hexagonal skill catalog and the repository-level
`.agent/skills/` catalog. The shared `run-local-quality-gate` skill is synced
into the repository-level `.agent/skills/` catalog only. The Python hexagonal
catalog keeps specialized Python quality gate guidance.

### `.agent/skills/`

Repository-level Agent Skill files available at the workspace root:

| Skill                      | Path                                                | Purpose                                                                                     |
| -------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Using Agent Skills         | `.agent/skills/using-agent-skills/SKILL.md`         | Discover and invoke the right skill for the current task                                    |
| Interview Me               | `.agent/skills/interview-me/SKILL.md`               | Clarify underspecified user intent before planning or implementation                        |
| Author Agent Skill         | `.agent/skills/author-agent-skill/SKILL.md`         | Create, update, or review Agent Skill directories and SKILL.md files                        |
| Review implementation plan | `.agent/skills/review-implementation-plan/SKILL.md` | Review plans for scope, ambiguity, sequencing, dependencies, risks, validation, and handoff |
| Run local quality gate     | `.agent/skills/run-local-quality-gate/SKILL.md`     | Discover and run project-defined quality checks before handoff                              |
| Update project docs        | `.agent/skills/update-project-docs/SKILL.md`        | Update project-facing documentation after visible changes                                   |

### `shared/clinerules/`

Portable, language-agnostic Cline rules and workflows that can be synced into
rulesets or repository-level `.clinerules/` directories:

| Asset                    | Path                                                | Purpose                                                                       |
| ------------------------ | --------------------------------------------------- | ----------------------------------------------------------------------------- |
| Cline operating guidance | `shared/clinerules/001-cline-operating-guidance.md` | Atomic Cline working style, scope control, editing discipline, and validation |
| Command execution safety | `shared/clinerules/999-command-execution-safety.md` | Atomic command and process execution safety rule for any workspace            |
| Improve workflow         | `shared/clinerules/workflows/improve.md`            | Focused workflow for improving existing rules, skills, workflows, and tooling |

### `python/hexagonal/`

#### Cline skills

Drop-in SKILL.md files that guide Cline through common development tasks:

| Skill                 | Path                                                                   | Purpose                                                                                           |
| --------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Using Agent Skills    | `python/hexagonal/agents/skills/using-agent-skills/SKILL.md`           | Synced shared skill for discovering and invoking the right skill for the current task             |
| Planning tasks        | `python/hexagonal/agents/skills/planning-and-task-breakdown/SKILL.md`  | Synced shared skill for breaking clear requirements into ordered implementable tasks              |
| Incremental build     | `python/hexagonal/agents/skills/incremental-implementation/SKILL.md`   | Synced shared skill for landing changes in small validated slices                                 |
| Bootstrap app         | `python/hexagonal/agents/skills/bootstrap-python-app/SKILL.md`         | Initialise a Python app repo with `uv`, `ruff`, `mypy`, `pytest`, and a hexagonal `src/` layout   |
| Add hexagonal feature | `python/hexagonal/agents/skills/add-hexagonal-feature/SKILL.md`        | Domain model → application boundaries → application service → unit tests                          |
| Author Agent Skill    | `python/hexagonal/agents/skills/author-agent-skill/SKILL.md`           | Synced shared skill for creating, updating, or reviewing Agent Skill directories                  |
| Interview Me          | `python/hexagonal/agents/skills/interview-me/SKILL.md`                 | Synced shared skill for clarifying underspecified user intent before planning or implementation   |
| Review plan           | `python/hexagonal/agents/skills/review-implementation-plan/SKILL.md`   | Synced shared skill for reviewing implementation plans before coding                              |
| API design            | `python/hexagonal/agents/skills/api-and-interface-design/SKILL.md`     | Synced shared skill for designing stable ports, adapters, contracts, and module interfaces        |
| Add port              | `python/hexagonal/agents/skills/python-add-port/SKILL.md`              | Define a focused input or output port contract in the application layer                           |
| Add adapter           | `python/hexagonal/agents/skills/python-add-adapter/SKILL.md`           | Add an input (HTTP, CLI, event) or output (DB, API client) adapter with layered testing guidance  |
| Update project docs   | `python/hexagonal/agents/skills/update-project-docs/SKILL.md`          | Synced shared skill for updating project-facing docs after visible changes                        |
| Split Python module   | `python/hexagonal/agents/skills/split-python-module/SKILL.md`          | Split a growing module or package while preserving boundaries and intentional imports             |
| Source-driven dev     | `python/hexagonal/agents/skills/source-driven-development/SKILL.md`    | Synced shared skill for grounding external library, framework, API, and standard usage in docs    |
| Debugging             | `python/hexagonal/agents/skills/debugging-and-error-recovery/SKILL.md` | Synced shared skill for reproducing, localizing, fixing, and guarding failures                    |
| Add observability     | `python/hexagonal/agents/skills/add-observability/SKILL.md`            | Synced shared skill for logs, metrics, traces, profiling, and operational notes                   |
| Security hardening    | `python/hexagonal/agents/skills/security-and-hardening/SKILL.md`       | Synced shared skill for hardening adapters, configuration, secrets, and untrusted input handling  |
| Write docstrings      | `python/hexagonal/agents/skills/write-python-docstrings/SKILL.md`      | Write concise Google-style docstrings and inline comments where they add value                    |
| Write ADR             | `python/hexagonal/agents/skills/write-adr/SKILL.md`                    | Scaffold a numbered Architecture Decision Record under `docs/adr/`                                |
| Test-driven dev       | `python/hexagonal/agents/skills/test-driven-development/SKILL.md`      | Synced shared skill for driving behavior changes with tests                                       |
| Format Python code    | `python/hexagonal/agents/skills/format-python-code/SKILL.md`           | Run `ruff` formatting and safe auto-fixes                                                         |
| Lint Python code      | `python/hexagonal/agents/skills/lint-python-code/SKILL.md`             | Run `ruff` linting and `mypy` type checking                                                       |
| Write pytest tests    | `python/hexagonal/agents/skills/write-pytest-tests/SKILL.md`           | Write or refactor Python tests in clear, pytest-native style                                      |
| Run Python tests      | `python/hexagonal/agents/skills/run-python-tests/SKILL.md`             | Run the Python test suite with `pytest`                                                           |
| Local quality gate    | `python/hexagonal/agents/skills/run-local-quality-gate/SKILL.md`       | Orchestrate formatting, linting, type checking, and tests                                         |
| Code review           | `python/hexagonal/agents/skills/code-review-and-quality/SKILL.md`      | Synced shared skill for reviewing correctness, architecture, tests, docs, and validation evidence |
| Code simplification   | `python/hexagonal/agents/skills/code-simplification/SKILL.md`          | Synced shared skill for reducing unnecessary complexity without changing behavior                 |

#### Ruleset topics covered

- Core coding standards
- Architecture guardrails
- Testing standards
- Docs and ADR guidance
- Module structure conventions
- Performance and observability guidance
- Configuration and secrets management
- Repo navigation workflow
- PR and commit hygiene
- Tooling and CI expectations
- Documentation standards
- Logging conventions
- Command execution safety
