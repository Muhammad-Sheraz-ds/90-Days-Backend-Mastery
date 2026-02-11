"""
Task Manager (v2) — Enhanced with filtering, sorting, search, and logging.

Changes from Day 8:
- Filtering by status
- Sorting by date, title, priority, id
- Search by title
- Logging to file
- Input validation
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

from .models import Task, TaskStatus, Priority
from .storage import JSONStorage


# ============================================================================
# Logging Setup
# ============================================================================

logger = logging.getLogger("task_manager")
logger.setLevel(logging.DEBUG)

# File handler (detailed logs)
file_handler = logging.FileHandler("task_manager.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))
logger.addHandler(file_handler)


# ============================================================================
# Custom Exceptions
# ============================================================================

class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task #{task_id} not found")


class ValidationError(Exception):
    pass


# ============================================================================
# Task Manager
# ============================================================================

class TaskManager:
    """
    Manages tasks with CRUD, filtering, sorting, search, and logging.
    """
    
    def __init__(self, storage: Optional[JSONStorage] = None):
        self.storage = storage or JSONStorage()
        self.tasks: list[Task] = []
        self._next_id: int = 1
        self._load()
    
    # ---- Persistence -------------------------------------------------------
    
    def _load(self) -> None:
        data = self.storage.load()
        self.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        self._next_id = data.get("next_id", 1)
        logger.info(f"Loaded {len(self.tasks)} tasks from storage")
    
    def _save(self) -> None:
        data = {
            "tasks": [t.to_dict() for t in self.tasks],
            "next_id": self._next_id
        }
        self.storage.save(data)
        logger.debug("Saved tasks to storage")
    
    # ---- Validation --------------------------------------------------------
    
    @staticmethod
    def _validate_title(title: str) -> str:
        title = title.strip()
        if not title:
            raise ValidationError("Task title cannot be empty")
        if len(title) > 200:
            raise ValidationError("Task title too long (max 200 characters)")
        return title
    
    # ---- CRUD Operations ---------------------------------------------------
    
    def add(self, title: str, priority: str = "medium") -> Task:
        """Add a new task with validation."""
        title = self._validate_title(title)
        pri = Priority(priority)
        
        task = Task(id=self._next_id, title=title, priority=pri)
        self._next_id += 1
        self.tasks.append(task)
        self._save()
        logger.info(f"Added task #{task.id}: '{task.title}' [{pri.value}]")
        return task
    
    def get(self, task_id: int) -> Task:
        """Get a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(task_id)
    
    def complete(self, task_id: int) -> Task:
        """Mark a task as completed."""
        task = self.get(task_id)
        task.complete()
        self._save()
        logger.info(f"Completed task #{task.id}: '{task.title}'")
        return task
    
    def delete(self, task_id: int) -> Task:
        """Delete a task."""
        task = self.get(task_id)
        self.tasks.remove(task)
        self._save()
        logger.warning(f"Deleted task #{task.id}: '{task.title}'")
        return task
    
    # ---- Filtering ---------------------------------------------------------
    
    def list(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[Priority] = None,
    ) -> list[Task]:
        """List tasks with optional filtering."""
        tasks = self.tasks
        
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        if priority is not None:
            tasks = [t for t in tasks if t.priority == priority]
        
        return tasks
    
    # ---- Sorting -----------------------------------------------------------
    
    def sorted_list(
        self,
        tasks: Optional[list[Task]] = None,
        sort_by: str = "id",
        reverse: bool = False,
    ) -> list[Task]:
        """Sort tasks by a field."""
        if tasks is None:
            tasks = self.tasks
        
        sort_keys = {
            "id": lambda t: t.id,
            "title": lambda t: t.title.lower(),
            "date": lambda t: t.created_at,
            "status": lambda t: t.status.value,
            "priority": lambda t: t.priority.weight,
        }
        
        key_func = sort_keys.get(sort_by, sort_keys["id"])
        return sorted(tasks, key=key_func, reverse=reverse)
    
    # ---- Search ------------------------------------------------------------
    
    def search(self, query: str) -> list[Task]:
        """Search tasks by title (case-insensitive)."""
        query = query.lower()
        results = [t for t in self.tasks if query in t.title.lower()]
        logger.debug(f"Search '{query}' returned {len(results)} results")
        return results
    
    # ---- Stats -------------------------------------------------------------
    
    def count(self, status: Optional[TaskStatus] = None) -> int:
        return len(self.list(status))
    
    def stats(self) -> dict:
        """Get task statistics."""
        return {
            "total": len(self.tasks),
            "pending": self.count(TaskStatus.PENDING),
            "completed": self.count(TaskStatus.COMPLETED),
            "high_priority": len([t for t in self.tasks if t.priority == Priority.HIGH]),
        }
