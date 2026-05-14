# Drop-in portability for reusable assets

This is a repo-specific maintenance rule for reusable assets maintained in this repository. Root `.clinerules/` files may reference repository-local paths because they describe how this repository is maintained.

By default, reusable assets in this repository must remain drop-in portable unless a file or section is explicitly marked as repo-specific.

## Core rule

- Reusable assets under `shared/` and `python/hexagonal/` must be copyable into another repository without path rewrites tied to this repository's local structure.
- Portable content must not depend on this repository's directory layout, tooling paths, or project name unless that dependency is part of the reusable asset itself.

## What this applies to

- Skills under reusable content directories
- Reusable rulesets and workflows
- Templates, examples, and bootstrap guidance intended for reuse
- Shared hooks and workflow files that are synced into target `.clinerules/` directories

## Required authoring behavior

- Must avoid references to repository-local maintenance paths such as `tools/`, `shared/`, `.clinerules/`, or `python/hexagonal/` inside portable content unless the section is explicitly repo-specific.
- Must use generic placeholders such as `<package_name>`, `<app_name>`, `<repo_name>`, and `<python_version>` instead of local project identifiers.
- Must keep instructions self-contained so they still make sense when copied into another repository.
- Should describe conventions and expected outcomes in generic terms rather than anchoring them to this repository.
- Should keep reusable assets free of assumptions about adjacent files unless those files are part of the reusable asset itself.

## Repo-specific exceptions

- Repo-specific instructions are allowed only when they are clearly labeled as repo-specific.
- Repo-specific maintenance notes should live outside reusable assets whenever practical.
- If a reusable asset needs local context in this repository, that context should be documented separately rather than embedded into the reusable content.
- Root `.clinerules/` files are repo-specific by design and may document local source-of-truth paths, sync targets, and validation commands.

## Synced-source workflow

- Treat files copied from `shared/` as derived targets.
- When a synced workflow or hook needs a change, edit the shared source first.
- After editing a shared source, run the sync check or sync command documented for this repository.
- Do not patch a synced target directly unless the change is intentionally local and the sync strategy is documented.

## Review guidance

- When reviewing changes in this repository, check whether a supposedly reusable file can be copied into another repository without editing repository-local path references.
- If a file is intended to be portable, references to repository-local structure should be treated as a defect.
- Confirm reusable content does not mention repository maintenance paths unless the relevant section is clearly marked repo-specific.
- Confirm synced targets still match their shared sources after any workflow or hook change.
