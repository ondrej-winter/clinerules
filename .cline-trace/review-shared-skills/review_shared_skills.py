from pathlib import Path
import re


def strip_fenced_blocks(text: str) -> str:
    lines = []
    in_fence = False
    for line in text.splitlines():
        if line.startswith('```'):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return '\n'.join(lines)


for skill_path in sorted(Path('shared/agents/skills').glob('*/SKILL.md')):
    text = skill_path.read_text()
    stripped = strip_fenced_blocks(text)
    name = re.search(r'^name: (.+)$', text, re.M)
    description = re.search(r'^description: (.+)$', text, re.M)
    metadata = bool(re.search(r"^metadata:\n  version: \"[^\"]+\"", text, re.M))
    top_level_headings = re.findall(r'^# (.+)$', stripped, re.M)

    issues = []
    if not name or name.group(1) != skill_path.parent.name:
        issues.append('name')
    if not description or not description.group(1).strip():
        issues.append('description')
    if not metadata:
        issues.append('metadata')
    if len(top_level_headings) != 1:
        issues.append(f"h1={len(top_level_headings)}")

    status = 'OK' if not issues else '; '.join(issues)
    print(f"{skill_path.parent.name}: {status}")
