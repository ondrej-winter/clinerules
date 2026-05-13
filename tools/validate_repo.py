"""Validate repository-specific markdown conventions and inventory references."""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATHS = (
    REPO_ROOT / 'shared' / 'agents' / 'skills',
    REPO_ROOT / 'python' / 'hexagonal' / 'agents' / 'skills',
)
README_PATH = REPO_ROOT / 'README.md'
SKILL_NAME_PATTERN = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
EMOJI_PATTERN = re.compile(
    '['
    '\U0001F300-\U0001FAFF'
    '\U00002700-\U000027BF'
    '\U00002600-\U000026FF'
    ']'
)
DECORATIVE_SEPARATOR_PATTERN = re.compile(r'^([=*_])\1{3,}$|^-{4,}$')
REUSABLE_ASSET_PATHS = (
    REPO_ROOT / 'shared',
    REPO_ROOT / 'python' / 'hexagonal',
)
REPO_SPECIFIC_REFERENCE_PATTERNS = (
    re.compile(r'/Users/'),
    re.compile(r'ondrej', flags=re.IGNORECASE),
    re.compile(r'nosync', flags=re.IGNORECASE),
    re.compile(r'clinerules repository', flags=re.IGNORECASE),
    re.compile(r'repo-token-map'),
    re.compile(r'tools/'),
    re.compile(r'shared/'),
    re.compile(r'python/hexagonal/'),
)
SKIP_MARKDOWN_DIRS = {
    '.git',
    '.cline-logs',
    '.mypy_cache',
    '.pytest_cache',
    '.ruff_cache',
    '.venv',
    '__pycache__',
    'node_modules',
}


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def iter_skill_files() -> list[Path]:
    files: list[Path] = []
    for root in SKILL_PATHS:
        if not root.exists():
            continue
        files.extend(sorted(root.glob('*/SKILL.md')))
    return files


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO_ROOT.rglob('*.md'):
        if any(part in SKIP_MARKDOWN_DIRS for part in path.relative_to(REPO_ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def is_reusable_asset(path: Path) -> bool:
    return any(is_relative_to(path, root) for root in REUSABLE_ASSET_PATHS)


def extract_frontmatter(text: str, path: Path) -> tuple[str, str, list[str]]:
    if not text.startswith('---\n'):
        return '', text, [f"{repo_relative(path)}: missing YAML frontmatter start"]

    parts = text.split('---\n', 2)
    if len(parts) < 3:
        return '', text, [f"{repo_relative(path)}: malformed YAML frontmatter"]

    return parts[1], parts[2].lstrip('\n'), []


def extract_frontmatter_field(frontmatter: str, field_name: str) -> str | None:
    match = re.search(rf'^{field_name}:\s+(.+)$', frontmatter, flags=re.MULTILINE)
    if match is None:
        return None
    return match.group(1).strip()


def validate_skill_name(path: Path, frontmatter: str) -> list[str]:
    errors: list[str] = []
    skill_name = extract_frontmatter_field(frontmatter, 'name')
    if skill_name is None:
        return errors

    if not SKILL_NAME_PATTERN.fullmatch(skill_name):
        errors.append(f"{repo_relative(path)}: frontmatter name is not kebab-case: {skill_name}")

    expected_name = path.parent.name
    if skill_name != expected_name:
        errors.append(
            f"{repo_relative(path)}: frontmatter name does not match directory "
            f"name: {skill_name} != {expected_name}"
        )

    return errors


def validate_skill_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding='utf-8')

    frontmatter, body, frontmatter_errors = extract_frontmatter(text, path)
    if frontmatter_errors:
        return frontmatter_errors

    if not re.search(r'^name:\s+.+$', frontmatter, flags=re.MULTILINE):
        errors.append(f"{repo_relative(path)}: missing frontmatter name field")
    if not re.search(r'^description:\s+.+$', frontmatter, flags=re.MULTILINE):
        errors.append(
            f"{repo_relative(path)}: missing frontmatter description field"
        )
    if not body.startswith('# '):
        errors.append(
            f"{repo_relative(path)}: missing top-level heading after frontmatter"
        )
    errors.extend(validate_skill_name(path, frontmatter))

    return errors


def validate_markdown_plain_formatting(path: Path) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding='utf-8').splitlines()
    in_fence = False
    fence_marker = ''
    frontmatter_end_line: int | None = None

    if lines and lines[0] == '---':
        for line_number, line in enumerate(lines[1:], start=2):
            if line == '---':
                frontmatter_end_line = line_number
                break

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith(('```', '~~~')):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ''
            continue

        if in_fence or stripped != '---':
            if in_fence:
                continue
            if EMOJI_PATTERN.search(line):
                errors.append(f"{repo_relative(path)}:{line_number}: emoji character")
            if DECORATIVE_SEPARATOR_PATTERN.fullmatch(stripped):
                errors.append(f"{repo_relative(path)}:{line_number}: decorative separator")
            continue

        if line_number == 1 or line_number == frontmatter_end_line:
            continue

        errors.append(f"{repo_relative(path)}:{line_number}: decorative horizontal rule")

    return errors


def validate_reusable_asset_portability(path: Path) -> list[str]:
    if not is_reusable_asset(path):
        return []

    errors: list[str] = []
    lines = path.read_text(encoding='utf-8').splitlines()
    for line_number, line in enumerate(lines, start=1):
        for pattern in REPO_SPECIFIC_REFERENCE_PATTERNS:
            if pattern.search(line):
                errors.append(
                    f"{repo_relative(path)}:{line_number}: "
                    f"repo-specific reference in reusable asset: {pattern.pattern}"
                )
    return errors


def extract_repo_inventory_paths(readme_text: str) -> list[str]:
    paths: list[str] = []
    allowed_prefixes = ('python/', 'shared/', 'tools/', 'docs/', '.clinerules/')
    allowed_exact = {'README.md', 'Makefile', '.pre-commit-config.yaml'}
    in_inventory = False
    for line in readme_text.splitlines():
        if line.startswith('## Repository-specific inventory'):
            in_inventory = True
            continue
        if in_inventory and line.startswith('## '):
            break
        if not in_inventory:
            continue
        for match in re.findall(r'`([^`]+)`', line):
            if match.startswith('docs/adr/'):
                continue
            if match in allowed_exact or match.startswith(allowed_prefixes):
                paths.append(match)
    return paths


def validate_readme_paths() -> list[str]:
    errors: list[str] = []
    readme_text = README_PATH.read_text(encoding='utf-8')
    for relative_path in extract_repo_inventory_paths(readme_text):
        if not (REPO_ROOT / relative_path).exists():
            errors.append(f"README.md: referenced path does not exist: {relative_path}")
    return errors


def main() -> int:
    errors: list[str] = []

    for skill_file in iter_skill_files():
        errors.extend(validate_skill_file(skill_file))

    for markdown_file in iter_markdown_files():
        errors.extend(validate_markdown_plain_formatting(markdown_file))
        errors.extend(validate_reusable_asset_portability(markdown_file))

    errors.extend(validate_readme_paths())

    if errors:
        for error in errors:
            print(error)
        return 1

    print('Repository validation passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
