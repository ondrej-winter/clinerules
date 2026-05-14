"""Copy shared repository assets into their configured target locations."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


@dataclass(frozen=True)
class SyncEntry:
    """Repo-relative shared source and the targets derived from it."""

    source: str
    targets: tuple[str, ...]


@dataclass(frozen=True)
class SyncCheckIssue:
    """A missing, mismatched, or drifted sync target."""

    source: Path
    target: Path
    issue: str
    details: str | None = None


SYNC_MAP: tuple[SyncEntry, ...] = (
    SyncEntry(
        source='shared/clinerules/workflows/improve.md',
        targets=(
            'python/hexagonal/clinerules/workflows/',
            '.clinerules/workflows/',
        ),
    ),
    SyncEntry(
        source='shared/agents/skills/write-adr',
        targets=('python/hexagonal/agents/skills/write-adr',),
    ),
    SyncEntry(
        source='shared/agents/skills/add-observability',
        targets=('python/hexagonal/agents/skills/add-observability',),
    ),
    SyncEntry(
        source='shared/agents/skills/update-project-docs',
        targets=('python/hexagonal/agents/skills/update-project-docs',),
    ),
    SyncEntry(
        source='shared/clinerules/hooks/PreToolUse',
        targets=(
            'python/hexagonal/clinerules/hooks/',
            '.clinerules/hooks/',
        ),
    ),
    SyncEntry(
        source='shared/clinerules/hooks/pretooluse.py',
        targets=(
            'python/hexagonal/clinerules/hooks/',
            '.clinerules/hooks/',
        ),
    ),
)


def parse_args() -> argparse.Namespace:
    """Parse the sync command to run."""

    parser = argparse.ArgumentParser(
        description='Sync shared repository assets to configured targets.'
    )
    parser.add_argument(
        'command',
        nargs='?',
        choices=('sync', 'delete', 'reset', 'check'),
        default='sync',
        help='Command to run. Defaults to sync.',
    )
    return parser.parse_args()


def resolve_repo_path(relative_path: str) -> Path:
    """Resolve a repo-relative path and reject paths outside the repository."""

    path = (REPO_ROOT / relative_path).resolve()
    repo_root = REPO_ROOT.resolve()

    try:
        path.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(f"Path escapes repository root: {relative_path}") from exc

    return path


def repo_relative(path: Path) -> Path:
    """Return a path relative to the repository root for display."""

    return path.relative_to(REPO_ROOT)


def resolve_file_target(source: Path, target_relative: str) -> Path:
    """Resolve a file target, treating trailing slashes as target directories."""

    if target_relative.endswith(('/', '\\')):
        return resolve_repo_path(str(Path(target_relative) / source.name))

    return resolve_repo_path(target_relative)


def compare_paths(source: Path, target: Path) -> list[SyncCheckIssue]:
    """Return differences between a source file or directory and its target."""

    if not target.exists():
        return [SyncCheckIssue(source=source, target=target, issue='missing_target')]

    if source.is_file() and target.is_file():
        if source.read_bytes() != target.read_bytes():
            return [
                SyncCheckIssue(
                    source=source,
                    target=target,
                    issue='content_mismatch',
                )
            ]
        return []

    if source.is_dir() and target.is_dir():
        issues: list[SyncCheckIssue] = []
        source_entries = {item.name: item for item in source.iterdir()}
        target_entries = {item.name: item for item in target.iterdir()}

        for name in sorted(source_entries):
            target_entry = target_entries.get(name)
            if target_entry is None:
                issues.append(
                    SyncCheckIssue(
                        source=source_entries[name],
                        target=target / name,
                        issue='missing_target',
                    )
                )
                continue
            issues.extend(compare_paths(source_entries[name], target_entry))

        for name in sorted(set(target_entries) - set(source_entries)):
            issues.append(
                SyncCheckIssue(
                    source=source / name,
                    target=target_entries[name],
                    issue='content_mismatch',
                    details='target has extra path not present in source',
                )
            )

        return issues

    source_kind = 'directory' if source.is_dir() else 'file'
    target_kind = 'directory' if target.is_dir() else 'file'
    return [
        SyncCheckIssue(
            source=source,
            target=target,
            issue='type_mismatch',
            details=f'source is a {source_kind}, target is a {target_kind}',
        )
    ]


def collect_sync_issues(entry: SyncEntry) -> list[SyncCheckIssue]:
    """Collect sync drift issues for one configured mapping."""

    source = resolve_repo_path(entry.source)
    issues: list[SyncCheckIssue] = []

    if source.is_file():
        for target_relative in entry.targets:
            issues.extend(compare_paths(source, resolve_file_target(source, target_relative)))
        return issues

    if source.is_dir():
        for target_relative in entry.targets:
            issues.extend(compare_paths(source, resolve_repo_path(target_relative)))
        return issues

    raise FileNotFoundError(f"Missing source path: {entry.source}")


def sync_file(source_relative: str, target_relative: str) -> None:
    """Copy one shared file to one configured target."""

    source = resolve_repo_path(source_relative)
    target = resolve_file_target(source, target_relative)

    if not source.is_file():
        raise FileNotFoundError(f"Missing source file: {source_relative}")

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    print(f"Synced {source_relative} -> {repo_relative(target)}")


def sync_directory(source_relative: str, target_relative: str) -> None:
    """Replace one target directory with a copy of one shared directory."""

    source = resolve_repo_path(source_relative)
    target = resolve_repo_path(target_relative)

    if not source.is_dir():
        raise FileNotFoundError(f"Missing source directory: {source_relative}")

    if target.exists():
        if target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    print(f"Synced {source_relative}/ -> {target_relative}/")


def sync_entry(entry: SyncEntry) -> None:
    """Sync all targets for one configured source."""

    source = resolve_repo_path(entry.source)

    if source.is_file():
        for target in entry.targets:
            sync_file(entry.source, target)
        return

    if source.is_dir():
        for target in entry.targets:
            sync_directory(entry.source, target)
        return

    raise FileNotFoundError(f"Missing source path: {entry.source}")


def delete_target(target_relative: str) -> None:
    """Delete one configured target file or directory if it exists."""

    target = resolve_repo_path(target_relative)

    if not target.exists():
        print(f"Skipped missing target: {target_relative}")
        return

    if target.is_file():
        target.unlink()
        print(f"Deleted file target: {target_relative}")
        return

    shutil.rmtree(target)
    print(f"Deleted directory target: {target_relative}")


def delete_entry_targets(entry: SyncEntry) -> None:
    """Delete every target derived from one configured source."""

    source = resolve_repo_path(entry.source)

    for target_relative in entry.targets:
        if source.is_file():
            delete_target(str(repo_relative(resolve_file_target(source, target_relative))))
            continue

        delete_target(target_relative)


def delete_all_targets() -> None:
    """Delete all configured sync targets."""

    for entry in SYNC_MAP:
        delete_entry_targets(entry)


def check_all_targets() -> int:
    """Check every configured target and return a process exit code."""

    issues: list[SyncCheckIssue] = []
    for entry in SYNC_MAP:
        issues.extend(collect_sync_issues(entry))

    if not issues:
        print('All configured sync targets are aligned.')
        return 0

    for issue in sorted(issues, key=lambda item: (str(item.target), item.issue, str(item.source))):
        summary = (
            f"{issue.issue}: {repo_relative(issue.source)} -> "
            f"{repo_relative(issue.target)}"
        )
        if issue.details:
            summary = f'{summary} ({issue.details})'
        print(summary)

    return 1


def main() -> int:
    """Run the requested sync command."""

    args = parse_args()

    if args.command == 'check':
        return check_all_targets()

    if args.command in {'delete', 'reset'}:
        delete_all_targets()

    if args.command == 'delete':
        return 0

    for entry in SYNC_MAP:
        sync_entry(entry)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
