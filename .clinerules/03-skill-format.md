# Required format for skill files

Reusable skill files in this repository must use a consistent markdown format.

## Core rule

- Every skill file must start with YAML frontmatter.
- The frontmatter must use this shape:

```md
---
name: my-skill
description: Brief description of what this skill does and when to use it.
---
```

## Required structure

- After the frontmatter, the file must include a top-level heading that names the skill.
- The body must include clear instructions for when and how the skill should be used.
- Use section headings only when they improve navigation.
- Use `## Steps` when the skill contains a procedural sequence.

Example structure:

```md
---
name: my-skill
description: Brief description of what this skill does and when to use it.
---

# My Skill

Detailed instructions for Cline to follow when this skill is activated.

## Steps
1. First, do this
2. Then do that
3. For advanced usage, see [advanced.md](docs/advanced.md)
```

## Authoring guidance

- Keep skill names short, descriptive, and kebab-case.
- Write descriptions so they explain both what the skill does and when to use it.
- Keep skill instructions self-contained unless the skill intentionally links to files that are part of the reusable asset.
- Prefer plain markdown with simple headings, lists, and code fences.

## Review guidance

- Treat missing frontmatter as a defect.
- Treat missing `name` or `description` fields as a defect.
- Treat skill files that do not provide a clear heading and actionable instructions as incomplete.
