# Day 10: Python Magic Methods (Dunder Methods)

## 1. What are Magic Methods?
Magic methods (or "dunder" methods, short for **d**ouble **under**score) are special methods in Python that start and end with double underscores (e.g., `__init__`, `__str__`). They allow your custom objects to behave like built-in Python types (lists, dictionaries, numbers).

**Why use them?**
- **Expressiveness:** Code becomes more readable and "Pythonic".
- **Consistency:** Your objects integrate seamlessly with Python's top-level functions (`len()`, `print()`, `sorted()`).
- **Framework Magic:** Backend frameworks like **Django** and **FastAPI** rely heavily on them for things like ORM queries and dependency injection.

---

## 2. String Representation: `__str__` vs `__repr__`

These are the two most important magic methods for debugging and logging.

### `__str__(self)`: The User's View
- **Purpose:** Return a descriptive, readable string for end-users.
- **Called by:** `print()`, `str()`, and f-strings.
- **Goal:** Readability.

```python
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __str__(self):
        return f"User: {self.username} ({self.email})"

u = User("jdoe", "j@example.com")
print(u)  # Output: User: jdoe (j@example.com)
```

### `__repr__(self)`: The Developer's View
- **Purpose:** Return an unambiguous string representation for debugging. Ideally, it should look like valid Python code to recreate the object.
- **Called by:** The interactive shell (REPL), lists/dicts containing the object, and `repr()`.
- **Goal:** Unambiguity.

```python
    def __repr__(self):
        return f"User(username='{self.username}', email='{self.email}')"

# In a list, Python uses __repr__
users = [User("alice", "a@a.com"), User("bob", "b@b.com")]
print(users) 
# Output: [User(username='alice', email='a@a.com'), User(username='bob', email='b@b.com')]
```

> **Best Practice:** Always implement `__repr__`. If `__str__` is missing, Python falls back to `__repr__`.

---

## 3. Comparison Methods: `__eq__` and `__lt__`

To make your objects comparable (sortable, equality checks), implement these methods.

### `__eq__(self, other)`: Equality (`==`)
Allows you to define what makes two objects "equal". For backend entities, this is often the ID or a unique field like email.

```python
class Task:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __eq__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return self.id == other.id

t1 = Task(1, "Buy Milk")
t2 = Task(1, "Buy Milk")
print(t1 == t2)  # True (without __eq__, this would be False because they are different objects in memory)
```

### `__lt__(self, other)`: Less Than (`<`)
Allows sorting (`sorted()`, `.sort()`).

```python
class Task:
    def __init__(self, priority):
        self.priority = priority

    def __lt__(self, other):
        # High priority (1) comes before Low priority (10)
        return self.priority < other.priority

tasks = [Task(3), Task(1), Task(5)]
sorted_tasks = sorted(tasks) # Works because of __lt__
```

---

## 4. Container Methods: `__len__` and `__getitem__`

Make your classes iterable and accessible like lists.

### `__len__(self)`
Called by `len()`. Implementation should return the number of items in the container.

### `__getitem__(self, index)`
Allows indexing (`obj[0]`) and iteration (`for item in obj`).

```python
class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def __len__(self):
        return len(self.tasks)

    def __getitem__(self, index):
        return self.tasks[index]

manager = TaskManager()
manager.add_task("Code")
manager.add_task("Sleep")

print(len(manager))  # 2
print(manager[0])    # "Code"

# __getitem__ makes it iterable automatically!
for t in manager:
    print(t)
```

---

## Practical Backend Application

In **FastAPI** or **Django**, you'll see these patterns often:
1. **Models:** `__str__` is used in the Django Admin interface to display object names.
2. **QuerySets:** Custom collection classes often implement `__iter__` or `__getitem__` to allow looping through database results.
3. **Value Objects:** Money, Coordinates, or other value objects implement `__eq__` to ensure that `Money(5, 'USD') == Money(5, 'USD')`.
