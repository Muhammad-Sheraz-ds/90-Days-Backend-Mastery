# Day 8 Revision: CLI Task Manager (Part 1)
> ⏱️ 2-Minute Quick Recap

---

## TOPIC DEFINITIONS

### What is a CLI (Command-Line Interface)?
A **CLI** is a text-based interface where users interact with a program by typing commands in a terminal/console, rather than using a graphical interface.

**Purpose**: Automate tasks, create developer tools, build scripts, and control applications without a GUI.

### What is argparse?
**argparse** is Python's standard library module for parsing command-line arguments and options. It automatically handles help text, type conversion, and validation.

**Purpose**: Build professional CLI applications that accept user input from the terminal.

---

## ARGPARSE QUICK REFERENCE

### Basic Pattern

```python
import argparse

parser = argparse.ArgumentParser(description="My app")
parser.add_argument("filename")         # Positional (required)
parser.add_argument("-v", "--verbose", action="store_true")  # Flag
args = parser.parse_args()
```

### Key Components

| Type | Syntax | Example |
|------|--------|---------|
| Argument | `"name"` | `parser.add_argument("file")` |
| Option | `"-n"` / `"--name"` | `parser.add_argument("-o", "--output")` |
| Flag | `action="store_true"` | `--verbose` → `True` |

### Subcommands

```python
subparsers = parser.add_subparsers(dest="command")
add_parser = subparsers.add_parser("add")
add_parser.add_argument("title")
```

---

## TASK MANAGER STRUCTURE

```
task_manager/
├── models.py    # Task dataclass
├── manager.py   # TaskManager (CRUD)
├── storage.py   # JSON persistence
├── cli.py       # argparse commands
└── main.py      # Entry point
```

---

## KEY PATTERNS

### Dataclass with Serialization

```python
@dataclass
class Task:
    id: int
    title: str
    
    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title}
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(**data)
```

### Manager Save/Load

```python
def _load(self):
    data = self.storage.load()
    self.tasks = [Task.from_dict(t) for t in data["tasks"]]

def _save(self):
    self.storage.save({"tasks": [t.to_dict() for t in self.tasks]})
```

---

## COMMON MISTAKES

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| Mixing CLI and logic | Separate into layers |
| No error handling | Catch `TaskNotFoundError` |
| Forgetting `_save()` | Save after every mutation |
| Hardcoded file paths | Accept via storage class |

---

## CLI COMMANDS

```bash
# Add task
python main.py add "Buy groceries"

# List all
python main.py list

# List pending only
python main.py list --status pending

# Complete task
python main.py complete 1

# Delete task
python main.py delete 1
```

---

## KEY TERMS

| Term | One-liner |
|------|-----------|
| argparse | Standard library for CLI parsing |
| Subcommand | Nested command (`git commit`) |
| Positional | Required argument by position |
| Option/Flag | Optional argument with `-` prefix |
| Exit code | 0=success, non-zero=error |
