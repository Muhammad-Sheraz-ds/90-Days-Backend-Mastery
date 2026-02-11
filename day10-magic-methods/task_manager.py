import datetime

class Task:
    def __init__(self, id: int, title: str, priority: int = 1):
        self.id = id
        self.title = title
        self.priority = priority
        self.created_at = datetime.datetime.now()

    def __str__(self):
        """User-friendly string representation."""
        return f"[{self.id}] {self.title} (Priority: {self.priority})"

    def __repr__(self):
        """Developer-friendly string representation (unambiguous)."""
        return f"Task(id={self.id}, title='{self.title}', priority={self.priority})"

    def __eq__(self, other):
        """Checks equality based on ID."""
        if not isinstance(other, Task):
            return NotImplemented
        return self.id == other.id

    def __lt__(self, other):
        """Allows sorting by priority (lower number = higher priority)."""
        if not isinstance(other, Task):
            return NotImplemented
        return self.priority < other.priority

class TaskManager:
    def __init__(self):
        self._tasks = []

    def add_task(self, task: Task):
        self._tasks.append(task)

    def __len__(self):
        """Returns the count of tasks."""
        return len(self._tasks)

    def __getitem__(self, index):
        """Allows indexing and iteration (for task in manager)."""
        return self._tasks[index]

    def __repr__(self):
        return f"TaskManager({len(self)} tasks)"

# --- Demo Script ---
if __name__ == "__main__":
    print("--- Demonstrating Magic Methods ---")

    # 1. Comparison (__eq__)
    t1 = Task(1, "Fix Bug", priority=1)
    t2 = Task(1, "Fix Bug", priority=1)
    t3 = Task(2, "Write Docs", priority=2)
    
    print(f"t1 == t2: {t1 == t2}")  # True
    print(f"t1 == t3: {t1 == t3}")  # False

    # 2. String Representation (__str__ vs __repr__)
    print(f"str(t1): {str(t1)}")   # [1] Fix Bug (Priority: 1)
    print(f"repr(t1): {repr(t1)}") # Task(id=1, title='Fix Bug', priority=1)

    # 3. Sorting (__lt__)
    tasks = [
        Task(3, "Low Priority", 10),
        Task(4, "High Priority", 1),
        Task(5, "Medium Priority", 5)
    ]
    print("\nBefore Sorting:")
    for t in tasks: print(t)

    tasks.sort() # Uses __lt__
    print("\nAfter Sorting (by Priority):")
    for t in tasks: print(t)

    # 4. Container Methods (__len__, __getitem__)
    manager = TaskManager()
    manager.add_task(t1)
    manager.add_task(t3)

    print(f"\nManager has {len(manager)} tasks.")
    
    print("Iterating through manager directly:")
    for task in manager: # Uses __getitem__
        print(f" - {task}")
