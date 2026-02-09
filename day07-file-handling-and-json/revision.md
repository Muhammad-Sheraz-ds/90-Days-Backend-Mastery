# Day 7 Revision: File Handling & JSON
> ⏱️ 2-Minute Quick Recap

---

## TOPIC DEFINITIONS

### What is File Handling?
**File handling** is the ability to read from and write to files on the filesystem. It involves opening files, performing read/write operations, and properly closing them to prevent resource leaks.

**Purpose**: Store data persistently (survives program restart), process large datasets, create logs, read configuration, and exchange data between systems.

### What is JSON?
**JSON (JavaScript Object Notation)** is a lightweight, text-based data format for storing and exchanging structured data. It's language-independent and human-readable.

**Purpose**: Serialize Python objects to strings/files for storage or transmission, exchange data between APIs and clients, and store configuration settings.

---

## FILE HANDLING

### Opening Files

```python
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
# File automatically closed
```

**Always use `with`** — ensures file closes even on errors.

### File Modes

| Mode | Description |
|------|-------------|
| `'r'` | Read (default) |
| `'w'` | Write (overwrite) |
| `'a'` | Append |
| `'rb'`/`'wb'` | Binary read/write |

### Reading

| Method | Returns |
|--------|---------|
| `f.read()` | Entire file |
| `f.readline()` | Single line |
| `f.readlines()` | List of lines |
| `for line in f:` | Iterate (memory efficient) |

### Writing

```python
with open('out.txt', 'w') as f:
    f.write('Hello\n')
```

---

## JSON

### Core Functions

| Function | Direction |
|----------|-----------|
| `json.dumps(obj)` | Python → JSON string |
| `json.dump(obj, f)` | Python → JSON file |
| `json.loads(s)` | JSON string → Python |
| `json.load(f)` | JSON file → Python |

### Save to File

```python
import json
with open('data.json', 'w') as f:
    json.dump({"name": "Alice"}, f, indent=2)
```

### Load from File

```python
with open('data.json', 'r') as f:
    data = json.load(f)
```

### Type Mapping

| Python | JSON |
|--------|------|
| `dict` | `{}` |
| `list` | `[]` |
| `str` | `"string"` |
| `True/False` | `true/false` |
| `None` | `null` |

---

## ERROR HANDLING

```python
try:
    with open('file.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}  # Default
except json.JSONDecodeError:
    print("Invalid JSON")
```

---

## COMMON MISTAKES

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `open()` without `with` | `with open() as f:` |
| No encoding specified | `encoding='utf-8'` |
| `json.dumps()` to file | `json.dump()` to file |
| Binary mode for text | `'r'`/`'w'` for text |

---

## KEY TERMS

| Term | One-liner |
|------|-----------|
| `with` statement | Context manager for auto-cleanup |
| `open()` | Opens file, returns file object |
| encoding | Character set (use UTF-8) |
| `json.dump()` | Write Python to JSON file |
| `json.load()` | Read JSON file to Python |
| serialization | Python object → JSON |
| deserialization | JSON → Python object |
| `pathlib` | Modern path handling module |
