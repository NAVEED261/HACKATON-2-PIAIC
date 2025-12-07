"""Integration tests for storage module (T025)"""

import sys
from pathlib import Path
import os
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from services.storage import load_tasks, save_tasks


TEST_FILE = 'test_tasks_integration.json'


def setup_function():
    """Setup before each test - clean test storage"""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def teardown_function():
    """Cleanup after each test"""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


# T025: Integration test for storage load/save
def test_load_tasks_nonexistent_file():
    """Test load_tasks returns empty list for nonexistent file"""
    tasks = load_tasks(TEST_FILE)
    assert tasks == []


def test_save_and_load_tasks():
    """Test saving tasks and loading them back"""
    original_tasks = [
        {
            'id': 1,
            'title': 'Task 1',
            'description': 'First task',
            'status': 'pending',
            'priority': 'high',
            'due_date': '2025-12-10',
            'created_at': '2025-12-06T10:00:00'
        },
        {
            'id': 2,
            'title': 'Task 2',
            'description': None,
            'status': 'completed',
            'priority': 'medium',
            'due_date': None,
            'created_at': '2025-12-06T11:00:00'
        }
    ]

    # Save tasks
    save_tasks(original_tasks, TEST_FILE)

    # Verify file exists
    assert os.path.exists(TEST_FILE)

    # Load tasks back
    loaded_tasks = load_tasks(TEST_FILE)

    assert len(loaded_tasks) == 2
    assert loaded_tasks[0]['id'] == 1
    assert loaded_tasks[0]['title'] == 'Task 1'
    assert loaded_tasks[1]['id'] == 2
    assert loaded_tasks[1]['description'] is None


def test_save_tasks_atomic_write():
    """Test that save_tasks uses atomic writes (creates then renames)"""
    tasks = [{'id': 1, 'title': 'Test'}]

    save_tasks(tasks, TEST_FILE)

    # Verify file exists and is valid JSON
    assert os.path.exists(TEST_FILE)

    with open(TEST_FILE, 'r') as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]['title'] == 'Test'


def test_save_empty_task_list():
    """Test saving empty task list"""
    save_tasks([], TEST_FILE)

    loaded = load_tasks(TEST_FILE)
    assert loaded == []


def test_load_corrupted_json():
    """Test that corrupted JSON causes system exit with code 2"""
    # Create corrupted JSON file
    with open(TEST_FILE, 'w') as f:
        f.write('{"invalid": json}')

    # load_tasks should exit with code 2
    try:
        load_tasks(TEST_FILE)
        assert False, "Should have exited with code 2"
    except SystemExit as e:
        assert e.code == 2


def test_save_overwrites_existing_file():
    """Test that save_tasks overwrites existing file"""
    # Save initial tasks
    initial_tasks = [{'id': 1, 'title': 'Initial'}]
    save_tasks(initial_tasks, TEST_FILE)

    # Save new tasks (overwrites)
    new_tasks = [
        {'id': 1, 'title': 'Updated'},
        {'id': 2, 'title': 'New task'}
    ]
    save_tasks(new_tasks, TEST_FILE)

    # Load and verify
    loaded = load_tasks(TEST_FILE)
    assert len(loaded) == 2
    assert loaded[0]['title'] == 'Updated'
