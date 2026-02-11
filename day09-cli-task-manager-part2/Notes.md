# Additional Notes: CLI Best Practices & Patterns

> **Day 9 - Backend Mastery: CLI Task Manager (Part 2)**

---

## CLI UX Best Practices

### 1. Provide Feedback for Every Action

```python
# Bad:  silent operation
manager.add("Task")

# Good: confirm what happened
task = manager.add("Task")
success(f"Added task #{task.id}: {task.title}")
```

### 2. Show Help When No Command Given

```python
if not args.command:
    parser.print_help()
    return 0
```

### 3. Use Exit Codes Consistently

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error |
| `2` | Usage error (bad arguments) |
| `130` | Interrupted (Ctrl+C) |

---

## Table Formatting

### Simple Table

```python
def print_table(tasks: list[Task]) -> None:
    if not tasks:
        print("No tasks found.")
        return
    
    # Header
    header = f"{'ID':>4}  {'Status':<12}  {'Title':<40}  {'Created':<12}"
    print(header)
    print("─" * len(header))
    
    # Rows
    for t in tasks:
        icon = "✓ Done" if t.status == TaskStatus.COMPLETED else "○ Pending"
        date = t.created_at[:10]
        print(f"{t.id:>4}  {icon:<12}  {t.title:<40}  {date}")
```

### Summary Line

```python
total = len(tasks)
done = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
pending = total - done
print(f"\n{total} tasks: {pending} pending, {done} completed")
```

---

## Search Feature

```python
# argparse
list_parser.add_argument(
    "--search", "-q",
    help="Search tasks by title"
)

# Manager method
def search(self, query: str) -> list[Task]:
    query = query.lower()
    return [t for t in self.tasks if query in t.title.lower()]
```

---

## Batch Operations

```python
# Complete multiple tasks
complete_parser.add_argument(
    "task_ids",
    type=int,
    nargs="+",
    help="Task IDs to complete"
)

def cmd_complete(manager, task_ids):
    for tid in task_ids:
        try:
            task = manager.complete(tid)
            success(f"Completed #{tid}: {task.title}")
        except TaskNotFoundError:
            error(f"Task #{tid} not found, skipping")
```

---

## Undo Pattern (Soft Delete)

```python
@dataclass
class Task:
    # ... existing fields ...
    deleted: bool = False
    deleted_at: Optional[str] = None
    
    def soft_delete(self):
        self.deleted = True
        self.deleted_at = datetime.now().isoformat()
    
    def restore(self):
        self.deleted = False
        self.deleted_at = None

# Manager only shows non-deleted by default
def list(self, include_deleted=False):
    tasks = self.tasks
    if not include_deleted:
        tasks = [t for t in tasks if not t.deleted]
    return tasks
```

---

## Configuration via Environment Variables

```python
import os

DEFAULT_FILE = os.environ.get("TASK_FILE", "tasks.json")
LOG_LEVEL = os.environ.get("TASK_LOG_LEVEL", "INFO")

# Usage:
# TASK_FILE=work.json python main.py list
```

---

## README for CLI Project

A good project README should include:

```markdown
# Task Manager CLI

A command-line task manager with JSON persistence.

## Installation
No external dependencies — uses Python 3.10+ standard library.

## Usage
    python main.py add "Buy groceries"
    python main.py list
    python main.py list --status pending --sort date
    python main.py complete 1
    python main.py delete 1

## Features
- Add, list, complete, delete tasks
- Filter by status (pending/completed)
- Sort by date, title, status
- Colored terminal output
- Persistent storage (tasks.json)
- Logging to file (task_manager.log)
```

---

## Key Takeaways

1. **Always give feedback** — Confirm every action
2. **Handle edge cases** — Empty lists, invalid IDs, empty titles
3. **Log to file** — Keep terminal clean, file for debugging
4. **Exit codes matter** — Scripts depend on them
5. **Add search/filter** — Makes CLI genuinely useful
