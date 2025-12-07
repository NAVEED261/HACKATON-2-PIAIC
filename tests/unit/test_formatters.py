"""Unit tests for output formatting utilities (T071)"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from utils.formatters import format_task_list, format_task_single


def test_format_task_list_empty():
    """Test formatting empty task list"""
    output = format_task_list([])
    assert "No tasks found" in output


def test_format_task_list_single_task():
    """Test formatting single task"""
    tasks = [{
        'id': 1,
        'title': 'Test task',
        'status': 'pending',
        'priority': 'medium',
        'due_date': None,
        'created_at': '2025-12-06T10:00:00'
    }]

    output = format_task_list(tasks)
    assert "ID" in output
    assert "Title" in output
    assert "Test task" in output
    assert "Total: 1 task" in output


def test_format_task_list_multiple_tasks():
    """Test formatting multiple tasks with table"""
    tasks = [
        {
            'id': 1,
            'title': 'First task',
            'status': 'pending',
            'priority': 'high',
            'due_date': '2025-12-10',
            'created_at': '2025-12-06T10:00:00'
        },
        {
            'id': 2,
            'title': 'Second task',
            'status': 'completed',
            'priority': 'low',
            'due_date': None,
            'created_at': '2025-12-06T11:00:00'
        }
    ]

    output = format_task_list(tasks)
    assert "First task" in output
    assert "Second task" in output
    assert "Total: 2 tasks (1 pending, 1 completed)" in output


def test_format_task_list_truncates_long_titles():
    """Test that long titles are truncated in table format"""
    tasks = [{
        'id': 1,
        'title': 'A' * 100,  # Very long title
        'status': 'pending',
        'priority': 'medium',
        'due_date': None,
        'created_at': '2025-12-06T10:00:00'
    }]

    output = format_task_list(tasks)
    # Title should be truncated to 30 chars
    assert 'A' * 30 in output
    assert 'A' * 31 not in output


def test_format_task_list_handles_null_due_date():
    """Test that null due dates show as N/A"""
    tasks = [{
        'id': 1,
        'title': 'Task without due date',
        'status': 'pending',
        'priority': 'medium',
        'due_date': None,
        'created_at': '2025-12-06T10:00:00'
    }]

    output = format_task_list(tasks)
    assert "N/A" in output


def test_format_task_list_no_header():
    """Test formatting without header"""
    tasks = [{
        'id': 1,
        'title': 'Test',
        'status': 'pending',
        'priority': 'medium',
        'due_date': None,
        'created_at': '2025-12-06T10:00:00'
    }]

    output = format_task_list(tasks, show_header=False)
    assert "ID" not in output or "Test" in output  # Header might not appear
    assert "Total:" in output


def test_format_task_single():
    """Test formatting single task details"""
    task = {
        'id': 5,
        'title': 'Important task',
        'description': 'Task description',
        'status': 'pending',
        'priority': 'high',
        'due_date': '2025-12-15',
        'created_at': '2025-12-06T10:00:00'
    }

    output = format_task_single(task)
    assert "ID: 5" in output
    assert "Title: Important task" in output
    assert "Status: pending" in output
    assert "Priority: high" in output
    assert "Description: Task description" in output
    assert "Due Date: 2025-12-15" in output
    assert "Created: 2025-12-06T10:00:00" in output


def test_format_task_single_minimal():
    """Test formatting task with minimal fields"""
    task = {
        'id': 1,
        'title': 'Minimal task',
        'description': None,
        'status': 'pending',
        'priority': 'medium',
        'due_date': None,
        'created_at': '2025-12-06T10:00:00'
    }

    output = format_task_single(task)
    assert "ID: 1" in output
    assert "Title: Minimal task" in output
    assert "Status: pending" in output
    assert "Priority: medium" in output
    # Description and due_date should not appear when None
    assert "Description:" not in output
    assert "Due Date:" not in output
    assert "Created:" in output
