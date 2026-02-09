# mCoding: Python Type Hints - Video Notes

> **Source**: [mCoding - Python Type Hints](https://www.youtube.com/watch?v=QORvB-_mbZ0)
> **Day 5 - Backend Mastery: Dataclasses & Type Hints**

---

## What Are Type Hints?

Type hints are **annotations** that specify expected types for variables, function parameters, and return values. They are:

- **Not enforced at runtime** by Python
- **Used by static type checkers** like `mypy`
- **Improve code readability** and documentation
- **Enable IDE autocompletion** and error detection

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

---

## Basic Type Annotations

### Variables
```python
name: str = "Alice"
age: int = 30
price: float = 19.99
is_active: bool = True
```

### Functions
```python
def add(a: int, b: int) -> int:
    return a + b

def process(data: str) -> None:
    print(data)  # Returns None implicitly
```

---

## Container Types (Modern Syntax - Python 3.9+)

```python
# Lists
numbers: list[int] = [1, 2, 3]
names: list[str] = ["Alice", "Bob"]

# Dictionaries
config: dict[str, int] = {"timeout": 30, "retries": 3}
users: dict[int, str] = {1: "Alice", 2: "Bob"}

# Sets
unique_ids: set[int] = {1, 2, 3}

# Tuples (fixed length and types)
point: tuple[int, int] = (10, 20)
record: tuple[str, int, float] = ("item", 100, 9.99)
```

### Pre-3.9 Syntax (using typing module)
```python
from typing import List, Dict, Set, Tuple

numbers: List[int] = [1, 2, 3]
config: Dict[str, int] = {"timeout": 30}
```

---

## Optional Types

For values that can be `None`:

```python
from typing import Optional

# Optional[X] is equivalent to X | None (Python 3.10+)

def find_user(user_id: int) -> Optional[str]:
    """Returns username or None if not found."""
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)

# Python 3.10+ syntax
def find_user(user_id: int) -> str | None:
    ...
```

---

## Union Types

For values that can be multiple types:

```python
from typing import Union

# Union[X, Y] means X or Y
def process_id(id: Union[int, str]) -> str:
    return str(id)

# Python 3.10+ syntax
def process_id(id: int | str) -> str:
    return str(id)
```

---

## Any Type

Opt-out of type checking for a specific variable:

```python
from typing import Any

def log_anything(value: Any) -> None:
    print(value)

config: Any = load_external_config()  # Type unknown
```

> [!WARNING]
> Use `Any` sparingly - it defeats the purpose of type hints!

---

## Callable Types

For functions as parameters:

```python
from typing import Callable

def apply_operation(
    x: int, 
    y: int, 
    operation: Callable[[int, int], int]
) -> int:
    return operation(x, y)

def add(a: int, b: int) -> int:
    return a + b

result = apply_operation(5, 3, add)  # 8
```

**Syntax**: `Callable[[param_types], return_type]`

---

## Type Aliases

Create readable names for complex types:

```python
# Python 3.12+ syntax
type UserId = int
type UserRecord = dict[str, str | int]
type Handler = Callable[[str], None]

# Pre-3.12 syntax
from typing import TypeAlias

UserId: TypeAlias = int
UserRecord: TypeAlias = dict[str, str | int]
```

---

## Class as Type Annotations

```python
class User:
    def __init__(self, name: str):
        self.name = name

def get_username(user: User) -> str:
    return user.name

def create_user(name: str) -> User:
    return User(name)
```

### Forward References (for self-referencing)
```python
class Node:
    def __init__(self, value: int, next: "Node | None" = None):
        self.value = value
        self.next = next
```

---

## Generic Types

Create reusable type patterns:

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        return self._items.pop()

int_stack: Stack[int] = Stack()
int_stack.push(42)
```

---

## Mypy - Static Type Checker

### Installation
```bash
pip install mypy
```

### Usage
```bash
mypy your_script.py
```

### Configuration (mypy.ini or pyproject.toml)
```ini
[mypy]
python_version = 3.11
strict = true
warn_return_any = true
warn_unused_ignores = true
```

---

## Backend-Specific Type Patterns

### API Handler
```python
from typing import Optional

def get_user(
    user_id: int,
    include_profile: bool = False
) -> dict[str, str | int | None]:
    ...
```

### Database Results
```python
from typing import Optional

def fetch_record(table: str, id: int) -> Optional[dict[str, Any]]:
    """Returns record or None if not found."""
    ...
```

### Configuration
```python
type DatabaseConfig = dict[str, str | int]

def connect(config: DatabaseConfig) -> Connection:
    ...
```

### Async Functions
```python
from typing import Coroutine
import asyncio

async def fetch_data(url: str) -> dict[str, Any]:
    ...

# Return type is actually Coroutine[Any, Any, dict[str, Any]]
```

---

## Common Type Hints Reference

| Type | Example | Description |
|------|---------|-------------|
| `str` | `name: str` | String |
| `int` | `count: int` | Integer |
| `float` | `price: float` | Float |
| `bool` | `active: bool` | Boolean |
| `None` | `-> None` | No return value |
| `list[T]` | `list[int]` | List of T |
| `dict[K, V]` | `dict[str, int]` | Dictionary |
| `set[T]` | `set[str]` | Set of T |
| `tuple[T, ...]` | `tuple[int, str]` | Fixed tuple |
| `Optional[T]` | `Optional[str]` | T or None |
| `Union[T, U]` | `Union[int, str]` | T or U |
| `Any` | `value: Any` | Any type |
| `Callable[[], T]` | `Callable[[], int]` | Function type |

---

## Best Practices for Backend Development

1. **Type all public functions** - APIs, handlers, service methods
2. **Use Optional for nullable returns** - Database queries, API calls
3. **Define type aliases for complex types** - Improve readability
4. **Run mypy in CI/CD** - Catch errors before deployment
5. **Start with `--strict` mode** - Maximum type safety
6. **Avoid `Any`** - Only when truly dynamic (external data)

> [!IMPORTANT]
> Type hints are the foundation for **Pydantic validation** in FastAPI. Mastering them is essential for modern Python backend development.
