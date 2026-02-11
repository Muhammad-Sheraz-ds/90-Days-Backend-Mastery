"""
Task Manager

Business logic for managing tasks: add, list, complete, delete.
"""

from typing import Optional

from .models import Task, TaskStatus
from .storage import JSONStorage


class TaskNotFoundError(Exception):
    """Raised when a task with the given ID doesn't exist."""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task #{task_id} not found")


class TaskManager:
    """
    Manages a collection of tasks with persistence.
    
    Provides CRUD operations:
    - add: Create a new task
    - list: Get all tasks (with optional filtering)
    - complete: Mark a task as done
    - delete: Remove a task
    """
    
    def __init__(self, storage: Optional[JSONStorage] = None):
        """
        Initialize the task manager.
        
        Args:
            storage: Storage backend (defaults to JSONStorage)
        """
        self.storage = storage or JSONStorage()
        self.tasks: list[Task] = []
        self._next_id: int = 1
        self._load()
    
    def _load(self) -> None:
        """Load tasks from storage."""
        data = self.storage.load()
        self.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        self._next_id = data.get("next_id", 1)
    
    def _save(self) -> None:
        """Save tasks to storage."""
        data = {
            "tasks": [t.to_dict() for t in self.tasks],
            "next_id": self._next_id
        }
        self.storage.save(data)
    
    def add(self, title: str) -> Task:
        """
        Add a new task.
        
        Args:
            title: Task description
            
        Returns:
            The newly created Task
        """
        task = Task(id=self._next_id, title=title.strip())
        self._next_id += 1
        self.tasks.append(task)
        self._save()
        return task
    
    def list(self, status: Optional[TaskStatus] = None) -> list[Task]:
        """
        Get all tasks, optionally filtered by status.
        
        Args:
            status: Filter by this status (None for all)
            
        Returns:
            List of matching tasks
        """
        if status is None:
            return self.tasks.copy()
        return [t for t in self.tasks if t.status == status]
    
    def get(self, task_id: int) -> Task:
        """
        Get a task by ID.
        
        Args:
            task_id: The task ID to find
            
        Returns:
            The matching Task
            
        Raises:
            TaskNotFoundError: If no task with that ID exists
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(task_id)
    
    def complete(self, task_id: int) -> Task:
        """
        Mark a task as completed.
        
        Args:
            task_id: The task ID to complete
            
        Returns:
            The updated Task
            
        Raises:
            TaskNotFoundError: If no task with that ID exists
        """
        task = self.get(task_id)
        task.complete()
        self._save()
        return task
    
    def delete(self, task_id: int) -> Task:
        """
        Delete a task.
        
        Args:
            task_id: The task ID to delete
            
        Returns:
            The deleted Task
            
        Raises:
            TaskNotFoundError: If no task with that ID exists
        """
        task = self.get(task_id)
        self.tasks.remove(task)
        self._save()
        return task
    
    def count(self, status: Optional[TaskStatus] = None) -> int:
        """
        Count tasks, optionally filtered by status.
        
        Args:
            status: Filter by this status (None for all)
            
        Returns:
            Number of matching tasks
        """
        return len(self.list(status))
