# Sync shared tools

This folder contains the shared asset sync tool.

## What it does

`sync_shared.py` copies shared repository assets into preconfigured target locations.

It supports:

- file sources
- directory sources
- multiple targets per source
- deleting all configured targets
- reset mode for delete-then-sync

## Run with uv

```bash
uv run tools/sync-shared/sync_shared.py sync
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
```

Recommended workflow:

1. Edit shared content under `shared/`
2. Optionally clear generated targets with `delete`
3. Repopulate targets with `sync` or use `reset`

## Configure mappings

Update `SYNC_MAP` in `tools/sync-shared/sync_shared.py`.

Each entry has:

- `source`: repo-relative source path
- `targets`: one or more repo-relative target paths
