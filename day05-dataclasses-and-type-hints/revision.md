# Day 5 Revision: Dataclasses & Type Hints
> ⏱️ 2-Minute Quick Recap

---

## TOPIC DEFINITIONS

### What is a Dataclass?
A **dataclass** is a Python decorator (`@dataclass`) that automatically generates boilerplate code for classes primarily used to store data. It auto-creates `__init__`, `__repr__`, and `__eq__` methods based on class attributes with type annotations.

**Purpose**: Eliminate repetitive code when creating data containers, make classes more readable, enable easy serialization to dicts/JSON, and provide a foundation for validation libraries like Pydantic.

### What are Type Hints?
**Type hints** are annotations that specify the expected data type of variables, function parameters, and return values. They are checked by static analyzers like `mypy` but are NOT enforced at runtime by Python.

**Purpose**: Catch type-related bugs before runtime, enable IDE autocomplete and error detection, make code self-documenting, and define clear API contracts between functions/modules.

---

## DATACLASSES

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str                                      # Required
    age: int = 0                                   # Default
    tags: list[str] = field(default_factory=list) # Mutable default
```

### Key Parameters

| Parameter | Effect |
|-----------|--------|
| `frozen=True` | Immutable (can't change fields) |
| `order=True` | Enables `<`, `>`, `<=`, `>=` |
| `slots=True` | Less memory, faster access |

### field() Uses

| Need | Solution |
|------|----------|
| List/dict default | `field(default_factory=list)` |
| Hide from repr | `field(repr=False)` |
| Computed value | `field(init=False)` + `__post_init__` |

### Utility Functions
- `asdict(obj)` → Convert to dict
- `replace(obj, x=val)` → Copy with changes

---

## TYPE HINTS

```python
def get_user(id: int) -> dict[str, str]:
    return {"id": str(id), "name": "Alice"}
```

### Common Types

| Type | Meaning |
|------|---------|
| `str`, `int`, `float`, `bool` | Primitives |
| `list[T]` | List of T |
| `dict[K, V]` | Key-value mapping |
| `Optional[T]` or `T \| None` | T or None |
| `Union[A, B]` or `A \| B` | Either type |
| `Callable[[args], ret]` | Function type |
| `Any` | Anything (avoid when possible) |

---

## COMMON MISTAKES

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `items: list = []` | `items: list = field(default_factory=list)` |
| Skipping type hints | Always annotate public functions |
| Using `Any` everywhere | Be specific about types |

---

## MYPY

```bash
pip install mypy
mypy file.py        # Type check
mypy --strict file.py  # Strict mode
```

---

## BACKEND PATTERNS

| Scenario | Pattern |
|----------|---------|
| API models | `@dataclass(frozen=True)` |
| Config | `@dataclass` with defaults |
| Nullable returns | `-> Optional[T]` |
| JSON output | `asdict(obj)` |

---

## KEY TERMS

| Term | One-liner |
|------|-----------|
| `@dataclass` | Auto-generates class methods from fields |
| Type hint | Expected type annotation (not runtime enforced) |
| `field()` | Customize dataclass field behavior |
| `frozen` | Makes instance immutable |
| `default_factory` | Safe mutable defaults |
| `Optional[T]` | T or None |
| `mypy` | Static type checker |
| Pydantic | Validation library using dataclasses + types |
