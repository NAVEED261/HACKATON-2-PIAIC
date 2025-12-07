"""Contract tests for CLI interface

Tests the command-line interface contracts as specified in contracts/cli-commands.md
"""

import subprocess
import sys
import json
import os
from pathlib import Path


TEST_STORAGE_FILE = 'test_tasks.json'


def run_cli(args, input_text=None):
    """Helper to run CLI command and capture output

    Args:
        args: List of command arguments
        input_text: Optional input for prompts

    Returns:
        Result object with exit_code, output, error
    """
    cmd = [sys.executable, 'src/todo_cli.py'] + args

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        input=input_text
    )

    class Result:
        def __init__(self, returncode, stdout, stderr):
            self.exit_code = returncode
            self.output = stdout
            self.error = stderr

    return Result(result.returncode, result.stdout, result.stderr)


def setup_function():
    """Setup before each test - clean test storage"""
    if os.path.exists(TEST_STORAGE_FILE):
        os.remove(TEST_STORAGE_FILE)
    if os.path.exists('tasks.json'):
        os.remove('tasks.json')


def teardown_function():
    """Cleanup after each test"""
    if os.path.exists(TEST_STORAGE_FILE):
        os.remove(TEST_STORAGE_FILE)
    if os.path.exists('tasks.json'):
        os.remove('tasks.json')


# T013: Contract test for "add minimal task"
def test_add_task_minimal():
    """Test adding a task with only title (minimal required fields)"""
    result = run_cli(['add', 'Buy groceries'])

    assert result.exit_code == 0
    assert "Task added successfully" in result.output
    assert "ID:" in result.output
    assert "Title: Buy groceries" in result.output
    assert "Status: pending" in result.output


# T014: Contract test for "add full task with all options"
def test_add_task_full():
    """Test adding a task with all optional fields"""
    result = run_cli([
        'add',
        'Submit report',
        '-d', 'Q4 analysis',
        '--due-date', '2025-12-15',
        '-p', 'high'
    ])

    assert result.exit_code == 0
    assert "Task added successfully" in result.output
    assert "ID:" in result.output


# T015: Contract test for "add task with empty title error"
def test_add_task_empty_title():
    """Test that empty title produces error"""
    result = run_cli(['add', ''])

    assert result.exit_code == 1
    assert "Title cannot be empty" in result.output or "Title cannot be empty" in result.error


# T016: Contract test for "add task with invalid date error"
def test_add_task_invalid_date():
    """Test that invalid date format produces error"""
    result = run_cli(['add', 'Task', '--due-date', '12/31/2025'])

    assert result.exit_code == 1
    assert "Invalid date format" in result.output or "Invalid date format" in result.error


# T017: Contract test for "list all tasks"
def test_list_all_tasks():
    """Test listing all tasks shows table format"""
    # Add some tasks first
    run_cli(['add', 'Task 1'])
    run_cli(['add', 'Task 2'])

    result = run_cli(['list'])

    assert result.exit_code == 0
    assert "ID" in result.output
    assert "Title" in result.output
    assert "Task 1" in result.output
    assert "Task 2" in result.output
    assert "Total:" in result.output


# T018: Contract test for "list empty tasks"
def test_list_empty():
    """Test listing when no tasks exist"""
    result = run_cli(['list'])

    assert result.exit_code == 0
    assert "No tasks found" in result.output or "Total: 0" in result.output


# Additional contract tests for US2, US3, US4, US5 will be added in their respective phases
