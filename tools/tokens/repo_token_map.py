"""Generate a single tree-style Markdown token map for repository content."""

# /// script
# dependencies = [
#   "tiktoken",
# ]
# ///

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

import tiktoken


DEFAULT_ROOTS = ('shared', 'python')
DEFAULT_OUTPUT = 'tools/tokens/repo-token-map.md'
DEFAULT_ENCODING = 'cl100k_base'
SKIP_DIRS = {
    '.git',
    '.mypy_cache',
    '.pytest_cache',
    '.ruff_cache',
    '.venv',
    '__pycache__',
    'node_modules',
}
SKIP_SUFFIXES = {
    '.png',
    '.jpg',
    '.jpeg',
    '.gif',
    '.webp',
    '.ico',
    '.pdf',
    '.zip',
    '.gz',
    '.tar',
    '.tgz',
    '.bz2',
    '.xz',
    '.7z',
    '.pyc',
    '.pyo',
    '.so',
    '.dylib',
    '.db',
    '.sqlite',
    '.sqlite3',
    '.mp3',
    '.mp4',
    '.mov',
    '.avi',
}


@dataclass(slots=True)
class FileStat:
    path: Path
    tokens: int


@dataclass(slots=True)
class TreeNode:
    name: str
    path: Path
    is_dir: bool
    tokens: int = 0
    children: dict[str, 'TreeNode'] = field(default_factory=dict)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Generate a tree-style Markdown token map for repository folders.'
    )
    parser.add_argument(
        'roots',
        nargs='*',
        default=list(DEFAULT_ROOTS),
        help='Root directories to scan recursively. Defaults to: shared python',
    )
    parser.add_argument(
        '--output',
        default=DEFAULT_OUTPUT,
        help=f"Markdown output path. Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        '--encoding',
        default=DEFAULT_ENCODING,
        help=f"tiktoken encoding name. Default: {DEFAULT_ENCODING}",
    )
    return parser.parse_args()


def is_probably_binary(data: bytes) -> bool:
    if not data:
        return False
    if b'\x00' in data:
        return True
    text_bytes = sum(
        1
        for byte in data
        if byte in (9, 10, 13) or 32 <= byte <= 126 or byte >= 128
    )
    return text_bytes / len(data) < 0.85


def should_skip(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    return path.suffix.lower() in SKIP_SUFFIXES


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob('*'):
        if not path.is_file() or should_skip(path):
            continue
        files.append(path)
    return sorted(files)


def read_text_file(path: Path) -> str | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if is_probably_binary(raw):
        return None
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return raw.decode('utf-8', errors='replace')


def collect_stats(repo_root: Path, scan_roots: list[str], encoding_name: str) -> list[FileStat]:
    encoding = tiktoken.get_encoding(encoding_name)
    stats: list[FileStat] = []
    for root_name in scan_roots:
        root_path = repo_root / root_name
        if not root_path.exists() or not root_path.is_dir():
            print(f"Skipping missing root: {root_name}", file=sys.stderr)
            continue
        for path in iter_files(root_path):
            text = read_text_file(path)
            if text is None:
                continue
            stats.append(
                FileStat(
                    path=path.relative_to(repo_root),
                    tokens=len(encoding.encode(text)),
                )
            )
    return sorted(stats, key=lambda item: item.path.as_posix())


def build_tree(stats: list[FileStat]) -> TreeNode:
    root = TreeNode(name='.', path=Path('.'), is_dir=True)
    for stat in stats:
        current = root
        current.tokens += stat.tokens
        parts = stat.path.parts
        for index, part in enumerate(parts):
            is_dir = index < len(parts) - 1
            next_path = Path(*parts[: index + 1])
            if part not in current.children:
                current.children[part] = TreeNode(name=part, path=next_path, is_dir=is_dir)
            current = current.children[part]
            current.tokens += stat.tokens
    return root


def render_node(node: TreeNode, prefix: str = '', is_last: bool = True) -> list[str]:
    label = f"{node.name}/" if node.is_dir and node.name != '.' else node.name
    if node.name == '.':
        lines: list[str] = []
    else:
        connector = '└── ' if is_last else '├── '
        lines = [f"{prefix}{connector}{label} ({node.tokens})"]

    child_prefix = prefix + ('    ' if is_last else '│   ') if node.name != '.' else ''
    children = sorted(
        node.children.values(),
        key=lambda item: (not item.is_dir, item.name.lower()),
    )
    for index, child in enumerate(children):
        lines.extend(
            render_node(
                child,
                prefix=child_prefix,
                is_last=index == len(children) - 1,
            )
        )
    return lines


def build_report(stats: list[FileStat], scan_roots: list[str], encoding_name: str) -> str:
    tree = build_tree(stats)
    body_lines: list[str] = []
    root_nodes = [tree.children[root] for root in scan_roots if root in tree.children]
    for index, node in enumerate(root_nodes):
        body_lines.extend(render_node(node, prefix='', is_last=index == len(root_nodes) - 1))

    parts = [
        '# Repo token map',
        '',
        f"Scanned roots: {', '.join(scan_roots)}",
        f"Files counted: {len(stats)}",
        f"Total tokens: {sum(item.tokens for item in stats)}",
        f"Tokenizer encoding: {encoding_name}",
        '',
        '## Tree',
        '',
        '```text',
        *body_lines,
        '```',
        '',
    ]
    return '\n'.join(parts)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent.parent
    stats = collect_stats(repo_root, args.roots, args.encoding)
    if not stats:
        print('No text files found in the requested roots.', file=sys.stderr)
        return 1

    output_path = repo_root / args.output
    write_text(output_path, build_report(stats, args.roots, args.encoding))

    print(f"Wrote token map: {output_path.relative_to(repo_root)}")
    print(f"Scanned files: {len(stats)}")
    print(f"Total tokens: {sum(item.tokens for item in stats)}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
