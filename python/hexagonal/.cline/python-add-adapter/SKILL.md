# Skill: Add an Adapter

Use this skill to add an input adapter (HTTP endpoint, CLI command, event consumer) or an output adapter (database repository, HTTP client, message publisher) to a Python hexagonal project.

## Prerequisites

- Port interface exists in `src/<app_name>/application/ports/`.
- Technology chosen and library installed: `uv add <library>`

## Input adapter

Drives the application -- receives external input and calls an application service.

### 1 - Create the module

```
src/<app_name>/adapters/input/<adapter_name>/
    __init__.py
    <adapter_name>.py
```

Re-export the public symbol and declare `__all__` in `__init__.py`:

```python
from <app_name>.adapters.input.<adapter_name>.<adapter_name> import router

__all__ = ["router"]
```

### 2 - Implement

- Accept external input, map to command/query, call the service via its port, map result/exception back to external format.
- Do not import from `domain/` directly.
- Keep all business logic in the application service.
- Map domain exceptions to adapter-level error responses.

### 3 - Test

Place tests under `tests/integration/<adapter_name>/`. Test through the framework's test client; inject a fake application service to keep tests fast and isolated.

## Output adapter

Implements a port interface and talks to external infrastructure.

### 1 - Create the module

```
src/<app_name>/adapters/output/<adapter_name>/
    __init__.py
    <adapter_name>.py
```

Re-export the public symbol and declare `__all__` in `__init__.py`:

```python
from <app_name>.adapters.output.<adapter_name>.<adapter_name> import <AdapterName>

__all__ = ["<AdapterName>"]
```

### 2 - Implement

- Implement all port interface methods.
- Map infrastructure types to domain objects inside the adapter -- never leak them out.
- Raise domain exceptions, not infrastructure exceptions.

### 3 - Test

Write a unit test with a fake/stub of the port first. Follow with an integration test against a real or containerised infrastructure instance.
