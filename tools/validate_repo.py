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


def iter_skill_files() -> list[Path]:
    files: list[Path] = []
    for root in SKILL_PATHS:
        if not root.exists():
            continue
        files.extend(sorted(root.glob('*/SKILL.md')))
    return files


def validate_skill_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding='utf-8')

    if not text.startswith('---\n'):
        return [f"{path.relative_to(REPO_ROOT)}: missing YAML frontmatter start"]

    parts = text.split('---\n', 2)
    if len(parts) < 3:
        return [f"{path.relative_to(REPO_ROOT)}: malformed YAML frontmatter"]

    frontmatter = parts[1]
    body = parts[2].lstrip('\n')

    if not re.search(r'^name:\s+.+$', frontmatter, flags=re.MULTILINE):
        errors.append(f"{path.relative_to(REPO_ROOT)}: missing frontmatter name field")
    if not re.search(r'^description:\s+.+$', frontmatter, flags=re.MULTILINE):
        errors.append(
            f"{path.relative_to(REPO_ROOT)}: missing frontmatter description field"
        )
    if not body.startswith('# '):
        errors.append(
            f"{path.relative_to(REPO_ROOT)}: missing top-level heading after frontmatter"
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

    errors.extend(validate_readme_paths())

    if errors:
        for error in errors:
            print(error)
        return 1

    print('Repository validation passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
