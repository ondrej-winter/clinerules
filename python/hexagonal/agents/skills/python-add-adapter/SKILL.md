---
name: python-add-adapter
description: Add an input or output adapter to a Python hexagonal project while keeping business logic in the application layer.
---

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
    adapter.py
```

Keep `__init__.py` lightweight. Re-export the intended public symbol only when you want a stable package-level API, and declare `__all__` when that curated surface adds clarity:

```python
from .adapter import router

__all__ = ["router"]
```

### 2 - Implement

- Accept external input, map it to an application command/query DTO, call the application through its input port or service entry point, and map the result or exception back to the external format.
- Do not import from `domain/` directly.
- Keep all business logic in the application service.
- Map domain exceptions to adapter-level error responses.

### 3 - Test

Place tests under `tests/integration/<adapter_name>/`. Test through the framework's test client or transport boundary, and inject a fake or stubbed application service where possible to keep the tests focused on adapter behavior.

Add unit tests only if the adapter package contains meaningful mapping or serialization helpers that warrant direct, framework-free verification.

## Output adapter

Implements a port interface and talks to external infrastructure.

### 1 - Create the module

```
src/<app_name>/adapters/output/<adapter_name>/
    __init__.py
    adapter.py
```

Keep `__init__.py` lightweight. Re-export the intended public symbol only when you want a stable package-level API, and declare `__all__` when that curated surface adds clarity:

```python
from .adapter import <AdapterName>

__all__ = ["<AdapterName>"]
```

### 2 - Implement

- Implement all port interface methods.
- Map infrastructure types to domain objects inside the adapter -- never leak them out.
- Raise domain exceptions, not infrastructure exceptions.
- Keep framework clients, ORM models, serializers, and transport-specific configuration inside the adapter package.

### 3 - Test

Write unit tests against the adapter using fakes, stubs, or mocks around the infrastructure boundary where practical. Follow with integration tests against the real framework or infrastructure boundary when the adapter behavior depends on actual driver, network, or persistence integration.
