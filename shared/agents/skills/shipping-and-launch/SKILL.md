---
name: shipping-and-launch
description: Prepares production launches. Use when preparing to deploy to production. Use when you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy.
metadata:
  version: "1.1.0"
---

# Shipping and Launch

## Overview

Ship with confidence. The goal is not just to deploy — it's to deploy safely, with monitoring in place, a rollback plan ready, and a clear understanding of what success looks like. Every launch should be reversible, observable, and incremental.

## When to Use

- Deploying a feature to production for the first time
- Releasing a significant change to users
- Migrating data or infrastructure
- Opening a beta or early access program
- Any deployment that carries risk (all of them)

Use `add-observability` when launch readiness requires new logs, metrics, traces,
dashboards, alerts, or troubleshooting notes. Use `performance-optimization` when
launch readiness depends on diagnosing and fixing a performance bottleneck. Use
`debugging-and-error-recovery` when a launch, rollout, or rollback exposes an
active failure that needs root-cause repair.

## The Pre-Launch Checklist

### Code Quality

- [ ] Required tests pass, including unit, integration, contract, workflow, or end-to-end checks where relevant
- [ ] Build, package, migration, or deployment artifact generation succeeds with no unexpected warnings
- [ ] Static analysis, linting, schema checks, or type checks pass where used
- [ ] Code reviewed and approved
- [ ] No TODO comments, temporary flags, or debug-only paths that should be resolved before launch
- [ ] No ad hoc debugging output, sensitive logging, or noisy diagnostics left in production paths
- [ ] Error handling covers expected failure modes

### Security

- [ ] No secrets in code or version control
- [ ] Dependency, image, package, or artifact checks show no unacceptable release-blocking vulnerabilities
- [ ] Input validation covers user-facing, partner-facing, batch, and integration entry points
- [ ] Authentication and authorization checks are in place where identity or permissions are involved
- [ ] Transport, browser, API, and platform security controls are configured where relevant
- [ ] Abuse controls, rate limits, quotas, or backpressure are configured for sensitive operations
- [ ] Cross-origin, network, and integration access is restricted to intended consumers

### Performance

- [ ] User-facing responsiveness, request latency, or job processing time meets launch targets
- [ ] Critical paths avoid repeated, unbounded, or unexpectedly expensive work
- [ ] Payloads, assets, artifacts, and transferred data stay within release budgets
- [ ] Data access paths, indexes, partitions, or storage patterns are ready for expected production volume
- [ ] Caching, batching, pagination, or queueing behavior is configured where relevant
- [ ] Resource use and saturation limits are understood for expected traffic or data volume

### Accessibility

- [ ] Keyboard or non-pointer navigation works for interactive surfaces where applicable
- [ ] Assistive technologies can convey content, structure, and state for user interfaces
- [ ] Text, icons, and meaningful visual states meet contrast and non-color communication expectations
- [ ] Focus management works for dialogs, dynamic content, and workflow transitions
- [ ] Errors and recovery instructions are descriptive and connected to the affected action or input
- [ ] Automated or manual accessibility checks have no unresolved launch-blocking findings

### Infrastructure

- [ ] Production configuration, environment variables, and secrets are set through the approved mechanism
- [ ] Data migrations, schema changes, or infrastructure changes are applied or ready to apply safely
- [ ] Routing, networking, certificate, and access configuration are ready where relevant
- [ ] Static assets, packages, images, or deployment artifacts are published and cache behavior is understood
- [ ] Logging, metrics, tracing, and error reporting are configured
- [ ] Health, readiness, smoke, or equivalent verification checks exist and respond

### Documentation

- [ ] README updated with any new setup requirements
- [ ] User, operator, API, integration, or runbook documentation is current where relevant
- [ ] ADRs or decision records written for durable architectural or operational decisions
- [ ] Changelog updated
- [ ] User-facing documentation updated (if applicable)

## Feature Flag Strategy

Ship behind feature flags to decouple deployment from release:

```text
if release_control_enabled("new_capability", actor_or_context):
    use_new_behavior()
else:
    use_existing_behavior()
```

**Feature flag lifecycle:**

```
1. DEPLOY with flag OFF: Code is in production but inactive
2. ENABLE for team/beta: Internal testing in production environment
3. GRADUAL ROLLOUT: 5% to 25% to 50% to 100% of users
4. MONITOR at each stage: Watch error rates, performance, and user feedback
5. CLEAN UP: Remove flag and dead code path after full rollout
```

**Rules:**

- Every feature flag has an owner and an expiration date
- Clean up flags within 2 weeks of full rollout
- Don't nest feature flags (creates exponential combinations)
- Test both flag states (on and off) in CI

## Staged Rollout

### The Rollout Sequence

```
1. DEPLOY to staging
   - Full test suite in staging environment
   - Manual smoke test of critical flows

2. DEPLOY to production (feature flag OFF)
   - Verify deployment succeeded with a health check
   - Check error monitoring for new errors

3. ENABLE for team (flag ON for internal users)
   - Team uses the feature in production
   - 24-hour monitoring window

4. CANARY rollout (flag ON for 5% of users)
   - Monitor error rates, latency, and user behavior
   - Compare metrics: canary vs. baseline
   - 24-48 hour monitoring window
   - Advance only if all thresholds pass (see table below)

5. GRADUAL increase (25% -> 50% -> 100%)
   - Same monitoring at each step
   - Ability to roll back to previous percentage at any point

6. FULL rollout (flag ON for all users)
   - Monitor for 1 week
   - Clean up feature flag
```

### Rollout Decision Thresholds

Use these thresholds to decide whether to advance, hold, or roll back at each stage:

| Metric                      | Advance (green)        | Hold and investigate (yellow) | Roll back (red)     |
| --------------------------- | ---------------------- | ----------------------------- | ------------------- |
| Error rate                  | Within 10% of baseline | 10-100% above baseline        | >2x baseline        |
| P95 latency                 | Within 20% of baseline | 20-50% above baseline         | >50% above baseline |
| New failure modes           | No new severe types    | Low-volume non-severe types   | Severe or growing   |
| Product or business metrics | Neutral or positive    | Decline <5% or unclear signal | Decline >5%         |

### When to Roll Back

Roll back immediately if:

- Error rate increases by more than 2x baseline
- P95 latency increases by more than 50%
- User-reported issues spike
- Data integrity issues detected
- Security vulnerability discovered

## Monitoring and Observability

### What to Monitor

```
Application metrics:
- Error rate (total and by endpoint)
- Response time (p50, p95, p99)
- Request volume
- Active users
- Key business metrics (conversion, engagement)

Infrastructure metrics:
- CPU and memory utilization
- Database connection pool usage
- Disk space
- Network latency
- Queue depth (if applicable)

Client metrics:
- Frontend responsiveness or page load time, for browser-facing products
- Client-side, device-side, or edge errors
- API, integration, or synchronization failures from the consumer perspective
- Accessibility, usability, or workflow completion signals where relevant
```

### Error Reporting

```text
When an error reaches a release boundary:
1. Record the exception type, operation, correlation ID, release version, and safe context.
2. Exclude secrets, credentials, raw personal data, and sensitive internals.
3. Return or display a safe recovery message to the user or caller.
4. Emit a metric or alert signal when the failure affects launch thresholds.
5. Preserve enough detail for operators to diagnose the issue from logs or traces.
```

### Post-Launch Verification

In the first hour after launch:

```
1. Check health endpoint returns 200
2. Check error monitoring dashboard (no new error types)
3. Check latency dashboard (no regression)
4. Test the critical user flow manually
5. Verify logs are flowing and readable
6. Confirm rollback mechanism works (dry run if possible)
```

## Rollback Strategy

Every deployment needs a rollback plan before it happens:

```markdown
## Rollback Plan for [Feature/Release]

### Trigger Conditions

- Error rate > 2x baseline
- P95 latency > [X]ms
- User reports of [specific issue]

### Rollback Steps

1. Disable feature flag (if applicable)
   OR
1. Deploy or restore the previous known-good version: `<rollback_command>`
1. Verify rollback: health check, error monitoring
1. Communicate: notify team of rollback

### Data and State Considerations

- Migration, schema change, configuration change, or state transition [X] has a tested rollback or compensation plan
- Data written by the release is [preserved / migrated back / cleaned up / reconciled]

### Time to Rollback

- Feature flag: < 1 minute
- Redeploy previous version: < 5 minutes
- Database rollback: < 15 minutes
```

## See Also

- For security pre-launch checks, see `references/security-checklist.md`
- For performance pre-launch checklist, see `references/performance-checklist.md`
- For accessibility verification before launch, see `references/accessibility-checklist.md`

## Common Rationalizations

| Rationalization                                 | Reality                                                                                       |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------- |
| "It works in staging, it'll work in production" | Production has different data, traffic patterns, and edge cases. Monitor after deploy.        |
| "We don't need feature flags for this"          | Every feature benefits from a kill switch. Even "simple" changes can break things.            |
| "Monitoring is overhead"                        | Not having monitoring means you discover problems from user complaints instead of dashboards. |
| "We'll add monitoring later"                    | Add it before launch. You can't debug what you can't see.                                     |
| "Rolling back is admitting failure"             | Rolling back is responsible engineering. Shipping a broken feature is the failure.            |

## Red Flags

- Deploying without a rollback plan
- No monitoring or error reporting in production
- Big-bang releases (everything at once, no staging)
- Feature flags with no expiration or owner
- No one monitoring the deploy for the first hour
- Production environment configuration done by memory, not code
- "It's Friday afternoon, let's ship it"

## Verification

Before deploying:

- [ ] Pre-launch checklist completed (all sections green)
- [ ] Feature flag configured (if applicable)
- [ ] Rollback plan documented
- [ ] Monitoring dashboards set up
- [ ] Team notified of deployment

After deploying:

- [ ] Health check returns 200
- [ ] Error rate is normal
- [ ] Latency is normal
- [ ] Critical user flow works
- [ ] Logs are flowing
- [ ] Rollback tested or verified ready
