# Cline SDLC Orchestrator

## Status

- Artifact type: discovery brief
- Date: 2026-07-22
- Decision state: not yet an approved specification or implementation plan
- Intended scope: portable Cline tooling, not a Ritebook feature

## Problem Statement

How might we automate a software development lifecycle through the Cline
ecosystem—from a rough idea, idea file, specification file, or implementation
plan file through the remaining lifecycle stages—while retaining human control
at important product, execution, and risk boundaries?

The individual development procedures already exist as Agent Skills, but the
user currently has to invoke and coordinate each stage. Progress, approval,
review iterations, failure handling, and resumption are not governed by one
explicit lifecycle contract.

## Desired User Experience

A user should provide exactly one of these inputs:

- a rough idea supplied directly in the request;
- a path to an idea file;
- a path to a specification file;
- a path to an implementation plan file.

The orchestrator should inspect the supplied input, determine the earliest
incomplete lifecycle stage, and create only the missing downstream artifacts. A
partially implemented plan uses the implementation plan file as its input; its
recorded lifecycle and progress state determines where implementation resumes.

The intended lifecycle is:

```text
Idea
  -> Refine direction
  -> Create specification
  -> Human accepts specification
  -> Create implementation plan
  -> Independent plan review
  -> Revise and re-review plan
  -> Human approves execution
  -> Implement next vertical slice
  -> Test and verify slice
  -> Record progress
  -> Continue with next ready slice
  -> Final quality gate and review
```

The workflow should be resumable after a context reset, new Cline task, editor
restart, or temporary failure.

## Established Findings

### Existing skills cover the individual stages

The current skill ecosystem contains focused procedures for:

- `idea-refine`;
- `spec-driven-development`;
- `planning-and-task-breakdown`;
- `review-implementation-plan`;
- `incremental-implementation`;
- `test-driven-development`;
- `run-local-quality-gate`;
- code review, security, documentation, and other specialist concerns.

The missing capability is primarily lifecycle coordination, durable progress
state, approval policy, bounded review and recovery, and resumption. An
orchestrator should compose existing skills rather than duplicate their detailed
procedures.

### Cline Skills can provide an interactive entry point

Enabled Cline Skills can be triggered from chat as slash commands. A portable
skill could expose an entry point such as `/sdlc`.

A Skill is appropriate for interactive workflow guidance, selecting stage skills,
inspecting artifacts, deciding the next lifecycle stage, requesting approvals,
and resuming from repository-visible state. A Skill is prompt-driven guidance,
however; it is not by itself a deterministic workflow engine.

### Plan and Act modes form a lifecycle boundary

Plan mode supports repository inspection and strategy without modifying files.
Act mode permits implementation and command execution.

The orchestrator should respect this distinction:

- idea refinement, specification, planning, and plan review belong primarily in
  Plan mode;
- implementation belongs in Act mode;
- unexpected discoveries may require returning to Plan mode;
- entering implementation remains an explicit human decision in interactive
  Cline usage.

Act mode must not automatically authorize destructive, irreversible,
credential-sensitive, publishing, release, or deployment operations.

### Read-only subagents can provide independent plan review

Cline subagents receive separate context windows, can inspect files and use
skills, cannot modify files, and return focused reports to the main agent. This
makes a subagent suitable for fresh-context plan review.

The reviewer should receive the accepted specification, proposed plan, relevant
repository rules and files, explicit failure modes, and a required findings
format. It should not receive the plan author's complete reasoning because that
would bias the review toward agreement.

### Checkpoints are rollback safety, not workflow state

Cline Checkpoints snapshot project state during edits and commands and can persist
across editor sessions. They are valuable during implementation, but they should
not be authoritative SDLC state because they do not express specification
acceptance, plan readiness, approval scope, or portable progress metadata.

The workflow therefore needs repository-visible artifacts in addition to Cline
Checkpoints.

### Cline CLI supports automation

Cline CLI supports Plan and Act execution, headless runs, newline-delimited JSON
output, timeouts, retry limits, shell-command restrictions, auto-approval,
session resumption with `--id`, and isolated data directories.

These features could support automated orchestration outside an interactive IDE
session. Full auto-approval should be used only in a trusted or sandboxed
environment.

### Cline SDK supports policy-based approval

The Cline SDK can auto-approve read-only operations, require approval for writes
and commands, disable tools, make approval conditional on an operation, and
expose approval requests through a custom interface.

It is the strongest available foundation if the product requires deterministic
human-in-the-loop policies rather than prompt-only conventions.

### Agent Teams provide persistent coordination with overhead

Cline Agent Teams are available through the CLI, SDK, and Kanban, but not current
VS Code and JetBrains extensions. Team state includes a task board, mailbox, and
mission log and can persist across sessions.

Teams may help with large multi-agent implementations, but are probably
unnecessary initially because the lifecycle is mostly sequential. Read-only
subagents should be sufficient for independent plan review. Teams should be
considered only when tasks are genuinely independent or teammates need to
communicate with one another.

## Candidate Product Directions

### Direction B: Standalone Cline SDK Orchestrator

Build a standalone tool that owns lifecycle transitions, stage prompts, Cline
sessions, approval callbacks, review limits, permissions, logs, and recovery. A
Cline Skill could remain its interactive front end.

Advantages:

- explicit state machine;
- deterministic gates and retry behavior;
- interactive and headless execution;
- stronger auditability;
- foundation for later integrations.

Limitations:

- materially larger implementation;
- requires runtime and packaging decisions;
- must manage SDK compatibility, authentication, models, security, and recovery.

### Direction C: Thin Cline CLI Wrapper

Implement a process orchestrator around repeated Cline CLI invocations using JSON
output, session identifiers, retry limits, and repository-visible state.

Advantages:

- simpler than a complete SDK application;
- suitable for a proof of concept;
- uses existing CLI automation capabilities.

Limitations:

- parsing agent output is less reliable than typed SDK events;
- approval handling is less flexible;
- lifecycle state still needs a separate implementation;
- subprocess and session recovery can become complicated.

### Direction D: Agent Team Coordinator

Use a persistent Agent Team where a coordinator delegates plan review and
implementation tasks.

Advantages:

- persistent task board and mission history;
- natural multi-session support;
- specialist agents can own isolated tasks.

Limitations:

- unavailable in current IDE extensions;
- excessive overhead for a mostly sequential lifecycle;
- concurrent writers require repository isolation;
- product-level approval and artifact contracts are still necessary.

## Preliminary Recommendation

Choose between Direction B and Direction C based on the required approval model
and runtime guarantees. Prefer the SDK orchestrator when deterministic approval
policy and typed lifecycle events are required. Use a thin CLI wrapper only as a
bounded proof of concept when process orchestration is sufficient.

In either case, use the repository-visible artifacts and lifecycle contract
defined in this brief as the initial contract. Validate it on real work before
encoding it as rigid runtime behavior.

```text
Phase 1: Validate the lifecycle artifact and state contract
  -> exercise the four inputs, transitions, approvals, and resumption on real work
Phase 2: CLI proof of concept or SDK state-machine runner
  -> enforce transitions, approvals, and resumption
Phase 3: Optional CI, scheduling, or Agent Team integration
```

This recommendation is provisional. Unattended cross-session execution or strict
approval guarantees would favor the SDK orchestrator as the first version.

## Default Human-in-the-Loop Policy

The preferred default is a balanced policy.

### Human approval required

- confirm the refined direction when idea refinement is used;
- accept the specification before planning depends on it;
- approve the final reviewed plan before implementation;
- approve destructive, irreversible, credential-sensitive, publishing,
  deployment, or newly discovered high-risk operations;
- approve material revisions to an already approved plan.

### Automatic after plan approval

- select the next ready implementation slice;
- implement the slice;
- run focused tests and checks;
- update progress and validation evidence;
- proceed to the next low-risk slice;
- run checkpoints and the final quality gate.

### Stop conditions

Automation stops when:

- ambiguity changes behavior or scope;
- implementation contradicts the accepted specification;
- a material plan revision is required;
- a new architecture, schema, security, migration, dependency, or compatibility
  decision is discovered;
- destructive or external side effects are proposed;
- repository state conflicts with recorded state;
- validation repeatedly fails;
- review or recovery limits are exhausted;
- required context or skills are unavailable.

Possible later profiles are `supervised`, `balanced`, and `mostly-autonomous`.
The first version may support only `balanced` to avoid premature configuration.

## Artifact and State Direction

The host repository should contain portable, human-reviewable artifacts:

- an idea brief when refinement is necessary;
- a specification;
- an implementation plan;
- plan-review findings;
- lifecycle status and validation evidence.

These artifacts also define the file-based inputs. An idea file, specification
file, or implementation plan file enters the lifecycle at its corresponding
stage. A rough idea is the only non-file input and produces an idea brief before
the workflow continues. Existing host-repository conventions should determine
artifact locations when available.

One possible layout is:

```text
docs/
  ideas/<work-name>.md
  specs/<work-name>-spec.md
  plans/<work-name>-plan.md
```

The plan could initially contain lifecycle state so a separate state file is not
required:

```yaml
profile: balanced
phase: implementing
specification: docs/specs/example-spec.md
plan_revision: 2
review_iteration: 2
review_readiness: ready
current_task: task-3
current_slice: slice-3.1
last_verified_checkpoint: checkpoint-a
blocker: null
```

This is conceptual, not a settled schema.

## Review and Revision Direction

Plan review should use a bounded loop:

1. Create plan revision 1.
2. Review it in a separate read-only context.
3. Record findings with stable identifiers, severity, evidence, and required
   correction.
4. Revise the plan.
5. Re-review material changes in a fresh context.
6. Stop after the initial review plus at most two revision and re-review cycles.

If the plan is still not ready, mark the lifecycle blocked and request human
resolution. The tool must not silently waive findings or review itself
indefinitely.

## Approval Validity Direction

Review and approval should apply to an exact plan revision.

Progress-only updates should not invalidate approval:

- completed task checkboxes;
- validation evidence;
- timestamps;
- implementation notes;
- current-slice updates.

Material changes should invalidate approval:

- scope or non-goal changes;
- altered acceptance criteria;
- new dependencies;
- changed contracts or schemas;
- architecture or security decisions;
- migration or compatibility behavior;
- significant sequencing changes;
- newly discovered high-impact risks.

A persisted approval note is audit evidence, but should not automatically
authorize execution in a new session when the exact approval cannot be
established.

## Resumption Direction

On resume, the orchestrator should:

1. read the specification, plan, lifecycle state, and repository status;
2. reconcile recorded progress with the working tree;
3. identify the earliest incomplete task with completed dependencies;
4. resume a partial slice before starting another;
5. verify checked tasks against code or validation evidence;
6. invalidate approval when material divergence is found;
7. preserve unrelated human changes;
8. stop when ownership of existing changes is unclear.

Session identifiers and Checkpoints may assist recovery, but repository artifacts
should remain the portable source of truth.

## Key Assumptions to Validate

- [ ] Markdown state is sufficient for cross-session resume. Resume the same work
      from a fresh Cline session.
- [ ] A read-only subagent produces a meaningfully independent plan review.
      Compare it with same-context review.
- [ ] The balanced profile avoids excessive interruptions without allowing silent
      scope drift.
- [ ] Existing specialist skills have stable enough inputs and outputs for
      composition.
- [ ] Cline can continue across at least three low-risk slices without losing task
      boundaries.
- [ ] Material plan changes can be distinguished consistently from progress-only
      updates.
- [ ] The lifecycle remains useful across different languages and architectures.

## MVP Scope

The smallest useful MVP should:

- expose one orchestrator entry point;
- accept exactly one rough idea, idea file, specification file, or implementation
  plan file;
- infer resumption of partially completed work from state recorded with the plan;
- use existing stage-specific skills;
- support the balanced approval policy;
- perform independent plan review and a bounded revision loop;
- implement one slice at a time;
- discover and run project-specific validation;
- update repository-visible progress;
- stop safely on risk, drift, or failure;
- resume from recorded state.

The MVP should first be exercised on a small non-production example before it is
trusted for unattended changes.

## Not Doing and Why

- Ritebook integration or publication — this is a general Cline SDLC tool.
- Automatic commits, pushes, pull requests, releases, or deployments — these
  require separate authorization.
- A generic multi-agent organization — the mostly sequential lifecycle does not
  initially justify Agent Team complexity.
- A database-backed service — repository-visible artifacts should be tested first.
- Arbitrary approval profiles — start with balanced behavior.
- Unbounded autonomous repair — repeated failure becomes a blocker.
- Mandatory hexagonal architecture — follow the host repository's architecture.
- Replacing specialist skills — coordinate them instead.
- Treating Checkpoints as authoritative state — they are a rollback mechanism.
- CI/CD or issue-tracker integration in the MVP — validate the core lifecycle
  first.
- Fully unattended operation in an untrusted workspace — auto-approved tools can
  modify files and execute commands.

## Open Questions

### Product boundary

- Is the first standalone version an SDK application or a thin CLI wrapper?
- Must the MVP run unattended across multiple sessions?
- Is IDE support required, or is CLI/TUI sufficient initially?
- Is the tool intended for a solo developer, a team, or both?
- Does the lifecycle end after implementation and validation, or also include
  review, merge, release, and deployment?

### Runtime and packaging

- If a standalone runtime is needed, should it use the SDK or wrap the CLI?
- Where should the standalone tool be maintained?
- How should it be installed and updated?
- Should distribution expose or hide a Node.js dependency?
- Which Cline and SDK versions should be supported?

### State and artifacts

- Should state live in the plan or `.cline/sdlc/<work-id>/state.yaml`?
- Which artifacts should be committed?
- How are concurrent work items identified?
- How should revisions or digests be computed?
- How should stale or manually edited state be detected?
- How should existing repository spec and plan conventions be respected?

### Human approval

- What exact user action counts as approval?
- Can approval remain valid across sessions?
- Are plan approval and Plan-to-Act transition one combined decision?
- Which operations always require approval?
- Are dependency, schema, migration, architecture, and security changes always
  risk gates?
- How should approval work in headless mode?

### Plan review

- Does every plan require independent review or only complex plans?
- Is one read-only subagent sufficient?
- Should every re-review use a new subagent?
- What findings schema and readiness labels should be used?
- Should implementation receive a fresh-context review before completion?

### Implementation loop

- What is the maximum slice size?
- Should all approved slices run in one session when context permits?
- When should `/newtask` create a clean continuation task?
- Does validation run after every slice, checkpoint, or both?
- How many automatic repair attempts are allowed?
- Are commits optional checkpoints or entirely outside the orchestrator?

### Safety and isolation

- Must autonomous work use a sandbox, container, worktree, or clean branch?
- Which commands are denied by default?
- How are network operations handled?
- How are unrelated working-tree changes detected and preserved?
- Should protected branches be rejected?
- What rollback guarantees are required beyond Checkpoints?

### Multi-agent behavior

- Are subagents limited to read-only reviews?
- When should Agent Teams implement independent slices?
- Must multiple writers use separate Git worktrees?
- How are independently implemented slices integrated and revalidated?

### Success criteria

- What observable result proves the MVP useful?
- How much manual coordination should it eliminate?
- Which completion, intervention, failure, and rollback metrics are needed?
- How many real workflows should run before investing in an SDK runner?

## Research Basis

These findings were checked against Cline documentation available on 2026-07-22:

- [Skills](https://docs.cline.bot/customization/skills)
- [Using Commands](https://docs.cline.bot/core-workflows/using-commands)
- [Plan and Act Mode](https://docs.cline.bot/core-workflows/plan-and-act)
- [Checkpoints](https://docs.cline.bot/core-workflows/checkpoints)
- [Subagents](https://docs.cline.bot/features/subagents)
- [CLI Overview](https://docs.cline.bot/usage/cli-overview)
- [CLI Reference](https://docs.cline.bot/cli/cli-reference)
- [Agent Teams](https://docs.cline.bot/cli/agent-teams)
- [SDK Permission Handling](https://docs.cline.bot/sdk/guides/permission-handling)
- [SDK Multi-Agent Teams](https://docs.cline.bot/sdk/guides/multi-agent-teams)

## Next Decision

Choose the first delivery direction:

1. standalone Cline SDK orchestrator;
2. thin Cline CLI wrapper.

After that decision, convert this brief into a specification with concrete
acceptance criteria. Create an implementation plan only after the specification
has been reviewed and accepted.
