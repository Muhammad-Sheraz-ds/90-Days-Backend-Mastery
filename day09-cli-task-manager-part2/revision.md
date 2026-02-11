# Day 9 Revision: CLI Task Manager (Part 2)
> ⏱️ 2-Minute Quick Recap

---

## TOPIC DEFINITIONS

### What is Filtering?
**Filtering** is selecting a subset of data that matches specific criteria using conditional logic (list comprehensions, `filter()`).

**Purpose**: Let users narrow down results to what's relevant (e.g., show only pending tasks).

### What is Sorting?
**Sorting** rearranges data items by a key field using `sorted()` with a `key` function.

**Purpose**: Present data in a meaningful order (by date, priority, name).

---

## FILTERING

```python
# By status
tasks = [t for t in self.tasks if t.status == TaskStatus.PENDING]

# By priority
tasks = [t for t in tasks if t.priority == Priority.HIGH]

# Chained
def list(self, status=None, priority=None):
    tasks = self.tasks
    if status:
        tasks = [t for t in tasks if t.status == status]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    return tasks
```

---

## SORTING

```python
# By date
sorted(tasks, key=lambda t: t.created_at)

# By priority weight
sorted(tasks, key=lambda t: t.priority.weight, reverse=True)

# By multiple criteria
sort_keys = {
    "id":       lambda t: t.id,
    "title":    lambda t: t.title.lower(),
    "priority": lambda t: t.priority.weight,
}
sorted(tasks, key=sort_keys[sort_by], reverse=reverse)
```

---

## SEARCH

```python
def search(self, query: str) -> list[Task]:
    query = query.lower()
    return [t for t in self.tasks if query in t.title.lower()]
```

---

## WHAT'S NEW IN V2

| Feature | Day 8 | Day 9 |
|---------|-------|-------|
| Priority | ✗ | ✓ (low/medium/high) |
| Filtering | ✗ | ✓ (`--status`, `--priority`) |
| Sorting | ✗ | ✓ (`--sort`, `--reverse`) |
| Search | ✗ | ✓ (`--search`) |
| Batch complete | ✗ | ✓ (multiple IDs) |
| Stats command | ✗ | ✓ |
| Aliases | ✗ | ✓ (`ls`, `rm`, `done`) |
| Logging | ✗ | ✓ (to `task_manager.log`) |
| Validation | Basic | Title length + empty check |

---

## CLI COMMANDS

```bash
# Add with priority
python main.py add "Fix bug" --priority high

# Filter + sort
python main.py list --status pending --sort priority --reverse

# Search
python main.py list --search "grocery"

# Batch complete
python main.py complete 1 2 3

# Stats
python main.py stats
```

---

## COMMON MISTAKES

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| No feedback after action | Print success/error message |
| Silent failures | Log errors + user message |
| `print()` for errors | `print(..., file=sys.stderr)` |
| No validation | Check title, IDs, priorities |

---

## KEY TERMS

| Term | One-liner |
|------|-----------|
| Filtering | Selecting data matching criteria |
| Sorting | Ordering data by a key field |
| `sorted()` | Python built-in, returns new list |
| `key=lambda` | Function defining sort order |
| `nargs="+"` | argparse: one or more values |
| Aliases | Alternative command names |
| Exit codes | 0=ok, 1=error |
