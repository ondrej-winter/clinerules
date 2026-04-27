# Sync shared tools

This folder contains the shared asset sync tool.

## What it does

`sync_shared.py` copies shared repository assets into preconfigured target locations.

It supports:

- file sources
- directory sources
- multiple targets per source
- non-mutating drift checks
- deleting all configured targets
- reset mode for delete-then-sync

## Run with uv

```bash
uv run tools/sync-shared/sync_shared.py sync
```

Verify that configured targets still match their shared sources:

```bash
uv run tools/sync-shared/sync_shared.py check
```

Delete all configured targets:

```bash
uv run tools/sync-shared/sync_shared.py delete
```

Delete all configured targets and sync them again:

```bash
uv run tools/sync-shared/sync_shared.py reset
```

If no command is provided, `sync` is used by default.

From the repository root, you can also use:

```bash
make sync
make sync-delete
make sync-reset
make validate
```

Recommended workflow:

1. Edit shared content under `shared/`
2. Repopulate targets with `sync` or use `reset`
3. Run `check` before final review or pre-commit to confirm the derived targets
   still match their shared sources

Run `make sync` after shared-source edits so the derived targets under
`python/hexagonal/` stay aligned with their sources.

Run `uv run tools/sync-shared/sync_shared.py check` when you want a non-mutating
verification pass, such as in pre-commit or before handoff.

Run `make validate` before handoff to combine the sync drift check with the
repository convention checks and Python compile check.

If you change shared content and repository inventory docs in the same update,
run `make sync` before final review so generated targets reflect the current
source of truth.

## Configure mappings

Update `SYNC_MAP` in `tools/sync-shared/sync_shared.py`.

Each entry has:

- `source`: repo-relative source path
- `targets`: one or more repo-relative target paths
