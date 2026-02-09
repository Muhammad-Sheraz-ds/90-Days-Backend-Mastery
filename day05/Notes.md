# Additional Notes: Dataclasses & Type Hints for Backend

> **Day 5 - Backend Mastery: Supplementary Resources**
> Consolidated from official Python documentation and reliable sources

---

## Integration with Pydantic & FastAPI

Pydantic, the validation library powering FastAPI, is built on dataclass concepts and type hints:

```python
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    age: Optional[int] = None

# FastAPI endpoint
@app.post("/users")
async def create_user(user: UserCreate):
    return {"username": user.username}
```

**Why it matters**: Understanding dataclasses and type hints makes Pydantic intuitive.

---

## dataclasses vs Pydantic Comparison

| Feature | dataclass | Pydantic BaseModel |
|---------|-----------|-------------------|
| Runtime validation | ❌ No | ✅ Yes |
| Type coercion | ❌ No | ✅ Yes |
| JSON serialization | `asdict()` | `.model_dump()` |
| Schema generation | ❌ No | ✅ OpenAPI/JSON Schema |
| Performance | Faster creation | Slower (validation) |
| Use case | Internal data | API boundaries |

---

## Type Hints for Async/Await (Backend Essential)

```python
from typing import Coroutine, Awaitable
import asyncio

async def fetch_user(user_id: int) -> dict[str, str]:
    # Simulating DB call
    await asyncio.sleep(0.1)
    return {"id": str(user_id), "name": "Alice"}

async def get_multiple_users(ids: list[int]) -> list[dict[str, str]]:
    tasks = [fetch_user(id) for id in ids]
    return await asyncio.gather(*tasks)
```

---

## TypedDict for JSON Responses

When you need typed dictionaries (common in APIs):

```python
from typing import TypedDict

class UserResponse(TypedDict):
    id: int
    username: str
    email: str
    is_active: bool

def format_user(raw: dict) -> UserResponse:
    return {
        "id": raw["id"],
        "username": raw["username"],
        "email": raw["email"],
        "is_active": raw.get("active", True)
    }
```

---

## Protocol Classes (Structural Typing)

Define interfaces for dependency injection:

```python
from typing import Protocol

class Repository(Protocol):
    def get(self, id: int) -> dict: ...
    def save(self, data: dict) -> int: ...

class PostgresRepo:
    def get(self, id: int) -> dict:
        return {"id": id}
    
    def save(self, data: dict) -> int:
        return 1

def use_repo(repo: Repository):
    """Works with any class matching the Protocol signature."""
    return repo.get(1)

use_repo(PostgresRepo())  # Type checks!
```

---

## Mypy Configuration for Backend Projects

**pyproject.toml**:
```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true

# Ignore missing stubs for third-party libraries
[[tool.mypy.overrides]]
module = ["sqlalchemy.*", "redis.*"]
ignore_missing_imports = true
```

---

## Common Backend Type Patterns

### Database Query Results
```python
from typing import Optional, TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class QueryResult(Generic[T]):
    data: Optional[T]
    error: Optional[str] = None
    
    @property
    def success(self) -> bool:
        return self.error is None
```

### Configuration with Validation
```python
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class DatabaseConfig:
    host: str
    port: int = 5432
    max_connections: int = 10
    MIN_PORT: ClassVar[int] = 1
    MAX_PORT: ClassVar[int] = 65535
    
    def __post_init__(self):
        if not (self.MIN_PORT <= self.port <= self.MAX_PORT):
            raise ValueError(f"Port must be between {self.MIN_PORT} and {self.MAX_PORT}")
```

### Service Response Pattern
```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

@dataclass(frozen=True)
class ServiceResponse(Generic[T]):
    data: Optional[T] = None
    error: Optional[str] = None
    status_code: int = 200
    
    @classmethod
    def success(cls, data: T) -> "ServiceResponse[T]":
        return cls(data=data, status_code=200)
    
    @classmethod
    def error(cls, message: str, code: int = 400) -> "ServiceResponse[T]":
        return cls(error=message, status_code=code)
```

---

## Quick Reference: Type Hint Cheat Sheet

```python
# Basic types
x: int = 1
y: float = 1.0
z: str = "hello"
flag: bool = True

# Collections (Python 3.9+)
items: list[int] = [1, 2, 3]
mapping: dict[str, int] = {"a": 1}
unique: set[str] = {"a", "b"}
fixed: tuple[int, str, float] = (1, "a", 1.0)

# Optional (value or None)
maybe: str | None = None  # Python 3.10+
maybe: Optional[str] = None  # Earlier versions

# Union (multiple types)
multi: int | str = "hello"  # Python 3.10+
multi: Union[int, str] = "hello"  # Earlier versions

# Callable
func: Callable[[int, int], int] = lambda x, y: x + y

# Any (escape hatch)
unknown: Any = get_external_data()

# Type alias
type UserId = int  # Python 3.12+
UserId: TypeAlias = int  # Earlier versions
```

---

## Running Mypy

```bash
# Install
pip install mypy

# Check single file
mypy typed_models.py

# Check with strict mode
mypy --strict typed_models.py

# Generate HTML report
mypy --html-report ./mypy-report typed_models.py
```

---

## Key Takeaways

1. **Type hints + dataclasses = Modern Python**
2. **Pydantic extends these concepts** with validation
3. **Use frozen dataclasses** for immutable data transfer
4. **Run mypy in CI/CD** to catch errors early
5. **TypedDict and Protocol** for flexible typing
6. **Always type public APIs** (endpoints, service methods)
