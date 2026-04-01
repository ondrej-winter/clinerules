.PHONY: help sync sync-delete sync-reset tokens update

help:
	@echo "Available targets:"
	@echo "  sync         Sync shared assets into configured targets"
	@echo "  sync-delete  Delete all configured sync targets"
	@echo "  sync-reset   Delete and recreate all configured sync targets"
	@echo "  tokens       Update the repository token map"
	@echo "  update       Reset synced assets and update the token map"

sync:
	uv run tools/sync-shared/sync_shared.py sync

sync-delete:
	uv run tools/sync-shared/sync_shared.py delete

sync-reset:
	uv run tools/sync-shared/sync_shared.py reset

tokens:
	uv run tools/tokens/repo_token_map.py

update: sync-reset tokens
