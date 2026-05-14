# Validation workflow for repository maintenance

This is a repo-specific maintenance rule for choosing validation commands after changing rules, reusable assets, synced sources, hooks, skills, or tooling.

## Core rule

- Run the narrowest useful validation while iterating.
- Run the full repository validation before handoff when available.
- Treat validation failures as part of the change until they are fixed or explicitly documented.

## Required checks by change type

- Root `.clinerules/` rule changes:
  - `python3 tools/validate_repo.py`
  - `python3 tools/sync-shared/sync_shared.py check`
  - `make validate` before handoff when available
- Reusable asset changes under `shared/` or `python/hexagonal/`:
  - `python3 tools/validate_repo.py`
  - `python3 tools/sync-shared/sync_shared.py check` when workflows or hooks are involved
  - `make validate` before handoff when available
- Skill file changes:
  - `python3 tools/validate_repo.py`
  - Manual review of `SKILL.md` frontmatter, heading, and reusable examples
- Shared workflow or hook source changes:
  - Run the sync command or sync check documented for this repository
  - Confirm all intended targets changed or remain aligned
  - `make validate` before handoff when available
- Tooling script changes:
  - Run the focused script command when practical
  - Run `make validate` before handoff when available

## Manual review checks

- Confirm no decorative formatting, emojis, or ornamental separators were added.
- Confirm portable content does not depend on repository-local paths unless explicitly marked repo-specific.
- Confirm synced targets were not edited directly unless the local exception is intentional and documented.
- Confirm new or renamed files are reflected in any relevant index, README, or inventory.

## Handoff guidance

Summarize which files changed and which validation commands passed. If a recommended command was not run, state why and note the risk for the next maintainer.
