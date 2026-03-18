# Skill: Add an Adapter

Use this skill when the user asks to add a new inbound adapter (HTTP endpoint,
CLI command, event consumer, …) or a new outbound adapter (database repository,
HTTP client, message publisher, …) to a Python hexagonal project.

## Prerequisites

- The relevant port interface already exists in
  `src/<app_name>/application/ports/`.
- The user has specified what kind of adapter is needed.

---

## Inbound adapter

An inbound adapter **drives** the application — it receives external input
(HTTP request, CLI args, message, …) and calls an application service.

### Steps

#### 1 — Choose the technology

Common choices: `FastAPI`, `Flask`, `Click`, `Typer`, `aio-pika`, `kafka-python`.
Install with:

```bash
uv add <library>
```

#### 2 — Create the adapter module

```
src/<app_name>/adapters/inbound/<adapter_name>/
├── __init__.py
└── <adapter_name>.py
```

#### 3 — Implement the adapter

The adapter must:
- Accept external input (request body, CLI args, message payload).
- Map it to a command/query object expected by the application service.
- Call the application service via its port interface.
- Map the result (or exception) back to an external response format.

```python
# src/<app_name>/adapters/inbound/<adapter_name>/<adapter_name>.py

# Example: FastAPI router
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from <app_name>.application.<use_case_snake> import <UseCaseName>
from <app_name>.application.ports.<use_case>_port import <Command>

router = APIRouter()

class <RequestBody>(BaseModel):
    # …fields…

@router.post("/<resource>")
def <endpoint>(body: <RequestBody>, use_case: <UseCaseName>) -> dict:
    try:
        result = use_case.execute(<Command>(**body.model_dump()))
        return {"id": result.id}
    except <DomainException> as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
```

Rules:
- Inbound adapters must **not** import from `domain/` directly.
- All business logic stays in the application service.
- Map domain exceptions to adapter-level error responses here.

#### 4 — Write integration tests

```
tests/integration/<adapter_name>/
└── test_<adapter_name>.py
```

Use the framework's test client and inject a fake/mock application service.

---

## Outbound adapter

An outbound adapter **implements** a port interface defined in
`src/<app_name>/application/ports/` and talks to external infrastructure.

### Steps

#### 1 — Choose the technology

Common choices: `sqlalchemy`, `httpx`, `aiobotocore`, `redis-py`.
Install with:

```bash
uv add <library>
```

#### 2 — Create the adapter module

```
src/<app_name>/adapters/outbound/<adapter_name>/
├── __init__.py
└── <adapter_name>.py
```

#### 3 — Implement the adapter

```python
# src/<app_name>/adapters/outbound/<adapter_name>/<adapter_name>.py
from <app_name>.application.ports.<port_module> import <PortInterface>
from <app_name>.domain.<entity> import <Entity>

class <AdapterName>(<PortInterface>):
    def __init__(self, session: <Session>) -> None:
        self._session = session

    def save(self, entity: <Entity>) -> None:
        # map domain object → ORM model / API payload / message
        ...

    def find_by_id(self, id: str) -> <Entity> | None:
        # query infrastructure and map result → domain object
        ...
```

Rules:
- The adapter class must implement **all** methods of the port interface.
- Map infrastructure types (ORM rows, HTTP responses, …) to domain objects
  **inside** the adapter — never leak infrastructure types into the domain.
- Raise domain exceptions, not infrastructure exceptions, when appropriate.

#### 4 — Write integration tests

Test against a real or containerised instance of the infrastructure (use
`pytest-docker` or `testcontainers` where appropriate).

```python
# tests/integration/<adapter_name>/test_<adapter_name>.py

def test_save_and_find(real_session) -> None:
    adapter = <AdapterName>(real_session)
    entity = <Entity>(id="1", …)
    adapter.save(entity)
    found = adapter.find_by_id("1")
    assert found == entity
```

---

## After adding either adapter

```bash
uv run ruff check . --fix
uv run mypy .
uv run pytest --cov --cov-report=term-missing
```

All checks must pass before the adapter is considered complete.
