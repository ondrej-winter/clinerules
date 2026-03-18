# Skill: Add a Hexagonal Feature

Use this skill when the user asks to implement a new feature, use case, or
business capability in a Python hexagonal (ports & adapters) project.

## Prerequisites

- The project already has the standard hexagonal `src/` layout.
- The user has described the feature and you understand its inputs, outputs, and
  the business rule it encodes.

---

## Steps

### 1 — Name the use case

Derive a clear verb-noun name for the use case, e.g. `PlaceOrder`, `RegisterUser`,
`SendNotification`. This name drives every file name and class name below.

### 2 — Model the domain (if new concepts are needed)

Create or update files under `src/<app_name>/domain/`:

- **Entity** — an object with identity that changes over time.
- **Value object** — an immutable descriptor (e.g. `EmailAddress`, `Money`).
- **Domain event** — something that happened (e.g. `OrderPlaced`).

Rules:
- Domain objects must be **pure Python** — no framework imports, no I/O.
- Use `@dataclass(frozen=True)` for value objects.
- Raise domain-specific exceptions (not HTTP errors, not DB errors).

```python
# src/<app_name>/domain/<entity>.py
from dataclasses import dataclass

@dataclass
class <Entity>:
    id: str
    # …fields…
```

### 3 — Define port interfaces

Create port interfaces under `src/<app_name>/application/ports/`:

- **Inbound port** (driven) — the interface the use case exposes to the outside
  world. Typically a `Protocol` or `ABC` with a single `execute(command)` method.
- **Outbound port** (driving) — the interface the use case needs from
  infrastructure (e.g. a repository, an email sender).

```python
# src/<app_name>/application/ports/<use_case>_port.py
from typing import Protocol
from <app_name>.domain.<entity> import <Entity>

class <UseCaseName>Port(Protocol):
    def execute(self, command: <Command>) -> <Result>: ...

class <EntityRepository>Port(Protocol):
    def save(self, entity: <Entity>) -> None: ...
    def find_by_id(self, id: str) -> <Entity> | None: ...
```

### 4 — Implement the application service

Create the use case implementation under `src/<app_name>/application/`:

```python
# src/<app_name>/application/<use_case_snake>.py
from <app_name>.application.ports.<use_case>_port import (
    <EntityRepository>Port,
)
from <app_name>.domain.<entity> import <Entity>

class <UseCaseName>:
    def __init__(self, repository: <EntityRepository>Port) -> None:
        self._repository = repository

    def execute(self, command: <Command>) -> <Result>:
        # 1. Validate / load domain objects
        # 2. Apply business rule
        # 3. Persist via outbound port
        # 4. Return result or raise domain exception
        ...
```

Rules:
- The application service **only** depends on domain objects and port interfaces.
- It must not import from `adapters/`.
- It must not perform I/O directly (no `open()`, `requests`, DB calls).

### 5 — Write unit tests first (TDD encouraged)

Create tests under `tests/unit/`:

```python
# tests/unit/test_<use_case_snake>.py
from unittest.mock import MagicMock
from <app_name>.application.<use_case_snake> import <UseCaseName>

def test_<use_case_name>_happy_path() -> None:
    repo = MagicMock()
    use_case = <UseCaseName>(repository=repo)
    result = use_case.execute(<Command>(…))
    assert result == <expected>
    repo.save.assert_called_once()

def test_<use_case_name>_raises_when_<condition>() -> None:
    ...
```

- Use `MagicMock` or a hand-written fake for outbound ports — never the real
  infrastructure.
- Cover both the happy path and at least one failure / edge case.

### 6 — Wire up adapters (only if needed for this feature)

If the feature requires a new inbound entry point (HTTP endpoint, CLI command,
event handler) or a new outbound implementation (DB repo, API client), follow
the **Add Adapter** skill for that step.

### 7 — Run quality checks

```bash
uv run ruff check . --fix
uv run mypy .
uv run pytest --cov --cov-report=term-missing
```

All checks must pass before considering the feature complete.

---

## Dependency direction reminder

```
adapters/inbound  →  application  →  domain
adapters/outbound →  (implements application/ports)
```

Never let an arrow point in the opposite direction.
