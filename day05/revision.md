# Day 5 Quick Revision: Dataclasses & Type Hints
> ⏱️ **2-Minute Revision Guide** | Focus: Definitions, Core Concepts, Why We Use

---

## 🎯 DATACLASSES

### What?
A **decorator** (`@dataclass`) that auto-generates `__init__`, `__repr__`, `__eq__` methods for classes holding data.

### Why?
- **Eliminate boilerplate** — no manual `__init__` writing
- **Built-in equality** — compare objects by values, not identity
- **Readable repr** — `User(name='Alice', age=30)` instead of `<object at 0x...>`
- **Foundation for Pydantic/FastAPI**

### Core Syntax
```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str                              # Required field
    age: int = 0                           # Default value
    tags: list[str] = field(default_factory=list)  # Mutable default (SAFE)
```

### Essential Decorator Parameters
| Param | Default | Purpose |
|-------|---------|---------|
| `frozen=True` | False | **Immutable** instances (can't modify after creation) |
| `order=True` | False | Enable `<`, `>` comparison |
| `slots=True` | False | Memory optimization (Python 3.10+) |

### field() — When to Use
| Scenario | Solution |
|----------|----------|
| Mutable default (list/dict) | `field(default_factory=list)` |
| Exclude from repr | `field(repr=False)` |
| Computed field | `field(init=False)` + `__post_init__` |

### __post_init__ — Computed Values & Validation
```python
@dataclass
class Order:
    quantity: int
    price: float
    total: float = field(init=False)  # Not in __init__
    
    def __post_init__(self):
        self.total = self.quantity * self.price  # Auto-computed
```

### Key Functions
| Function | Purpose |
|----------|---------|
| `asdict(obj)` | Convert to dict (for JSON) |
| `replace(obj, field=val)` | Create modified copy |

---

## 🏷️ TYPE HINTS

### What?
Annotations specifying **expected types** for variables, parameters, return values.

### Why?
- **Catch bugs early** — mypy finds type errors before runtime
- **IDE autocomplete** — better code suggestions
- **Self-documenting** — code explains itself
- **API contracts** — clear function signatures

### Core Syntax
```python
def process(name: str, count: int = 0) -> dict[str, int]:
    return {name: count}
```

### Essential Types
| Type | Meaning | Example |
|------|---------|---------|
| `str`, `int`, `float`, `bool` | Basic types | `age: int = 25` |
| `list[T]` | List of T | `items: list[str]` |
| `dict[K, V]` | Dictionary | `config: dict[str, int]` |
| `Optional[T]` / `T \| None` | T or None | `user: Optional[str]` |
| `Union[A, B]` / `A \| B` | A or B | `id: int \| str` |
| `Any` | Any type (avoid!) | `data: Any` |
| `Callable[[args], ret]` | Function type | `Callable[[int], str]` |

### Optional = Can Be None
```python
from typing import Optional

def find_user(id: int) -> Optional[str]:  # Returns str OR None
    return db.get(id)  # Might not exist
```

---

## 🔗 WHY BOTH TOGETHER?

| Dataclass Feature | Requires Type Hints |
|-------------------|---------------------|
| Field definitions | ✅ `name: str` |
| Auto __init__ params | ✅ Uses hint as type |
| Pydantic models | ✅ Built on both |

```python
@dataclass
class APIResponse:          # Dataclass = structure
    status: int             # Type hint = contract
    message: str
    data: Optional[dict]    # Can be None
```

---

## ⚠️ CRITICAL GOTCHAS

| ❌ Wrong | ✅ Correct | Why |
|---------|-----------|-----|
| `items: list = []` | `items: list = field(default_factory=list)` | Shared mutable default |
| `Optional[str]` for required | Just `str` | Optional means nullable |
| Skip type hints | Always add | Mypy can't check untyped code |

---

## 🛠️ MYPY — Static Type Checker

```bash
pip install mypy
mypy your_file.py          # Check for type errors
mypy --strict your_file.py # Maximum strictness
```

---

## 🎯 BACKEND QUICK REFERENCE

| Use Case | Pattern |
|----------|---------|
| API Request/Response | `@dataclass(frozen=True)` |
| Config objects | `@dataclass` with defaults |
| DB query results | `Optional[T]` return type |
| Service methods | Full type annotations |
| JSON output | `asdict(obj)` |

---

## 📝 ONE-LINE DEFINITIONS

- **Dataclass**: Decorator that auto-generates class boilerplate from type-annotated fields
- **Type Hint**: Annotation declaring expected type (not enforced at runtime)
- **field()**: Customize individual dataclass field behavior
- **frozen**: Makes dataclass immutable (like tuple)
- **default_factory**: Safe way to create mutable defaults
- **Optional**: Type that can also be None
- **mypy**: Static analyzer that catches type errors before runtime
- **Pydantic**: Validation library built on dataclasses + type hints (used by FastAPI)
