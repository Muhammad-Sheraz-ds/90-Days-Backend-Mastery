# CLI Filtering, Sorting & Polish

> **Day 9 - Backend Mastery: CLI Task Manager (Part 2)**
> **Focus**: Extend Day 8 with filtering, sorting, error messages, and logging

---

## Filtering Patterns

### By Status

```python
def list_tasks(status: Optional[str] = None) -> list[Task]:
    """Filter tasks by status."""
    if status is None:
        return self.tasks
    return [t for t in self.tasks if t.status.value == status]
```

### argparse with Choices

```python
list_parser.add_argument(
    "--status", "-s",
    choices=["pending", "completed", "all"],
    default="all",
    help="Filter by status"
)
```

### Multiple Filters (Chaining)

```python
def list_tasks(
    status: Optional[str] = None,
    search: Optional[str] = None,
) -> list[Task]:
    tasks = self.tasks
    
    if status:
        tasks = [t for t in tasks if t.status.value == status]
    if search:
        tasks = [t for t in tasks if search.lower() in t.title.lower()]
    
    return tasks
```

---

## Sorting Patterns

### By Date

```python
from datetime import datetime

def sort_by_date(tasks: list[Task], reverse: bool = False) -> list[Task]:
    """Sort tasks by creation date."""
    return sorted(
        tasks,
        key=lambda t: datetime.fromisoformat(t.created_at),
        reverse=reverse
    )
```

### By Multiple Fields

```python
def sort_tasks(tasks: list[Task], sort_by: str = "date") -> list[Task]:
    """Sort tasks by different criteria."""
    if sort_by == "date":
        return sorted(tasks, key=lambda t: t.created_at)
    elif sort_by == "title":
        return sorted(tasks, key=lambda t: t.title.lower())
    elif sort_by == "status":
        return sorted(tasks, key=lambda t: t.status.value)
    elif sort_by == "id":
        return sorted(tasks, key=lambda t: t.id)
    return tasks
```

### argparse Sort Option

```python
list_parser.add_argument(
    "--sort",
    choices=["date", "title", "status", "id"],
    default="id",
    help="Sort tasks by field (default: id)"
)
list_parser.add_argument(
    "--reverse", "-r",
    action="store_true",
    help="Reverse sort order"
)
```

---

## Polishing Error Messages

### Consistent Error Format

```python
import sys

def error(msg: str) -> None:
    print(f"\033[91m✗ Error:\033[0m {msg}", file=sys.stderr)

def warning(msg: str) -> None:
    print(f"\033[93m! Warning:\033[0m {msg}", file=sys.stderr)

def success(msg: str) -> None:
    print(f"\033[92m✓\033[0m {msg}")

def info(msg: str) -> None:
    print(f"\033[96mℹ\033[0m {msg}")
```

### User-Friendly Errors

```python
def cmd_complete(manager, task_id):
    try:
        task = manager.complete(task_id)
        success(f"Completed: {task.title}")
    except TaskNotFoundError:
        error(f"No task with ID #{task_id}. Use 'list' to see available tasks.")
        return 1
    return 0
```

### Input Validation

```python
def validate_title(title: str) -> str:
    """Validate and clean task title."""
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty")
    if len(title) > 200:
        raise ValueError("Task title too long (max 200 characters)")
    return title
```

---

## Adding Logging

```python
import logging

# Configure logging to file
logging.basicConfig(
    filename="task_manager.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# In operations:
def add(self, title: str) -> Task:
    task = Task(id=self._next_id, title=title)
    self.tasks.append(task)
    self._save()
    logger.info(f"Added task #{task.id}: {task.title}")
    return task

def delete(self, task_id: int) -> Task:
    task = self.get(task_id)
    self.tasks.remove(task)
    self._save()
    logger.warning(f"Deleted task #{task.id}: {task.title}")
    return task
```

---

## Advanced argparse Features

### Mutually Exclusive Options

```python
group = list_parser.add_mutually_exclusive_group()
group.add_argument("--pending", action="store_true")
group.add_argument("--completed", action="store_true")
```

### Aliases

```python
subparsers.add_parser("ls", help="Alias for list")
subparsers.add_parser("rm", help="Alias for delete")
subparsers.add_parser("done", help="Alias for complete")
```

### Epilog (Usage Examples)

```python
parser = argparse.ArgumentParser(
    prog="task",
    description="A CLI task manager",
    epilog="""
Examples:
  task add "Buy groceries"
  task list --status pending
  task complete 1
  task delete 2
"""
)
```

---

## Key Takeaways

| Feature | Implementation |
|---------|---------------|
| Filter | List comprehension with conditions |
| Sort | `sorted()` with `key=lambda` |
| Colors | ANSI escape codes |
| Logging | `logging` module to file |
| Validation | Strip, length checks, early return |
| Error messages | Helpful context + next steps |
