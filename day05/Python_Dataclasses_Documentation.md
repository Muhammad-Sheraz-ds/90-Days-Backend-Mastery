# Python Dataclasses - Official Documentation Notes

> **Source**: [Python Dataclasses Documentation](https://docs.python.org/3/library/dataclasses.html)
> **Day 5 - Backend Mastery: Dataclasses & Type Hints**

---

## What Are Dataclasses?

Dataclasses provide a **decorator and functions for automatically generating special methods** like `__init__()`, `__repr__()`, and `__eq__()` for user-defined classes. Introduced in Python 3.7 via PEP 557.

```python
from dataclasses import dataclass

@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand
```

**Auto-generated `__init__`:**
```python
def __init__(self, name: str, unit_price: float, quantity_on_hand: int = 0):
    self.name = name
    self.unit_price = unit_price
    self.quantity_on_hand = quantity_on_hand
```

---

## The @dataclass Decorator Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `init` | `True` | Generate `__init__()` method |
| `repr` | `True` | Generate `__repr__()` method |
| `eq` | `True` | Generate `__eq__()` method (compares as tuple of fields) |
| `order` | `False` | Generate `__lt__`, `__le__`, `__gt__`, `__ge__` methods |
| `frozen` | `False` | Make instances immutable (raises exception on assignment) |
| `slots` | `False` | Generate `__slots__` for memory optimization (3.10+) |
| `kw_only` | `False` | All fields are keyword-only in `__init__` (3.10+) |

```python
@dataclass(frozen=True, order=True)
class ImmutablePoint:
    x: float
    y: float
```

---

## The field() Function

Use `field()` for advanced per-field configuration:

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    name: str
    items: list = field(default_factory=list)  # Safe mutable default
    _cache: dict = field(default_factory=dict, repr=False, compare=False)
```

### field() Parameters

| Parameter | Description |
|-----------|-------------|
| `default` | Default value for the field |
| `default_factory` | Zero-argument callable for mutable defaults |
| `init` | Include in `__init__()` (default: True) |
| `repr` | Include in `__repr__()` (default: True) |
| `compare` | Include in comparison methods (default: True) |
| `hash` | Include in `__hash__()` (default: same as compare) |
| `metadata` | Read-only mapping for third-party extensions |
| `kw_only` | Mark field as keyword-only (3.10+) |

---

## Mutable Default Values - Critical Backend Concept

> [!CAUTION]
> Never use mutable objects as default values directly. This causes all instances to share the same object!

**❌ Wrong:**
```python
@dataclass
class BadService:
    connections: list = []  # ValueError raised!
```

**✅ Correct:**
```python
@dataclass
class GoodService:
    connections: list = field(default_factory=list)  # Each instance gets new list
```

---

## Post-Init Processing

Use `__post_init__()` for computed fields or validation:

```python
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)  # Computed, not in __init__

    def __post_init__(self):
        self.area = self.width * self.height
```

---

## Init-Only Variables (InitVar)

Variables used only during initialization, not stored as fields:

```python
from dataclasses import dataclass, field, InitVar

@dataclass
class UserService:
    username: str
    password_hash: str = field(init=False)
    password: InitVar[str] = None  # Not stored as a field

    def __post_init__(self, password: str):
        if password:
            self.password_hash = hash_password(password)
```

---

## Frozen (Immutable) Dataclasses

**Critical for API response models and thread safety:**

```python
@dataclass(frozen=True)
class APIResponse:
    status_code: int
    message: str
    data: dict
```

- Raises `FrozenInstanceError` on assignment attempts
- Enables `__hash__()` generation (can be used in sets/dicts)
- Small performance penalty in `__init__`

---

## Inheritance

Fields are ordered by first definition, derived classes override base classes:

```python
@dataclass
class BaseModel:
    id: int
    created_at: str = ""

@dataclass
class User(BaseModel):
    username: str
    email: str = ""  # Required: defaults after inherited defaults
```

> [!WARNING]
> If base class has defaults, all subclass fields must also have defaults.

---

## Utility Functions

| Function | Purpose |
|----------|---------|
| `fields(obj)` | Return tuple of Field objects |
| `asdict(obj)` | Convert to dict (recursive) |
| `astuple(obj)` | Convert to tuple (recursive) |
| `replace(obj, **changes)` | Create copy with modifications |
| `is_dataclass(obj)` | Check if dataclass or instance |

```python
from dataclasses import asdict, replace

user = User(id=1, username="admin")
user_dict = asdict(user)  # {'id': 1, 'username': 'admin', ...}
updated = replace(user, username="superadmin")
```

---

## Backend Relevance

| Feature | Backend Use Case |
|---------|------------------|
| `frozen=True` | API response models, DTOs, cache keys |
| `field(default_factory=...)` | Service containers, configuration objects |
| `__post_init__` | Validation, computed properties, DB connections |
| `asdict()` | JSON serialization, ORM mapping |
| `slots=True` | High-performance data objects, reduced memory |
| `InitVar` | Dependency injection, password handling |

> [!IMPORTANT]
> **Pydantic (FastAPI's validation library) is built on dataclasses and type hints.** Mastering these concepts is essential for modern Python backend development.
