"""Copy shared repository assets into their configured target locations."""

from __future__ import annotations

import argparse
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Sync shared repository assets to configured targets.'
    )
    parser.add_argument(
        'command',
        nargs='?',
        choices=('sync', 'delete', 'reset'),
        default='sync',
        help='Command to run. Defaults to sync.',
    )
    return parser.parse_args()


def resolve_repo_path(relative_path: str) -> Path:
    path = (REPO_ROOT / relative_path).resolve()
    repo_root = REPO_ROOT.resolve()

    try:
        path.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(f'Path escapes repository root: {relative_path}') from exc

    return path


def sync_file(source_relative: str, target_relative: str) -> None:
    source = resolve_repo_path(source_relative)
    target = resolve_repo_path(target_relative)

    if not source.is_file():
        raise FileNotFoundError(f'Missing source file: {source_relative}')

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    print(f'Synced {source_relative} -> {target_relative}')


def sync_directory(source_relative: str, target_relative: str) -> None:
    source = resolve_repo_path(source_relative)
    target = resolve_repo_path(target_relative)

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
    source = resolve_repo_path(entry.source)

    if source.is_file():
        for target in entry.targets:
            sync_file(entry.source, target)
        return

    if source.is_dir():
        for target in entry.targets:
            sync_directory(entry.source, target)
        return

    raise FileNotFoundError(f'Missing source path: {entry.source}')


def delete_target(target_relative: str) -> None:
    target = resolve_repo_path(target_relative)

    if not target.exists():
        print(f'Skipped missing target: {target_relative}')
        return

    if target.is_file():
        target.unlink()
        print(f'Deleted file target: {target_relative}')
        return

    shutil.rmtree(target)
    print(f'Deleted directory target: {target_relative}')


def delete_all_targets() -> None:
    for entry in SYNC_MAP:
        for target in entry.targets:
            delete_target(target)


def main() -> int:
    args = parse_args()

    if args.command in {'delete', 'reset'}:
        delete_all_targets()

    if args.command == 'delete':
        return 0

    for entry in SYNC_MAP:
        sync_entry(entry)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
