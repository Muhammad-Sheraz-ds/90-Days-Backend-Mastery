# Additional Notes: File Handling & JSON

> **Day 7 - Backend Mastery: Supplementary Resources**

---

## pathlib: Modern Path Handling

`pathlib` is the modern way to handle paths (Python 3.4+):

```python
from pathlib import Path

# Create path object
data_dir = Path('data')
file_path = data_dir / 'users.json'  # Join with /

# Check existence
if file_path.exists():
    content = file_path.read_text(encoding='utf-8')

# Write file
file_path.write_text('Hello', encoding='utf-8')

# Get parts
print(file_path.name)      # 'users.json'
print(file_path.stem)      # 'users'
print(file_path.suffix)    # '.json'
print(file_path.parent)    # 'data'

# Create directories
data_dir.mkdir(parents=True, exist_ok=True)
```

### pathlib vs os.path

| os.path | pathlib |
|---------|---------|
| `os.path.join('a', 'b')` | `Path('a') / 'b'` |
| `os.path.exists(path)` | `path.exists()` |
| `os.makedirs(path)` | `path.mkdir(parents=True)` |
| `os.path.basename(path)` | `path.name` |

---

## Working with CSV

```python
import csv

# Write CSV
with open('data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'age'])  # Header
    writer.writerow(['Alice', 30])
    writer.writerow(['Bob', 25])

# Read CSV
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        print(row)  # ['Alice', '30']

# DictReader for named access
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'], row['age'])
```

---

## JSON Best Practices for APIs

### Consistent Date Format

```python
from datetime import datetime
import json

def datetime_serializer(obj):
    """ISO 8601 format for all datetimes."""
    if isinstance(obj, datetime):
        return obj.isoformat() + 'Z'  # UTC indicator
    raise TypeError(f"Type {type(obj)} not serializable")

json.dumps(data, default=datetime_serializer)
```

### Pretty vs Compact

```python
# Development: Pretty for debugging
json.dumps(data, indent=2)

# Production: Compact for efficiency
json.dumps(data, separators=(',', ':'))
```

---

## Atomic File Writes

Prevents corrupted files if write fails mid-way:

```python
import json
import os
from tempfile import NamedTemporaryFile

def save_json_atomic(path: str, data: dict) -> None:
    """Write JSON atomically — all or nothing."""
    dir_name = os.path.dirname(path) or '.'
    
    with NamedTemporaryFile('w', dir=dir_name, delete=False) as tmp:
        json.dump(data, tmp, indent=2)
        temp_path = tmp.name
    
    os.replace(temp_path, path)  # Atomic rename
```

---

## Large File Handling

### Streaming JSON (for huge files)

```python
import ijson  # pip install ijson

# Parse large JSON file without loading all into memory
with open('huge.json', 'rb') as f:
    for item in ijson.items(f, 'users.item'):
        process(item)
```

### Line-by-line Processing

```python
# Process log file without loading all into memory
with open('server.log', 'r') as f:
    for line in f:
        if 'ERROR' in line:
            print(line.strip())
```

---

## File Locking (Multi-process Safety)

```python
import fcntl  # Unix only
import json

def read_json_locked(path: str) -> dict:
    with open(path, 'r') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)  # Shared lock
        data = json.load(f)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    return data

def write_json_locked(path: str, data: dict) -> None:
    with open(path, 'w') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock
        json.dump(data, f, indent=2)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
```

---

## Configuration Management Pattern

```python
from dataclasses import dataclass, asdict
from pathlib import Path
import json

@dataclass
class AppConfig:
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    
    @classmethod
    def load(cls, path: Path) -> "AppConfig":
        if path.exists():
            data = json.loads(path.read_text())
            return cls(**data)
        return cls()  # Defaults
    
    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), indent=2))

# Usage
config = AppConfig.load(Path('config.json'))
config.debug = True
config.save(Path('config.json'))
```

---

## Environment-Specific Configs

```python
import os
import json
from pathlib import Path

def load_config() -> dict:
    env = os.getenv('APP_ENV', 'development')
    config_path = Path(f'config.{env}.json')
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file for '{env}' not found")
    
    return json.loads(config_path.read_text())
```

---

## Key Takeaways

1. **Use `pathlib`** — Modern, readable path operations
2. **Always specify encoding** — `encoding='utf-8'` everywhere
3. **Use atomic writes** — Prevent corrupted files
4. **Stream large files** — Don't load everything into memory
5. **Handle errors** — `FileNotFoundError`, `JSONDecodeError`
6. **Lock files** — When multiple processes access same file
