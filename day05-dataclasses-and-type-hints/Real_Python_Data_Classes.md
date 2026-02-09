# Real Python: Data Classes Guide - Study Notes

> **Source**: [Real Python - Data Classes in Python](https://realpython.com/python-data-classes/)
> **Day 5 - Backend Mastery: Dataclasses & Type Hints**

---

## Why Dataclasses Over Regular Classes?

### Regular Class (Verbose):
```python
class RegularCard:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f'{self.__class__.__name__}(rank={self.rank!r}, suit={self.suit!r})'

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self.rank, self.suit) == (other.rank, other.suit)
```

### Dataclass (Clean):
```python
from dataclasses import dataclass

@dataclass
class DataClassCard:
    rank: str
    suit: str
```

**Result**: Same functionality, 90% less boilerplate.

---

## Alternatives Comparison

| Approach | Pros | Cons |
|----------|------|------|
| `tuple` | Simple | No named access, order-dependent |
| `dict` | Flexible | Key inconsistency, no attribute access |
| `namedtuple` | Immutable, tuple-like | Hard defaults, always immutable |
| `@dataclass` | Full-featured, flexible | Requires type hints |

### Why Not namedtuple?

```python
from collections import namedtuple

Person = namedtuple('Person', ['first_initial', 'last_name'])
Card = namedtuple('Card', ['rank', 'suit'])

# Dangerous! Different types compare as equal:
Person('A', 'Spades') == Card('A', 'Spades')  # True!
```

**Dataclasses avoid this by checking class type in `__eq__`.**

---

## Default Values

```python
@dataclass
class Position:
    name: str
    lon: float = 0.0
    lat: float = 0.0
```

```python
>>> Position('Null Island')
Position(name='Null Island', lon=0.0, lat=0.0)

>>> Position('Greenwich', lat=51.8)
Position(name='Greenwich', lon=0.0, lat=51.8)
```

---

## Type Hints Are Required (But Not Enforced)

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class FlexibleModel:
    name: Any      # Accept anything
    value: Any = 42
```

> [!NOTE]
> Python does **not** enforce types at runtime. Use `mypy` for static checking.

```python
# This runs without error despite wrong types:
>>> Position(3.14, 'pi day', 2018)
Position(name=3.14, lon='pi day', lat=2018)
```

---

## Adding Custom Methods

Dataclasses are regular classes - add any methods you need:

```python
from dataclasses import dataclass
from math import radians, cos, sin, asin, sqrt

@dataclass
class GeoPoint:
    name: str
    lon: float = 0.0
    lat: float = 0.0

    def distance_to(self, other: "GeoPoint") -> float:
        """Calculate distance using Haversine formula."""
        r = 6371  # Earth radius in km
        lam_1, lam_2 = radians(self.lon), radians(other.lon)
        phi_1, phi_2 = radians(self.lat), radians(other.lat)
        h = (sin((phi_2 - phi_1) / 2)**2 +
             cos(phi_1) * cos(phi_2) * sin((lam_2 - lam_1) / 2)**2)
        return 2 * r * asin(sqrt(h))
```

---

## Mutable Default Values with default_factory

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Deck:
    cards: List[str] = field(default_factory=list)  # Safe!
```

> [!CAUTION]
> `cards: List[str] = []` raises `ValueError` - dataclasses protect you!

---

## Ordering and Comparison

Enable comparison operators with `order=True`:

```python
@dataclass(order=True)
class Priority:
    level: int
    name: str
```

```python
>>> Priority(1, 'low') < Priority(5, 'high')
True
```

**Comparison is tuple-based on field order.** For custom ordering:

```python
@dataclass(order=True)
class PlayingCard:
    sort_index: int = field(init=False, repr=False)
    rank: str
    suit: str

    def __post_init__(self):
        RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
        SUITS = '♣ ♢ ♡ ♠'.split()
        self.sort_index = RANKS.index(self.rank) * len(SUITS) + SUITS.index(self.suit)
```

---

## Frozen (Immutable) Dataclasses

```python
@dataclass(frozen=True)
class ImmutablePosition:
    name: str
    lon: float = 0.0
    lat: float = 0.0
```

```python
>>> pos = ImmutablePosition('Oslo', 10.8, 59.9)
>>> pos.name = 'Stockholm'
FrozenInstanceError: cannot assign to field 'name'
```

> [!WARNING]
> Nested mutable objects (like lists) can still be modified!

---

## Inheritance Patterns

```python
@dataclass
class BaseModel:
    id: int
    created_at: str = ""

@dataclass
class User(BaseModel):
    username: str
    email: str = ""  # Must have default (inherited fields have defaults)
```

**Field order in `__init__`**: `name`, `lon`, `lat`, `country`

---

## Slots Optimization for Performance

```python
@dataclass
class SimplePosition:
    name: str
    lon: float
    lat: float

@dataclass
class SlotPosition:
    __slots__ = ['name', 'lon', 'lat']
    name: str
    lon: float
    lat: float
```

| Metric | Regular | Slots |
|--------|---------|-------|
| Memory | 440 bytes | 248 bytes |
| Attribute Access | ~0.09ms | ~0.06ms |

**Python 3.10+**: Use `@dataclass(slots=True)` instead.

---

## Backend Patterns Summary

| Pattern | Use Case |
|---------|----------|
| `@dataclass` | DTOs, Models, Configuration |
| `frozen=True` | API responses, Cache keys, Thread-safe objects |
| `field(default_factory=...)` | Lists, dicts, service dependencies |
| `__post_init__` | Validation, computed fields, transformations |
| `order=True` | Priority queues, sorting, comparison logic |
| `slots=True` | High-performance services, reduced memory |

---

## Key Takeaways for Backend Development

1. **Reduce boilerplate** in data models with `@dataclass`
2. **Always use `default_factory`** for mutable defaults
3. **frozen=True** for immutable response/request models
4. **Type hints required** - enables mypy and IDE support
5. **Foundation for Pydantic** - essential for FastAPI
