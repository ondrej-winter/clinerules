# Repository-level Cline rules

This directory contains repo-specific maintenance rules. These files guide how
reusable skills, rules, workflows, documentation, and validation tooling are
maintained in this repository.

Root `.clinerules/` files may reference repository-local paths because they are
not portable reusable assets. Reusable content under `shared/` and
`python/hexagonal/` should remain drop-in portable unless a file or section is
explicitly marked as repo-specific.

## Rule ordering

Rules use numeric prefixes so they are easy to read in dependency order:

- `000-readme.md`: Repo-specific index, ownership notes, and validation commands.
- `001-cline-operating-guidance.md`: Atomic Cline operating behavior rule synced from shared sources.
- `002-dropin-portability.md`: Portability requirements for reusable assets.
- `003-plain-formatting.md`: Plain formatting requirements for markdown and text content.
- `004-skill-format.md`: Required structure for repository `SKILL.md` files.
- `005-sync-source-of-truth.md`: Source-of-truth rules for synced workflows.
- `006-validation-workflow.md`: Validation expectations by change type.
- `999-command-execution-safety.md`: Atomic command execution and process safety rule synced from shared sources.

## Synced targets

Some root `.clinerules/` files are generated from shared sources and should not be edited directly:

- `.clinerules/workflows/improve.md` is synced from `shared/clinerules/workflows/improve.md`.
- `.clinerules/001-cline-operating-guidance.md` is synced from `shared/clinerules/001-cline-operating-guidance.md`.
- `.clinerules/999-command-execution-safety.md` is synced from `shared/clinerules/999-command-execution-safety.md`.

When a synced target needs a change, edit the shared source first, run the sync workflow, then validate the repository.

## Validation commands

Run these checks after changing root rules, reusable assets, synced sources, or skill files:

```sh
python3 tools/validate_repo.py
python3 tools/sync-shared/sync_shared.py check
make validate
```

Use the focused Python commands while iterating. Use `make validate` before handoff when available.
