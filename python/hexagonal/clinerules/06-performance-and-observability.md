# Performance and observability: budgets, profiling, tracing, logging, metrics

Use these rules to keep performance regressions visible and runtime behavior traceable.

## Performance budgets and baselines
- **Should** define latency/throughput/error-budget expectations for user-facing or operationally critical workflows.
- **Must** benchmark representative workloads before claiming a performance improvement on a hot path.
- **Should** avoid introducing heavy dependencies without profiling evidence.

## Profiling expectations
- **Should** profile when changing hot paths (external API calls, parsing, persistence).
- **Must** capture before/after numbers when optimizing.
- **Should** note the dataset/environment when numbers drive a decision.
- **Should** prefer targeted micro-benchmarks for isolated code and end-to-end timings for workflow claims.

## Logging, tracing, and metrics
- **Should** add metrics for long-running steps (parsing, external API calls, rendering, persistence).
- **Should** use tracing spans around external I/O (external APIs, filesystem, databases, message queues).
- **Must** keep metric labels/tags low-cardinality; avoid user IDs, raw queries, full file paths, or other highly variable values as labels.
- **Should** propagate request, correlation, or job IDs across adapter boundaries when available.
- Align logging field names and metric dimensions with `11-logging-conventions.md`.

## Operational notes
- **Should** add troubleshooting notes when new failure modes are introduced.
- **Should** document dashboards, alerts, or runbook hooks for new critical paths when they exist.
- **Must** document new observability hooks in the README or ADRs.
