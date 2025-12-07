"""Unit tests for task service functions (T023, T024)"""

import sys
from pathlib import Path
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from services.task_service import get_next_id, create_task


def setup_function():
    """Setup before each test - clean test storage"""
    if os.path.exists('tasks.json'):
        os.remove('tasks.json')


def teardown_function():
    """Cleanup after each test"""
    if os.path.exists('tasks.json'):
        os.remove('tasks.json')


# T023: Unit test for get_next_id
def test_get_next_id_empty_list():
    """Test get_next_id returns 1 for empty task list"""
    assert get_next_id([]) == 1


def test_get_next_id_existing_tasks():
    """Test get_next_id returns max ID + 1"""
    tasks = [
        {'id': 1, 'title': 'Task 1'},
        {'id': 3, 'title': 'Task 3'},
        {'id': 2, 'title': 'Task 2'}
    ]
    assert get_next_id(tasks) == 4


def test_get_next_id_single_task():
    """Test get_next_id with single task"""
    tasks = [{'id': 5, 'title': 'Only task'}]
    assert get_next_id(tasks) == 6


# T024: Unit test for create_task
def test_create_task_minimal():
    """Test create_task with minimal fields"""
    task = create_task(title="Test task")

    assert task['id'] == 1  # First task
    assert task['title'] == "Test task"
    assert task['description'] is None
    assert task['status'] == 'pending'
    assert task['priority'] == 'medium'
    assert task['due_date'] is None
    assert 'created_at' in task


def test_create_task_full():
    """Test create_task with all fields"""
    task = create_task(
        title="Full task",
        description="Complete description",
        priority="high",
        due_date="2025-12-15"
    )

    assert task['title'] == "Full task"
    assert task['description'] == "Complete description"
    assert task['priority'] == "high"
    assert task['due_date'] == "2025-12-15"
    assert task['status'] == 'pending'


def test_create_task_empty_title():
    """Test create_task rejects empty title"""
    try:
        create_task(title="")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Title cannot be empty" in str(e)


def test_create_task_invalid_priority():
    """Test create_task rejects invalid priority"""
    try:
        create_task(title="Task", priority="urgent")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Priority must be one of" in str(e)


def test_create_task_invalid_date():
    """Test create_task rejects invalid date format"""
    try:
        create_task(title="Task", due_date="12/31/2025")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Invalid date format" in str(e)


def test_create_task_long_title():
    """Test create_task rejects title over 200 characters"""
    long_title = "A" * 201

    try:
        create_task(title=long_title)
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "200 characters" in str(e)


def test_create_task_incremental_ids():
    """Test that multiple create_task calls read current state from storage"""
    # First task creation (storage empty)
    task1 = create_task(title="Task 1")
    assert task1['id'] == 1

    # Second create without saving - still reads from empty storage
    task2 = create_task(title="Task 2")
    assert task2['id'] == 1  # Same ID since first task wasn't saved

    # Note: Use add_task() for persistent incremental IDs (tested in integration tests)
