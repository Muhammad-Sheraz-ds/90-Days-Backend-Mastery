# Real Python: Reading and Writing Files - Study Notes

> **Source**: [Real Python - Reading and Writing Files](https://realpython.com/read-write-files-python/)
> **Day 7 - Backend Mastery: File Handling & JSON Persistence**

---

## What is a File?

A file is a contiguous set of bytes for storing data. At its core:
- **Header**: Metadata (name, size, type)
- **Data**: The actual content
- **End of File (EOF)**: Special marker

---

## File Paths

| Component | Example |
|-----------|---------|
| Folder path | `/home/user/docs/` |
| Filename | `report` |
| Extension | `.txt` |
| Full path | `/home/user/docs/report.txt` |

```python
import os

# Get current directory
current = os.getcwd()

# Join paths (cross-platform)
path = os.path.join('folder', 'file.txt')
```

---

## Opening and Closing Files

### The Problem (Without `with`)

```python
reader = open('file.txt')
try:
    # Process file
    data = reader.read()
finally:
    reader.close()  # Must always close!
```

### The Solution (With `with`)

```python
with open('file.txt', 'r') as reader:
    data = reader.read()
# Automatically closed here, even on error
```

> **Always use `with`** — it's cleaner and safer.

---

## File Object Types

| Type | Description | Example Mode |
|------|-------------|--------------|
| Text files | Human-readable strings | `'r'`, `'w'` |
| Buffered binary | Images, audio, PDFs | `'rb'`, `'wb'` |
| Raw binary | Low-level access | `'rb'` (unbuffered) |

---

## Reading Methods

```python
with open('file.txt', 'r') as f:
    # Read entire file
    content = f.read()
    
    # Read specific characters
    chunk = f.read(100)  # First 100 chars
    
    # Read single line
    line = f.readline()
    
    # Read all lines as list
    lines = f.readlines()
    
    # Iterate efficiently (memory-friendly)
    for line in f:
        process(line)
```

### Comparison

| Method | Returns | Memory |
|--------|---------|--------|
| `.read()` | Entire file string | High |
| `.readline()` | Single line | Low |
| `.readlines()` | List of lines | High |
| `for line in f:` | One line at a time | Low |

---

## Writing Methods

```python
with open('output.txt', 'w') as f:
    # Write string
    f.write('Line 1\n')
    
    # Write multiple lines
    lines = ['a\n', 'b\n', 'c\n']
    f.writelines(lines)
```

---

## Working with Two Files

```python
# Copy file content
with open('source.txt', 'r') as reader:
    with open('dest.txt', 'w') as writer:
        for line in reader:
            writer.write(line)

# Or more concisely
with open('source.txt', 'r') as src, open('dest.txt', 'w') as dst:
    dst.write(src.read())
```

---

## Appending to File

```python
# 'a' mode adds to end, doesn't overwrite
with open('log.txt', 'a') as f:
    f.write('New entry\n')
```

---

## `__file__` Attribute

Get the path of the current Python script:

```python
# Get directory containing this script
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build path relative to script
data_path = os.path.join(script_dir, 'data', 'file.txt')
```

---

## Creating Custom Context Manager

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        return False  # Don't suppress exceptions

# Usage
with FileManager('file.txt', 'r') as f:
    content = f.read()
```

---

## Key Takeaways

| Concept | What to Remember |
|---------|------------------|
| `with open()` | Always use for automatic cleanup |
| Iterating | Use `for line in f:` for large files |
| Binary mode | Use `'rb'`/`'wb'` for non-text files |
| Encoding | Specify `encoding='utf-8'` explicitly |
| `__file__` | Get script's directory path |
