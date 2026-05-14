# Drop-in portability for reusable assets

This repository maintains reusable skills, rules, workflows, and supporting guidance. Root `.clinerules/` files are repo-specific maintenance rules for that content.

By default, reusable assets in this repository must remain drop-in portable unless a file or section is explicitly marked as repo-specific.

## Core rule

- Reusable assets under content roots such as `shared/` and `python/` **must** be copyable into another repository without path rewrites tied to this repository's local structure.

## What this applies to

- Skills under reusable content directories
- Reusable rulesets and workflows
- Templates, examples, and bootstrap guidance intended for reuse

## Required authoring behavior

- **Must** avoid references to this repository's internal paths, folder names, or layout inside reusable content.
- **Must** use generic placeholders such as `<package_name>`, `<app_name>`, `<repo_name>`, and `<python_version>` instead of local project identifiers.
- **Must** keep instructions self-contained so they still make sense when copied into another repository.
- **Should** describe conventions and expected outcomes in generic terms rather than anchoring them to this repository.
- **Should** keep reusable assets free of assumptions about adjacent files unless those files are part of the reusable asset itself.

## Repo-specific exceptions

- Repo-specific instructions are allowed only when they are clearly labeled as repo-specific.
- Repo-specific maintenance notes should live outside reusable assets whenever practical.
- If a reusable asset needs local context in this repository, that context should be documented separately rather than embedded into the reusable content.

## Review guidance

- When reviewing changes in this repository, check whether a supposedly reusable file can be copied into another repository without editing repository-local path references.
- If a file is intended to be portable, references to repository-local structure should be treated as a defect.
