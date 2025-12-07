"""Task entity model for Phase 1 Console Todo App

This module defines the Task data structure with 7 fields designed for
Phase 2 PostgreSQL migration.
"""

from datetime import datetime
from typing import Optional


class Task:
    """Task entity with all 7 fields from data-model.md"""

    def __init__(
        self,
        id: int,
        title: str,
        description: Optional[str] = None,
        status: str = "pending",
        priority: str = "medium",
        due_date: Optional[str] = None,
        created_at: Optional[str] = None
    ):
        """Initialize a Task instance

        Args:
            id: Unique sequential integer ID
            title: Task title (required, max 200 chars)
            description: Task description (optional, max 1000 chars)
            status: Task status ("pending" or "completed")
            priority: Priority level ("low", "medium", "high")
            due_date: Due date in ISO 8601 format (YYYY-MM-DD)
            created_at: Creation timestamp (auto-generated if not provided)
        """
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.created_at = created_at or self._generate_timestamp()

    @staticmethod
    def _generate_timestamp() -> str:
        """Generate current timestamp in ISO 8601 format"""
        return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

    def to_dict(self) -> dict:
        """Convert Task instance to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create Task instance from dictionary

        Args:
            data: Dictionary with task fields

        Returns:
            Task instance
        """
        return cls(
            id=data['id'],
            title=data['title'],
            description=data.get('description'),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'medium'),
            due_date=data.get('due_date'),
            created_at=data.get('created_at')
        )
