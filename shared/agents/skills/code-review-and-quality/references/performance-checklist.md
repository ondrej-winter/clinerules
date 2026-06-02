# Performance Review Checklist

Use this checklist when reviewing changes that affect request paths, rendering, database access, background work, caching, data volume, startup time, or bundle size.

## Checks

- Confirm hot paths avoid unnecessary network calls, database queries, file reads, and repeated computation.
- Confirm loops and joins scale with expected data volume rather than only sample data.
- Confirm caches have clear invalidation, bounds, and fallback behavior.
- Confirm frontend changes avoid unnecessary re-renders, oversized assets, and blocking work on the main thread.
- Confirm database changes use appropriate indexes and avoid N+1 query patterns.
- Confirm performance-sensitive changes include measurement or a documented rationale.

## Review prompts

- What is the expected input size, request rate, or user concurrency?
- Which operation is now on the critical path?
- What metric would show this change made performance worse?
- Is the performance trade-off intentional and documented?
