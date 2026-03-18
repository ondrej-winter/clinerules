---
name: add-hexagonal-feature
description: Implement a new feature or use case in a Python hexagonal project, including domain modeling, ports, application service, and tests.
---

# Skill: Add a Hexagonal Feature

Use this skill to implement a new feature, use case, or business capability in
a Python hexagonal (ports and adapters) project.

## Prerequisites

- The project already has the standard hexagonal `src/` layout.
- The feature is clear enough that you understand its inputs, outputs, and core
  business rules.

## Steps

### 1 — Name the use case

Choose a clear verb-noun name for the use case, for example `PlaceOrder`,
`RegisterUser`, or `SendNotification`. Use that name consistently for the
related files and classes.

### 2 — Model the domain (if new concepts are needed)

Create or update files under `src/<app_name>/domain/`:

- **Entity** — an object with identity that changes over time.
- **Value object** — an immutable descriptor (e.g. `EmailAddress`, `Money`).
- **Domain event** — something that happened (e.g. `OrderPlaced`).

Rules:

- Domain objects must be pure Python with no framework imports or I/O.
- Use `@dataclass(frozen=True)` for value objects.
- Raise domain-specific exceptions (not HTTP errors, not DB errors).

```python
# src/<app_name>/domain/<entity>.py
from dataclasses import dataclass

@dataclass
class <Entity>:
    id: str
```

### 3 — Define port interfaces

Create port interfaces under `src/<app_name>/application/ports/`:

- **Input port** — the interface the use case exposes to the outside world.
  Typically a `Protocol` or `ABC` with a single `execute(command)` method.
- **Output port** — the interface the use case needs from infrastructure, such
  as a repository or email sender.

```python
from typing import Protocol

class <UseCaseName>Port(Protocol):
    def execute(self, command: <Command>) -> <Result>: ...

class <EntityRepository>Port(Protocol):
    def save(self, entity: <Entity>) -> None: ...
```

### 4 — Implement the application service

Create the use case implementation under `src/<app_name>/application/`:

```python
class <UseCaseName>:
    def __init__(self, repository: <EntityRepository>Port) -> None:
        self._repository = repository

    def execute(self, command: <Command>) -> <Result>:
        ...
```

Rules:

- The application service **only** depends on domain objects and port interfaces.
- It must not import from `adapters/`.
- It must not perform I/O directly, including `open()`, HTTP calls, or database
  access.

### 5 — Write unit tests first (TDD encouraged)

Create tests under `tests/unit/`:

```python
from unittest.mock import MagicMock

def test_<use_case_name>_happy_path() -> None:
    repo = MagicMock()
    use_case = <UseCaseName>(repository=repo)
    use_case.execute(<Command>(...))
    repo.save.assert_called_once()
```

- Use `MagicMock` or a hand-written fake for outbound ports, never real
  infrastructure.
- Cover the happy path and at least one failure or edge case.

## Dependency direction reminder

```
adapters/input   →  application  →  domain
adapters/output  →  (implements application/ports)
```

Never let an arrow point in the opposite direction.
