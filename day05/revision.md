# Day 5 Revision: Dataclasses & Type Hints
> ⏱️ 2-Minute Quick Recap

---

## DATACLASSES

**Definition**: A decorator that auto-generates `__init__`, `__repr__`, `__eq__` for data-holding classes.

**Why use?**
- Eliminates repetitive boilerplate code
- Objects compare by values, not memory address
- Clean string representation for debugging
- Required foundation for Pydantic & FastAPI

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

**Definition**: Annotations specifying expected types for variables, parameters, and return values.

**Why use?**
- `mypy` catches type bugs before runtime
- IDE provides better autocomplete
- Code documents itself
- Defines clear API contracts

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
