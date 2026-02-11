# Additional Notes: CLI Design Patterns

> **Day 8 - Backend Mastery: CLI Task Manager (Part 1)**

---

## Project Structure for CLI Apps

```
task_manager/
├── __init__.py
├── models.py       # Task dataclass
├── manager.py      # TaskManager class (CRUD)
├── storage.py      # JSON persistence
├── cli.py          # argparse/Click interface
└── main.py         # Entry point
```

### Separation of Concerns

| File | Responsibility |
|------|----------------|
| `models.py` | Data structures (what a Task is) |
| `manager.py` | Business logic (what operations exist) |
| `storage.py` | Persistence (how data is saved/loaded) |
| `cli.py` | User interface (how user interacts) |
| `main.py` | Wiring everything together |

---

## Task Dataclass Design

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"

@dataclass
class Task:
    id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    completed_at: Optional[str] = None
    
    def complete(self) -> None:
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status.value,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            status=TaskStatus(data["status"]),
            created_at=data["created_at"],
            completed_at=data.get("completed_at")
        )
```

---

## TaskManager Class

```python
from typing import Optional

class TaskManager:
    def __init__(self, storage):
        self.storage = storage
        self.tasks: list[Task] = []
        self._next_id = 1
        self.load()
    
    def load(self) -> None:
        """Load tasks from storage."""
        data = self.storage.load()
        self.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        self._next_id = data.get("next_id", 1)
    
    def save(self) -> None:
        """Save tasks to storage."""
        self.storage.save({
            "tasks": [t.to_dict() for t in self.tasks],
            "next_id": self._next_id
        })
    
    def add(self, title: str) -> Task:
        """Add a new task."""
        task = Task(id=self._next_id, title=title)
        self._next_id += 1
        self.tasks.append(task)
        self.save()
        return task
    
    def list(self, status: Optional[TaskStatus] = None) -> list[Task]:
        """List tasks, optionally filtered by status."""
        if status:
            return [t for t in self.tasks if t.status == status]
        return self.tasks
    
    def complete(self, task_id: int) -> Task:
        """Mark a task as complete."""
        task = self.get(task_id)
        task.complete()
        self.save()
        return task
    
    def delete(self, task_id: int) -> Task:
        """Delete a task."""
        task = self.get(task_id)
        self.tasks.remove(task)
        self.save()
        return task
    
    def get(self, task_id: int) -> Task:
        """Get a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(task_id)

class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        super().__init__(f"Task #{task_id} not found")
```

---

## Storage Layer

```python
import json
from pathlib import Path

class JSONStorage:
    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = Path(filepath)
    
    def load(self) -> dict:
        """Load data from JSON file."""
        if not self.filepath.exists():
            return {"tasks": [], "next_id": 1}
        
        try:
            return json.loads(self.filepath.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"tasks": [], "next_id": 1}
    
    def save(self, data: dict) -> None:
        """Save data to JSON file."""
        self.filepath.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )
```

---

## CLI Best Practices

### 1. Exit Codes

```python
import sys

def main():
    try:
        # ... app logic ...
        sys.exit(0)  # Success
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)  # General error
    except KeyboardInterrupt:
        sys.exit(130)  # Ctrl+C
```

### 2. Standard Streams

```python
import sys

# Normal output
print("Results go here")

# Errors and warnings
print("Error: Something went wrong", file=sys.stderr)
```

### 3. Colors (Without Dependencies)

```python
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

def success(msg: str):
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")

def error(msg: str):
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")

def warning(msg: str):
    print(f"{Colors.YELLOW}! {msg}{Colors.RESET}")
```

---

## Table Formatting

```python
def print_tasks(tasks: list[Task]) -> None:
    if not tasks:
        print("No tasks found.")
        return
    
    # Header
    print(f"{'ID':>4} {'Status':<10} {'Title':<40} {'Created':<20}")
    print("-" * 80)
    
    # Rows
    for task in tasks:
        status = "✓" if task.status == TaskStatus.COMPLETED else "○"
        created = task.created_at[:10]  # Date only
        print(f"{task.id:>4} {status:<10} {task.title:<40} {created:<20}")
```

---

## Config File Locations

```python
from pathlib import Path
import os

def get_data_dir() -> Path:
    """Get appropriate data directory for the OS."""
    if os.name == "nt":  # Windows
        base = Path(os.environ.get("LOCALAPPDATA", Path.home()))
    else:  # Unix/Linux/Mac
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    
    data_dir = base / "task_manager"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir
```

---

## Key Takeaways

1. **Separate concerns** — Models, business logic, storage, CLI
2. **Use dataclasses** — Clean data modeling with type hints
3. **Enum for status** — Prevents invalid values
4. **JSON persistence** — Simple, human-readable storage
5. **Exit codes** — 0 for success, non-zero for errors
6. **stderr for errors** — Allows output piping
