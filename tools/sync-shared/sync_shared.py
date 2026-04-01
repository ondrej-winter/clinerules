"""Copy shared repository assets into their configured target locations."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


@dataclass(frozen=True)
class SyncEntry:
    source: str
    targets: tuple[str, ...]


SYNC_MAP: tuple[SyncEntry, ...] = (
    SyncEntry(
        source='shared/clinerules/workflows/improve.md',
        targets=(
            'python/hexagonal/clinerules/workflows/improve.md',
        ),
    ),
    SyncEntry(
        source='shared/agents/skills/write-adr',
        targets=(
            'python/hexagonal/agents/skills/write-adr',
        ),
    ),
)


def sync_file(source_relative: str, target_relative: str) -> None:
    source = REPO_ROOT / source_relative
    target = REPO_ROOT / target_relative

    if not source.is_file():
        raise FileNotFoundError(f'Missing source file: {source_relative}')

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    print(f'Synced {source_relative} -> {target_relative}')


def sync_directory(source_relative: str, target_relative: str) -> None:
    source = REPO_ROOT / source_relative
    target = REPO_ROOT / target_relative

    if not source.is_dir():
        raise FileNotFoundError(f'Missing source directory: {source_relative}')

    if target.exists():
        if target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    print(f'Synced {source_relative}/ -> {target_relative}/')


def sync_entry(entry: SyncEntry) -> None:
    source = REPO_ROOT / entry.source

    if source.is_file():
        for target in entry.targets:
            sync_file(entry.source, target)
        return

    if source.is_dir():
        for target in entry.targets:
            sync_directory(entry.source, target)
        return

    raise FileNotFoundError(f'Missing source path: {entry.source}')


def main() -> int:
    for entry in SYNC_MAP:
        sync_entry(entry)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
