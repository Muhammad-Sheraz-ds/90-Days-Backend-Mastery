# Python argparse - CLI Foundations

> **Source**: [Real Python - Command-Line Interfaces with argparse](https://realpython.com/command-line-interfaces-python-argparse/)
> **Day 8 - Backend Mastery: CLI Task Manager (Part 1)**

---

## What is a CLI?

A **Command-Line Interface** allows users to interact with your program through the terminal. Components:

| Component | Example | Purpose |
|-----------|---------|---------|
| Command | `python app.py` | Program to run |
| Argument | `input.txt` | Required input (positional) |
| Option | `--verbose` | Optional behavior modifier |
| Subcommand | `git commit` | Grouped functionality |

---

## argparse Basics

### Four Steps

```python
import argparse

# 1. Create parser
parser = argparse.ArgumentParser(description="My CLI app")

# 2. Add arguments
parser.add_argument("filename")  # Positional (required)

# 3. Add options
parser.add_argument("-v", "--verbose", action="store_true")

# 4. Parse
args = parser.parse_args()

# Access values
print(args.filename)    # Positional argument
print(args.verbose)     # Boolean from --verbose
```

---

## Positional Arguments (Required)

```python
parser.add_argument("name")        # String by default
parser.add_argument("count", type=int)  # Convert to int
parser.add_argument("files", nargs="+")  # Multiple values
```

| `nargs` | Meaning |
|---------|---------|
| `N` | Exactly N arguments |
| `?` | Zero or one |
| `*` | Zero or more |
| `+` | One or more |

---

## Options (Optional)

```python
# Boolean flag (no value needed)
parser.add_argument("-v", "--verbose", action="store_true")

# Option with value
parser.add_argument("-o", "--output", default="out.txt")

# Required option
parser.add_argument("-c", "--config", required=True)
```

### Common Actions

| Action | Result |
|--------|--------|
| `"store"` | Store value (default) |
| `"store_true"` | Store `True` if present |
| `"store_false"` | Store `False` if present |
| `"count"` | Count occurrences (`-vvv` → 3) |
| `"append"` | Collect multiple values |

---

## Type Conversion

```python
# Integer
parser.add_argument("count", type=int)

# Float
parser.add_argument("rate", type=float)

# Choice from list
parser.add_argument("level", choices=["low", "medium", "high"])

# File handling
parser.add_argument("input", type=argparse.FileType('r'))
```

---

## Subcommands (Git-like)

```python
import argparse

parser = argparse.ArgumentParser(prog="task")
subparsers = parser.add_subparsers(dest="command")

# Add subcommand
add_parser = subparsers.add_parser("add", help="Add a task")
add_parser.add_argument("title")

# List subcommand
list_parser = subparsers.add_parser("list", help="List tasks")
list_parser.add_argument("--status", choices=["pending", "done"])

# Parse
args = parser.parse_args()

if args.command == "add":
    print(f"Adding: {args.title}")
elif args.command == "list":
    print(f"Listing with status: {args.status}")
```

**Usage:**
```bash
python task.py add "Buy groceries"
python task.py list --status pending
```

---

## Auto-Generated Help

argparse generates help automatically:

```bash
$ python app.py --help
usage: app.py [-h] [-v] filename

positional arguments:
  filename       Input file

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Enable verbose output
```

Add custom help text:

```python
parser.add_argument(
    "-o", "--output",
    help="Output file path (default: %(default)s)",
    default="output.txt"
)
```

---

## Complete Example: File Lister

```python
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    prog="ls",
    description="List directory contents"
)
parser.add_argument("path", nargs="?", default=".", help="Target directory")
parser.add_argument("-l", "--long", action="store_true", help="Detailed format")
parser.add_argument("-a", "--all", action="store_true", help="Include hidden")

args = parser.parse_args()
target = Path(args.path)

for entry in target.iterdir():
    if not args.all and entry.name.startswith("."):
        continue
    
    if args.long:
        stat = entry.stat()
        print(f"{stat.st_size:>8} {entry.name}")
    else:
        print(entry.name)
```

---

## Key Takeaways

| Concept | Remember |
|---------|----------|
| `add_argument("name")` | Positional (required) |
| `add_argument("-n", "--name")` | Optional (flag format) |
| `action="store_true"` | Boolean flag |
| `type=int` | Type conversion |
| `add_subparsers()` | Git-like subcommands |
| `-h/--help` | Auto-generated help |
