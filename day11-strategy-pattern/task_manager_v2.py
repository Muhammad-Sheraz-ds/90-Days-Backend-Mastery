from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

# --- 1. The Data Model ---
class Task:
    def __init__(self, id: int, title: str, priority: int, created_at: datetime):
        self.id = id
        self.title = title
        self.priority = priority # 1 (High) to 5 (Low)
        self.created_at = created_at

    def __repr__(self):
        return f"Task(id={self.id}, priority={self.priority}, date={self.created_at.strftime('%Y-%m-%d')})"

# --- 2. The Strategy Interface ---
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, tasks: List[Task]) -> List[Task]:
        """Sorts a list of tasks and returns the sorted list."""
        pass

# --- 3. Concrete Strategies ---
class SortByDate(SortStrategy):
    def sort(self, tasks: List[Task]) -> List[Task]:
        # Sort by created_at (ascending)
        return sorted(tasks, key=lambda t: t.created_at)

class SortByPriority(SortStrategy):
    def sort(self, tasks: List[Task]) -> List[Task]:
        # Sort by priority (ascending: 1 is higher than 5)
        return sorted(tasks, key=lambda t: t.priority)

# --- 4. The Context (TaskManager) ---
class TaskManager:
    def __init__(self, strategy: SortStrategy):
        self._tasks = []
        self._strategy = strategy # Composition: TaskManager HAS A SortStrategy

    def add_task(self, task: Task):
        self._tasks.append(task)

    def set_strategy(self, strategy: SortStrategy):
        """Allows changing strategy at runtime."""
        self._strategy = strategy

    def get_tasks(self):
        """Returns tasks sorted by the current strategy."""
        return self._strategy.sort(self._tasks)

# --- Demo Script ---
if __name__ == "__main__":
    # Create Tasks
    t1 = Task(1, "Urgent Bug", priority=1, created_at=datetime(2023, 10, 25))
    t2 = Task(2, "Refactor", priority=3, created_at=datetime(2023, 10, 20)) # Older but lower priority
    t3 = Task(3, "Documentation", priority=2, created_at=datetime(2023, 10, 26))

    # Initialize with Priority Strategy
    manager = TaskManager(SortByPriority())
    manager.add_task(t1)
    manager.add_task(t2)
    manager.add_task(t3)

    print("--- Sorted by Priority (Default) ---")
    for t in manager.get_tasks():
        print(t)
    # Expected: t1 (p1), t3 (p2), t2 (p3)

    # Change Strategy to Date at Runtime
    print("\n--- Switching to Sort by Date ---")
    manager.set_strategy(SortByDate())
    
    for t in manager.get_tasks():
        print(t)
    # Expected: t2 (Oct 20), t1 (Oct 25), t3 (Oct 26)
