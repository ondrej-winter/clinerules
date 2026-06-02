# Shared Agent Skills Authoring Track

This track file records the plan to review and improve every skill under
`shared/agents/skills/` using the guidance in
`shared/agents/skills/author-agent-skill/SKILL.md`.

Scope for this track:

- Review each shared skill directory as a complete reusable Agent Skill.
- Address both `SKILL.md` authoring quality and optional support-file structure.
- Check whether `scripts/`, `references/`, and `assets/` are used only when they
  improve progressive disclosure or provide necessary reusable material.
- Review templates, examples, schemas, static files, and helper scripts for
  portability before editing individual skills.
- Record remediation needs before editing any individual skill.
- Keep this file as the coordination point for future skill-authoring work.
- Do not treat this file as evidence that a skill has already been fixed.

## Review criteria

For each skill, check these criteria from `author-agent-skill` and the local skill
format rules.

### Metadata and main file

- `SKILL.md` exists in the skill directory.
- Frontmatter starts at the first line.
- Frontmatter includes `name`, `description`, and `metadata.version`.
- `name` matches the parent directory exactly.
- `name` is valid kebab-case.
- `description` explains both what the skill does and when to use it.
- `metadata.version` is present, quoted, and increased when the skill changed.
- Unsupported frontmatter fields are absent.
- Supported optional frontmatter fields are correctly shaped and necessary.
- Exactly one top-level heading follows the frontmatter.
- Instructions explain when and how to use the skill.
- Formatting is plain and free of decorative noise.

### Skill directory structure

- The skill directory contains `SKILL.md` and only necessary optional support
  directories.
- Optional support directories use the expected names: `scripts/`, `references/`,
  and `assets/`.
- Optional support directories are not empty.
- Support files are referenced from `SKILL.md` when an agent needs to know they
  exist.
- File references are relative to the skill root and avoid unnecessary nesting.
- Detailed or rarely used material is moved out of `SKILL.md` only when that
  improves progressive disclosure.
- Short guidance remains in `SKILL.md` instead of being split into support files
  only to mirror a convention.

### Assets, templates, and examples

- Templates, static examples, schemas, configuration samples, and reusable snippets
  live under `assets/` when they are meant to be copied, adapted, or inserted.
- Asset filenames make their purpose clear, such as `*.template.*` for templates
  when that convention helps avoid confusion with active project files.
- Template placeholders are generic, explicit, and portable, such as
  `<package_name>`, `<app_name>`, `<repo_name>`, and `<python_version>`.
- Assets avoid repository-local paths, private project names, local usernames, and
  commands that only make sense in this repository unless clearly marked as
  repo-specific.
- Examples are minimal and focused on the skill behavior.
- Assets are not duplicated across skills unless duplication is intentional and
  keeps each skill drop-in portable.

### References

- Focused supporting documentation lives under `references/` when it would make
  `SKILL.md` too long or too detailed.
- Reference files are scoped to one topic or checklist.
- `SKILL.md` explains when to consult each reference file.
- Reference chains are shallow enough that an agent can find the necessary detail
  without loading many files.
- Reference content remains portable unless a repo-specific section is clearly
  labeled.

### Scripts

- Executable helper code lives under `scripts/` only when a repeatable command or
  automation materially helps the skill.
- Scripts are self-contained or document their dependencies.
- Scripts include helpful error messages and handle common edge cases.
- Script names describe the action they perform.
- Scripts do not require hidden local state, repository-specific paths, or
  interactive prompts unless the skill explicitly documents that requirement.
- Any script invocation in `SKILL.md` uses a relative path from the skill root and
  explains expected inputs and outputs.

### Portability and validation

- Reusable skills can be copied into another compatible repository without path
  rewrites tied to this repository.
- Repo-specific exceptions are clearly labeled and are necessary.
- Validation was run or any skipped validation is documented.
- Completed remediation notes include the changed files and validation evidence.

## Work sequence

Use this sequence when addressing each skill:

1. Read the skill's `SKILL.md` and inventory optional support files.
2. Classify support files as `scripts/`, `references/`, `assets/`, or misplaced.
3. Compare the main skill file and support files against the review criteria above.
4. Record required actions in the tracking table before editing.
5. Make the smallest targeted skill update needed.
6. Run the narrowest useful validation.
7. Update this track file with completion and validation notes.

## Tracking table

Use `Not reviewed`, `Needs work`, `Completed`, or `Not applicable` for status
columns. Keep required actions specific enough that another maintainer can resume
the work without redoing the review.

| Skill                          | Structure | Assets and templates | References     | Scripts        | Required actions                                                                                                                                                               | Validation                                                               |
| ------------------------------ | --------- | -------------------- | -------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `add-observability`            | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `api-and-interface-design`     | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `author-agent-skill`           | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `browser-runtime-verification` | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `ci-cd-and-automation`         | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `code-review-and-quality`      | Completed | Not applicable       | Completed      | Not applicable | No changes needed; reference checklists are focused, portable, and referenced from `SKILL.md`                                                                                  | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `code-simplification`          | Completed | Not applicable       | Not applicable | Not applicable | Removed decorative attribution blockquote from `SKILL.md`; no support files needed                                                                                             | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `context-engineering`          | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `debugging-and-error-recovery` | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `deprecation-and-migration`    | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `documentation-and-adrs`       | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `doubt-driven-development`     | Completed | Not applicable       | Completed      | Not applicable | Replaced unsafe heredoc/echo prompt guidance with file-based stdin guidance; orchestration reference is focused, portable, and referenced from `SKILL.md`                      | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `frontend-ui-engineering`      | Completed | Not applicable       | Completed      | Not applicable | No changes needed; accessibility reference is focused, portable, and referenced from `SKILL.md`                                                                                | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `git-workflow-and-versioning`  | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `idea-refine`                  | Completed | Not applicable       | Completed      | Completed      | No changes needed; references are focused and portable, and helper script is referenced from `SKILL.md` with clear purpose                                                     | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `incremental-implementation`   | Completed | Not applicable       | Not applicable | Not applicable | Replaced decorative diagram and symbolic markers in `SKILL.md` with plain text; no support files needed                                                                        | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `interview-me`                 | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `performance-optimization`     | Completed | Not applicable       | Completed      | Not applicable | Replaced decorative workflow/tree notation in `SKILL.md` with plain text; performance reference is focused, portable, and referenced from `SKILL.md`                           | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `planning-and-task-breakdown`  | Completed | Not applicable       | Not applicable | Not applicable | Replaced decorative dependency diagram and dash placeholder in `SKILL.md` with plain text; no support files needed                                                             | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `review-implementation-plan`   | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `run-local-quality-gate`       | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `security-and-hardening`       | Completed | Not applicable       | Completed      | Not applicable | Replaced decorative audit and secrets diagrams in `SKILL.md` with plain text; security reference is focused, portable, and referenced from `SKILL.md`                          | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `shipping-and-launch`          | Completed | Not applicable       | Completed      | Not applicable | Replaced decorative rollout and monitoring diagrams in `SKILL.md` with plain text; launch references are focused, portable, and referenced from `SKILL.md`                     | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `source-driven-development`    | Completed | Not applicable       | Not applicable | Not applicable | Replaced decorative process diagram and prompt markers in `SKILL.md` with plain text; no support files needed                                                                  | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `spec-driven-development`      | Completed | Not applicable       | Not applicable | Not applicable | Replaced decorative workflow diagram, path mapping markers, and prompt markers in `SKILL.md` with plain text; no support files needed                                          | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `test-driven-development`      | Completed | Not applicable       | Completed      | Not applicable | Replaced decorative TDD, bug-fix, test-pyramid, and test-choice diagrams in `SKILL.md` with plain text; testing reference is focused, portable, and referenced from `SKILL.md` | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `update-project-docs`          | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `using-agent-skills`           | Completed | Not applicable       | Not applicable | Not applicable | Replaced decorative skill-discovery diagram, lifecycle arrows, and prompt markers in `SKILL.md` with plain text; no support files needed                                       | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |
| `write-adr`                    | Completed | Not applicable       | Not applicable | Not applicable | No changes needed; `SKILL.md` only and structure is portable                                                                                                                   | `python3 tools/validate_repo.py`, sync check, and `make validate` passed |

## Handoff checklist

- [x] Every shared skill directory has been structurally reviewed.
- [x] Required actions are recorded for every reviewed skill.
- [x] Misplaced or unnecessary support files have been addressed.
- [x] Template and asset portability has been checked.
- [x] Completed remediations are marked in the tracking table.
- [x] Validation evidence is recorded for every completed remediation.
- [x] Repository validation has been run before final handoff.
