# Required format for skill files

This is a repo-specific maintenance rule for `SKILL.md` files maintained in this repository's skill roots. The skill files themselves should remain reusable unless explicitly marked otherwise.

## Core rule

- Every `SKILL.md` file must start with YAML frontmatter at the first line of the file.
- The frontmatter must include `name` and `description` fields.
- Do not add other frontmatter fields unless repository tooling or an external skill format requires them.
- The frontmatter must use this shape:

```md
---
name: my-skill
description: Brief description of what this skill does and when to use it.
---
```

## Required structure

- After the frontmatter, the file must include one top-level heading that names the skill.
- The frontmatter `name` must be kebab-case and should match the skill directory name.
- The top-level heading should be the human-readable skill name.
- The body must include clear instructions for when and how the skill should be used.
- Use section headings only when they improve navigation.
- Use `## Steps` for procedural sequences when the skill describes a repeatable workflow.
- Add context, references, or advanced sections only when they make the skill easier to use.

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
- Keep examples generic and portable. Use placeholders instead of repository-local names when the skill is intended for reuse.

## Review guidance

- Treat missing frontmatter as a defect.
- Treat missing `name` or `description` fields as a defect.
- Treat skill files that do not provide a clear heading and actionable instructions as incomplete.
- Confirm the frontmatter `name` matches the skill directory name for repository skill roots.
- Run `python3 tools/validate_repo.py` after changing skill files.
