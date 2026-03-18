# Built-in Slash Commands

Quick reference for Cline slash commands.

---

## `/newtask`
Starts a fresh Cline task in a new context window, clearing the current conversation history.

**Use when:** The current task is complete and you want to start something unrelated, or when the context window is getting full and you need a clean slate.

---

## `/smol`
Compacts the current conversation by summarising it, reducing token usage while preserving key context.

**Use when:** You're mid-task and the context window is running low, but you don't want to abandon the current task with `/newtask`.

---

## `/newrule`
Creates a new `.clinerules` file (or entry) for the current project to guide Cline's behaviour.

**Use when:** You want to encode a convention, constraint, or workflow preference so Cline follows it automatically in future tasks in this repo.

---

## `/deep-planning`
Switches Cline into an extended planning mode, producing a detailed plan before writing any code.

**Use when:** The task is complex, cross-cutting, or carries significant risk — and you want to review a full plan before Cline starts making changes.

---

## `/explain-changes`
Generates a human-readable explanation of recent code changes, annotated inline on the diff.

**Use when:** You've just received a PR, completed a refactor, or want to document what changed before merging or reviewing with a colleague.

---

## `/reportbug`
Opens a bug report flow to capture unexpected Cline behaviour and submit it for review.

**Use when:** Cline produces wrong output, crashes, misunderstands a command, or behaves in a way that seems like a defect rather than a model limitation.
