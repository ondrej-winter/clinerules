.PHONY: help sync sync-delete sync-reset tokens compile validate update

help:
	@echo "Available targets:"
	@echo "  sync         Sync shared assets into configured targets"
	@echo "  sync-delete  Delete all configured sync targets"
	@echo "  sync-reset   Delete and recreate all configured sync targets"
	@echo "  tokens       Update the repository token map"
	@echo "  compile      Compile repository Python scripts"
	@echo "  validate     Run repository validation checks"
	@echo "  update       Reset synced assets and update the token map"

sync:
	uv run tools/sync-shared/sync_shared.py sync

sync-delete:
	uv run tools/sync-shared/sync_shared.py delete

sync-reset:
	uv run tools/sync-shared/sync_shared.py reset

tokens:
	uv run tools/tokens/repo_token_map.py

compile:
	python3 -m compileall tools shared/clinerules/hooks python/hexagonal/clinerules/hooks
	find tools shared/clinerules/hooks python/hexagonal/clinerules/hooks -type d -name __pycache__ -prune -exec rm -rf {} +

validate: compile
	python3 tools/sync-shared/sync_shared.py check
	python3 tools/validate_repo.py

update: sync-reset tokens
