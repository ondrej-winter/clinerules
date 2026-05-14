# Sync source-of-truth for generated targets

This is a repo-specific maintenance rule for files copied from shared sources into target `.clinerules/` directories.

## Core rule

- Treat synced workflow and hook files as derived targets, not primary editing locations.
- Edit the configured shared source before changing a synced target.
- Keep every synced target aligned with its source unless an intentional local exception is documented.

## Synced root targets

The root `.clinerules/` directory includes these synced targets:

- `.clinerules/workflows/improve.md` comes from `shared/clinerules/workflows/improve.md`.
- `.clinerules/hooks/PreToolUse` comes from `shared/clinerules/hooks/PreToolUse`.
- `.clinerules/hooks/pretooluse.py` comes from `shared/clinerules/hooks/pretooluse.py`.

Other reusable rule sets may also receive synced copies from the same shared sources. Check the sync configuration before editing a workflow or hook target.

## Required workflow

1. Identify whether the file is a shared source or a synced target.
2. If it is a synced target, find the corresponding source before editing.
3. Make the change at the source when the behavior should apply to all synced copies.
4. Run the repository sync command or sync check required for the change.
5. Validate the repository before handoff.

## Local exceptions

Direct edits to synced targets are allowed only when the change is intentionally local to that target. Document the reason near the change or in the relevant maintenance notes, then confirm the sync strategy will not overwrite the local exception unexpectedly.

## Review guidance

- Treat unexpected sync drift as a defect.
- Confirm source and target files are aligned after shared source changes.
- Confirm direct target edits are intentional, documented, and not better handled at the shared source.
- Run `python3 tools/sync-shared/sync_shared.py check` before handoff.
