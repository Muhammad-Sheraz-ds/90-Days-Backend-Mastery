"""
Task Model (v2) — Enhanced with sorting support

Changes from Day 8:
- Added priority field
- Added __lt__ for sorting
- Enhanced __str__ with priority display
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
    @property
    def weight(self) -> int:
        """Numeric weight for sorting (higher = more urgent)."""
        return {"low": 1, "medium": 2, "high": 3}[self.value]


@dataclass
class Task:
    """
    A task with id, title, status, priority, and timestamps.
    
    Enhanced in Day 9 with:
    - priority field (low/medium/high)
    - Sorting support via __lt__
    """
    id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.MEDIUM
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    completed_at: Optional[str] = None
    
    def complete(self) -> None:
        """Mark as completed."""
        if self.status == TaskStatus.COMPLETED:
            return
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status.value,
            "priority": self.priority.value,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            status=TaskStatus(data["status"]),
            priority=Priority(data.get("priority", "medium")),
            created_at=data["created_at"],
            completed_at=data.get("completed_at")
        )
    
    def __str__(self) -> str:
        icon = "✓" if self.status == TaskStatus.COMPLETED else "○"
        pri = {"high": "!!!", "medium": "!!", "low": "!"}[self.priority.value]
        return f"[{icon}] #{self.id} ({pri}) {self.title}"
