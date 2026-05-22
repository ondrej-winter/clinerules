# Required format for skill files

This is a repo-specific maintenance rule for `SKILL.md` files maintained in this repository's skill roots. The skill files themselves should remain reusable unless explicitly marked otherwise.

This rule is the authoritative local copy of the Agent Skills specification for this repository.

## Core rule

- A skill is a directory containing, at minimum, a `SKILL.md` file.
- `SKILL.md` must start with YAML frontmatter at the first line of the file, followed by Markdown content.
- The frontmatter must include `name` and `description` fields.
- The frontmatter may include the optional Agent Skills fields `license`, `compatibility`, `metadata`, and `allowed-tools`.
- Do not add frontmatter fields outside the Agent Skills specification unless repository tooling or another external skill format requires them.
- The minimal frontmatter shape is:

```md
---
name: skill-name
description: Brief description of what this skill does and when to use it.
---
```

Optional fields may be added when they are useful:

```md
---
name: skill-name
description: Brief description of what this skill does and when to use it.
license: Apache-2.0
compatibility: Requires git and network access.
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(git:*) Read
---
```

## Frontmatter fields

- `name` is required.
  - Must be 1 to 64 characters.
  - May contain only lowercase letters, numbers, and hyphens.
  - Must not start or end with a hyphen.
  - Must not contain consecutive hyphens.
  - Must match the parent skill directory name.
- `description` is required.
  - Must be 1 to 1024 characters.
  - Must be non-empty.
  - Should describe both what the skill does and when to use it.
  - Should include specific keywords that help agents identify relevant tasks.
- `license` is optional.
  - Use a short license name or a reference to a bundled license file.
- `compatibility` is optional.
  - Must be 1 to 500 characters when provided.
  - Include it only when the skill has specific environment requirements.
  - It may describe the intended product, required system packages, network access needs, or similar constraints.
- `metadata` is optional.
  - Use it as an arbitrary key-value mapping for additional metadata.
  - Choose reasonably unique keys to avoid accidental conflicts.
- `allowed-tools` is optional.
  - Use a space-separated string of pre-approved tools the skill may use.
  - Treat this field as experimental because support may vary between agent implementations.

## Required structure

- A skill directory must contain `SKILL.md`.
- A skill directory may contain optional `scripts/`, `references/`, and `assets/` directories.
- After the frontmatter, the file must include one top-level heading that names the skill.
- The frontmatter `name` must match the skill directory name.
- The top-level heading should be the human-readable skill name.
- The body must include clear instructions for when and how the skill should be used.
- Use section headings only when they improve navigation.
- Use `## Steps` for procedural sequences when the skill describes a repeatable workflow.
- Add context, references, or advanced sections only when they make the skill easier to use.

Example structure:

```md
---
name: skill-name
description: Brief description of what this skill does and when to use it.
---

# Skill Name

Detailed instructions for Cline to follow when this skill is activated.

## Steps

1. First, do this
2. Then do that
3. For advanced usage, see [the reference guide](references/REFERENCE.md)
```

## Optional directories

- `scripts/` contains executable code that agents can run.
  - Scripts should be self-contained or clearly document dependencies.
  - Scripts should include helpful error messages.
  - Scripts should handle edge cases gracefully.
- `references/` contains additional focused documentation that agents can read when needed.
  - Keep individual reference files focused because agents load them on demand.
- `assets/` contains static resources such as templates, images, data files, lookup tables, and schemas.

## Authoring guidance

- Keep skill names short, descriptive, and kebab-case.
- Write descriptions so they explain both what the skill does and when to use it.
- Keep skill instructions self-contained unless the skill intentionally links to files that are part of the reusable asset.
- Prefer plain markdown with simple headings, lists, and code fences.
- Keep examples generic and portable. Use placeholders instead of repository-local names when the skill is intended for reuse.
- Keep the main `SKILL.md` concise. As a practical target, keep it under 500 lines.
- Move detailed reference material to focused files in `references/`.
- Use relative paths from the skill root when referencing other files.
- Keep file references one level deep from `SKILL.md` where practical.
- Avoid deeply nested reference chains.

## Progressive disclosure

Structure skills so agents load only the detail they need:

1. Metadata is loaded at startup for all skills and consists mainly of `name` and `description`.
2. Instructions are the Markdown body of `SKILL.md` and are loaded when the skill is activated.
3. Resources in `scripts/`, `references/`, and `assets/` are loaded only when needed.

## Review guidance

- Treat missing frontmatter as a defect.
- Treat missing `name` or `description` fields as a defect.
- Treat invalid `name`, `description`, `compatibility`, `metadata`, or `allowed-tools` fields as defects according to this rule.
- Treat skill files that do not provide a clear heading and actionable instructions as incomplete.
- Confirm the frontmatter `name` matches the skill directory name for repository skill roots.
- Confirm optional frontmatter fields match the Agent Skills specification.
- Confirm file references are relative to the skill root and avoid unnecessary nesting.
- Run `python3 tools/validate_repo.py` after changing skill files.
- When the external Agent Skills reference validator is available, use `skills-ref validate ./my-skill` to check frontmatter and naming conventions for an individual skill.
