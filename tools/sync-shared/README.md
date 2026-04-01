# Sync shared tools

This folder contains the shared asset sync tool.

## What it does

`sync_shared.py` copies shared repository assets into preconfigured target locations.

It supports:

- file sources
- directory sources
- multiple targets per source

## Run with uv

```bash
uv run tools/sync-shared/sync_shared.py
```

## Configure mappings

Update `SYNC_MAP` in `tools/sync-shared/sync_shared.py`.

Each entry has:

- `source`: repo-relative source path
- `targets`: one or more repo-relative target paths
