"""Integration tests for CLI workflows (T026)"""

import sys
from pathlib import Path
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from services.task_service import add_task, list_tasks
from services.storage import load_tasks, save_tasks


TEST_FILE = 'test_workflow.json'


def setup_function():
    """Setup before each test - clean test storage"""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    if os.path.exists('tasks.json'):
        os.remove('tasks.json')


def teardown_function():
    """Cleanup after each test"""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    if os.path.exists('tasks.json'):
        os.remove('tasks.json')


# T026: Integration test for add+list workflow
def test_add_and_list_workflow():
    """Test complete workflow: add tasks then list them"""
    # Add first task
    task1 = add_task(title="First task", priority="high")
    assert task1['id'] == 1
    assert task1['title'] == "First task"

    # Add second task
    task2 = add_task(
        title="Second task",
        description="With description",
        priority="low",
        due_date="2025-12-20"
    )
    assert task2['id'] == 2

    # List all tasks
    all_tasks = list_tasks()
    assert len(all_tasks) == 2
    assert all_tasks[0]['id'] == 1
    assert all_tasks[1]['id'] == 2


def test_add_multiple_tasks_sequential_ids():
    """Test that multiple adds create sequential IDs"""
    task1 = add_task(title="Task 1")
    task2 = add_task(title="Task 2")
    task3 = add_task(title="Task 3")

    assert task1['id'] == 1
    assert task2['id'] == 2
    assert task3['id'] == 3

    all_tasks = list_tasks()
    assert len(all_tasks) == 3


def test_list_filters_by_priority():
    """Test list_tasks with priority filter"""
    add_task(title="High priority task", priority="high")
    add_task(title="Medium priority task", priority="medium")
    add_task(title="Low priority task", priority="low")

    high_tasks = list_tasks(priority="high")
    assert len(high_tasks) == 1
    assert high_tasks[0]['priority'] == "high"


def test_list_filters_by_status():
    """Test list_tasks with status filter"""
    add_task(title="Pending task 1")
    add_task(title="Pending task 2")

    # Mark one as completed (will be implemented in US2, but status can be manually set)
    tasks = load_tasks()
    tasks[0]['status'] = 'completed'
    save_tasks(tasks)

    pending_tasks = list_tasks(status="pending")
    assert len(pending_tasks) == 1

    completed_tasks = list_tasks(status="completed")
    assert len(completed_tasks) == 1


def test_empty_list_returns_empty_array():
    """Test list_tasks returns empty array when no tasks exist"""
    tasks = list_tasks()
    assert tasks == []
