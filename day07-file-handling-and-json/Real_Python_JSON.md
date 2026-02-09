# Real Python: Working with JSON - Study Notes

> **Source**: [Real Python - Working with JSON](https://realpython.com/python-json/)
> **Day 7 - Backend Mastery: File Handling & JSON Persistence**

---

## What is JSON?

**JSON (JavaScript Object Notation)** is a lightweight text format for data exchange. It's:
- Human-readable
- Language-independent
- The standard for APIs and web communication

---

## JSON Syntax

```json
{
    "name": "Alice",
    "age": 30,
    "active": true,
    "balance": null,
    "tags": ["python", "backend"],
    "address": {
        "city": "NYC"
    }
}
```

### Rules

| Rule | Example |
|------|---------|
| Keys must be strings | `"name"` not `name` |
| Strings use double quotes | `"hello"` not `'hello'` |
| Boolean is lowercase | `true`/`false` not `True` |
| No trailing commas | `{"a": 1}` not `{"a": 1,}` |

---

## Python ↔ JSON Type Mapping

| Python | JSON |
|--------|------|
| `dict` | `object {}` |
| `list`, `tuple` | `array []` |
| `str` | `string ""` |
| `int`, `float` | `number` |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

> **Note**: JSON keys are always strings. `{1: "a"}` becomes `{"1": "a"}`.

---

## Serialization (Python → JSON)

### To String: `json.dumps()`

```python
import json

data = {"name": "Alice", "age": 30}
json_string = json.dumps(data)
# '{"name": "Alice", "age": 30}'
```

### To File: `json.dump()`

```python
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)
```

---

## Deserialization (JSON → Python)

### From String: `json.loads()`

```python
json_string = '{"name": "Alice", "age": 30}'
data = json.loads(json_string)
# {'name': 'Alice', 'age': 30}
```

### From File: `json.load()`

```python
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

---

## Quick Reference

| Function | Direction | Source/Target |
|----------|-----------|---------------|
| `dumps()` | Python → JSON | Returns string |
| `dump()` | Python → JSON | Writes to file |
| `loads()` | JSON → Python | Parses string |
| `load()` | JSON → Python | Reads from file |

> **Memory trick**: The `s` stands for **s**tring.

---

## Pretty Printing

```python
# Indented, readable output
json_string = json.dumps(data, indent=2)

# With sorted keys
json_string = json.dumps(data, indent=2, sort_keys=True)
```

Output:
```json
{
  "age": 30,
  "name": "Alice"
}
```

---

## Handling Non-Serializable Types

JSON can't serialize `datetime`, `set`, custom objects by default.

### Solution: Custom Encoder

```python
from datetime import datetime
import json

def custom_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Cannot serialize {type(obj)}")

data = {"timestamp": datetime.now()}
json_string = json.dumps(data, default=custom_encoder)
# {"timestamp": "2024-01-15T10:30:00"}
```

### For Dataclasses

```python
from dataclasses import dataclass, asdict
import json

@dataclass
class User:
    name: str
    age: int

user = User("Alice", 30)
json_string = json.dumps(asdict(user))
```

---

## Error Handling

```python
import json

try:
    data = json.loads('{"invalid": }')
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
```

---

## Backend Patterns

### Config File

```python
def load_config(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(path: str, config: dict) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
```

### API Response/Request

```python
# FastAPI returns dict as JSON automatically
@app.get("/users/{id}")
def get_user(id: int) -> dict:
    return {"id": id, "name": "Alice"}

# Parsing incoming JSON
data = json.loads(request_body)
```

---

## Key Takeaways

| Concept | Remember |
|---------|----------|
| `dumps()`/`loads()` | Work with strings |
| `dump()`/`load()` | Work with files |
| Always handle `JSONDecodeError` | Invalid input happens |
| Use `encoding='utf-8'` | JSON standard requires UTF-8 |
| Pretty print with `indent=2` | For debugging/config files |
| Custom encoder for datetime | JSON doesn't support datetime |
