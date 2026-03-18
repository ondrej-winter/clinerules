# Token tools

This folder contains the repository token mapping tool.

## What it does

`repo_token_map.py` scans `shared/` and `python/` recursively and writes one Markdown file with a tree-style map. Each directory line shows aggregated tokens. Each file line shows its own token count.

## Run with uv

```bash
uv run tools/tokens/repo_token_map.py
```

Generated output:

- `tools/tokens/repo-token-map.md`

## Optional usage

Custom roots:

```bash
uv run tools/tokens/repo_token_map.py shared python
```

Custom output path:

```bash
uv run tools/tokens/repo_token_map.py --output tools/tokens/repo-token-map.md
```
