# Testing Patterns

Use these patterns when choosing how to make behavior verifiable before or during implementation.

## Behavior-first tests

- Name the behavior from the user's or caller's perspective.
- Arrange only the state required for that behavior.
- Assert the observable outcome rather than internal implementation details.
- Keep setup small enough that the failure points to one behavior.

## Regression tests

- Reproduce the reported failure before fixing it.
- Keep the test focused on the bug's public symptom.
- Verify the test fails for the current behavior and passes after the fix.
- Add edge cases only when they represent distinct risks.

## Contract tests

- Use contract tests at module, service, adapter, or API boundaries.
- Verify success, failure, and malformed input paths.
- Avoid coupling the contract test to a single implementation when alternatives are allowed.

## Anti-patterns

- Testing private implementation details instead of behavior.
- Writing broad tests with many unrelated assertions.
- Adding mocks that duplicate the implementation.
- Accepting a test that never failed for the bug or feature it claims to cover.
