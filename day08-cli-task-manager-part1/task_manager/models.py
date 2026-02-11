"""
Task Model

Defines the Task dataclass with status, serialization, and timestamps.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    """Possible states for a task."""
    PENDING = "pending"
    COMPLETED = "completed"


@dataclass
class Task:
    """
    Represents a single task.
    
    Attributes:
        id: Unique identifier
        title: Task description
        status: Current status (pending/completed)
        created_at: ISO timestamp of creation
        completed_at: ISO timestamp of completion (if completed)
    """
    id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    completed_at: Optional[str] = None
    
    def complete(self) -> None:
        """Mark task as completed."""
        if self.status == TaskStatus.COMPLETED:
            return  # Already completed
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status.value,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create Task from dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            status=TaskStatus(data["status"]),
            created_at=data["created_at"],
            completed_at=data.get("completed_at")
        )
    
    def __str__(self) -> str:
        status_icon = "✓" if self.status == TaskStatus.COMPLETED else "○"
        return f"[{status_icon}] #{self.id}: {self.title}"
