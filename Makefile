.PHONY: help sync sync-delete sync-reset tokens improve-skills format compile validate update

help:
	@echo "Available targets:"
	@echo "  sync         Sync shared assets into configured targets"
	@echo "  sync-delete  Delete all configured sync targets"
	@echo "  sync-reset   Delete and recreate all configured sync targets"
	@echo "  tokens       Update the repository token map"
	@echo "  improve-skills Run Cline skill maintenance across skill folders"
	@echo "  format       Format Markdown files"
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

improve-skills:
	python3 tools/skills/run_cline_skill_workflow.py

format:
	pre-commit run prettier-markdown --all-files

compile:
	python3 -m compileall tools
	find tools -type d -name __pycache__ -prune -exec rm -rf {} +

validate: compile
	python3 tools/sync-shared/sync_shared.py check
	python3 tools/validate_repo.py

update: sync-reset tokens
