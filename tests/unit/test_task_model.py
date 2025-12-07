"""Unit tests for Task model (T019)"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from models.task import Task


def test_task_creation_minimal():
    """Test Task creation with minimal required fields"""
    task = Task(id=1, title="Test task")

    assert task.id == 1
    assert task.title == "Test task"
    assert task.description is None
    assert task.status == "pending"
    assert task.priority == "medium"
    assert task.due_date is None
    assert task.created_at is not None


def test_task_creation_full():
    """Test Task creation with all fields"""
    task = Task(
        id=2,
        title="Complete task",
        description="Full description",
        status="completed",
        priority="high",
        due_date="2025-12-15",
        created_at="2025-12-06T10:00:00"
    )

    assert task.id == 2
    assert task.title == "Complete task"
    assert task.description == "Full description"
    assert task.status == "completed"
    assert task.priority == "high"
    assert task.due_date == "2025-12-15"
    assert task.created_at == "2025-12-06T10:00:00"


def test_task_to_dict():
    """Test Task.to_dict() conversion"""
    task = Task(id=1, title="Test", priority="low")
    task_dict = task.to_dict()

    assert task_dict['id'] == 1
    assert task_dict['title'] == "Test"
    assert task_dict['priority'] == "low"
    assert task_dict['status'] == "pending"
    assert 'created_at' in task_dict


def test_task_from_dict():
    """Test Task.from_dict() creation"""
    data = {
        'id': 3,
        'title': "From dict",
        'description': "Test description",
        'status': 'pending',
        'priority': 'medium',
        'due_date': None,
        'created_at': '2025-12-06T12:00:00'
    }

    task = Task.from_dict(data)

    assert task.id == 3
    assert task.title == "From dict"
    assert task.description == "Test description"
    assert task.created_at == '2025-12-06T12:00:00'
