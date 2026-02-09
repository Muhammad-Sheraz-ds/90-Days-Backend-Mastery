# Python File I/O Documentation - Study Notes

> **Source**: [Python Input/Output Tutorial](https://docs.python.org/3/tutorial/inputoutput.html)
> **Day 7 - Backend Mastery: File Handling & JSON Persistence**

---

## Opening Files

```python
f = open('workfile', 'w', encoding="utf-8")
```

| Argument | Purpose |
|----------|---------|
| `filename` | Path to file (string) |
| `mode` | How to open (read, write, etc.) |
| `encoding` | Text encoding (use `"utf-8"`) |

---

## File Modes

| Mode | Description |
|------|-------------|
| `'r'` | Read only (default) |
| `'w'` | Write only (overwrites existing) |
| `'a'` | Append (adds to end) |
| `'r+'` | Read and write |
| `'rb'` | Read binary |
| `'wb'` | Write binary |

> **UTF-8**: Always use `encoding="utf-8"` for text files (modern standard).

---

## Context Manager (`with` Statement)

**Always use `with`** — automatically closes file even on exceptions:

```python
# ✅ Correct way
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
# File automatically closed here

# ❌ Risky way (file may stay open)
f = open('file.txt')
content = f.read()
f.close()  # Might never run if exception above
```

**Why?** Without `with`, data may not be written to disk if program crashes.

---

## Reading Files

| Method | Returns |
|--------|---------|
| `f.read()` | Entire file as string |
| `f.read(n)` | First n characters |
| `f.readline()` | Single line (includes `\n`) |
| `f.readlines()` | List of all lines |

```python
# Read entire file
with open('data.txt', 'r') as f:
    content = f.read()

# Read line by line (memory efficient)
with open('data.txt', 'r') as f:
    for line in f:
        print(line.strip())

# Read all lines as list
with open('data.txt', 'r') as f:
    lines = f.readlines()
```

---

## Writing Files

```python
# Write (overwrite)
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write('Hello\n')
    f.write('World\n')

# Append
with open('log.txt', 'a', encoding='utf-8') as f:
    f.write('New log entry\n')
```

`f.write()` returns number of characters written.

---

## File Position

| Method | Purpose |
|--------|---------|
| `f.tell()` | Current position in bytes |
| `f.seek(offset)` | Move to position |
| `f.seek(0)` | Go to beginning |
| `f.seek(0, 2)` | Go to end |

---

## Binary Mode

Use for images, PDFs, executables:

```python
# Read binary
with open('image.png', 'rb') as f:
    data = f.read()  # Returns bytes

# Write binary
with open('copy.png', 'wb') as f:
    f.write(data)
```

> **Warning**: Don't use text mode for binary files — it will corrupt them.

---

## JSON with Files

```python
import json

# Save Python object to JSON file
data = {'name': 'Alice', 'age': 30}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)

# Load JSON file to Python object
with open('data.json', 'r', encoding='utf-8') as f:
    loaded = json.load(f)
```

| Function | Purpose |
|----------|---------|
| `json.dump(obj, file)` | Write to file |
| `json.load(file)` | Read from file |
| `json.dumps(obj)` | Convert to string |
| `json.loads(string)` | Parse from string |

---

## Error Handling

```python
try:
    with open('file.txt', 'r') as f:
        content = f.read()
except FileNotFoundError:
    print("File doesn't exist")
except PermissionError:
    print("No permission to read file")
except json.JSONDecodeError:
    print("Invalid JSON format")
```

---

## Backend Best Practices

| Practice | Reason |
|----------|--------|
| Always use `with` statement | Prevents resource leaks |
| Use `encoding='utf-8'` | Cross-platform compatibility |
| Handle `FileNotFoundError` | Graceful error handling |
| Use `'rb'`/`'wb'` for binary | Prevents corruption |
| Close files explicitly in loops | Avoid hitting file limits |
