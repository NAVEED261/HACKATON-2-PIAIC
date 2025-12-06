# CLI Command Contracts: Phase 1 - Console Todo App

**Date**: 2025-12-06
**Feature**: 001-phase1-console-todo
**Purpose**: Define command-line interface contracts for all CLI operations

## Command Structure

```
todo <command> [arguments] [options]
```

## Commands Overview

| Command | Purpose | Priority |
|---------|---------|----------|
| `add` | Create a new task | P1 |
| `list` | Display all or filtered tasks | P1 |
| `complete` | Mark a task as completed | P2 |
| `update` | Modify task details | P3 |
| `delete` | Remove a task | P4 |

---

## 1. Add Task

### Command

```bash
todo add <title> [--description TEXT] [--due-date YYYY-MM-DD] [--priority LEVEL]
```

### Arguments

- **title** (required): Task title as a string
  - If title contains spaces, wrap in quotes: `"Buy groceries"`
  - Max length: 200 characters

### Options

- **--description, -d** (optional): Task description
  - Max length: 1000 characters
  - Example: `-d "Milk, eggs, bread"`

- **--due-date** (optional): Task due date
  - Format: YYYY-MM-DD (ISO 8601)
  - Must be a valid date
  - Example: `--due-date 2025-12-31`

- **--priority, -p** (optional): Task priority level
  - Valid values: `low`, `medium`, `high`
  - Default: `medium`
  - Example: `-p high`

### Success Output

```
Task added successfully!
ID: 5
Title: Buy groceries
Status: pending
```

### Error Outputs

**Empty title**:
```
Error: Title cannot be empty
```

**Invalid date format**:
```
Error: Invalid date format. Use YYYY-MM-DD
Example: 2025-12-31
```

**Invalid priority**:
```
Error: Priority must be one of: low, medium, high
```

### Examples

```bash
# Minimal task (title only)
todo add "Call dentist"

# Full task with all options
todo add "Submit Q4 report" -d "Financial analysis for board meeting" --due-date 2025-12-15 -p high

# Task with description only
todo add "Read documentation" --description "Django REST framework tutorial"
```

### Contract Tests

```python
# tests/contract/test_cli_interface.py

def test_add_task_minimal():
    result = run_cli(['add', 'Buy groceries'])
    assert result.exit_code == 0
    assert "Task added successfully" in result.output
    assert "ID:" in result.output

def test_add_task_full():
    result = run_cli(['add', 'Submit report', '-d', 'Q4 analysis', '--due-date', '2025-12-15', '-p', 'high'])
    assert result.exit_code == 0
    assert "Task added successfully" in result.output

def test_add_task_empty_title():
    result = run_cli(['add', ''])
    assert result.exit_code == 1
    assert "Title cannot be empty" in result.output

def test_add_task_invalid_date():
    result = run_cli(['add', 'Task', '--due-date', '12/31/2025'])
    assert result.exit_code == 1
    assert "Invalid date format" in result.output
```

---

## 2. List Tasks

### Command

```bash
todo list [--status STATUS] [--priority PRIORITY] [--sort-by FIELD]
```

### Options

- **--status, -s** (optional): Filter by task status
  - Valid values: `pending`, `completed`, `all`
  - Default: `all`
  - Example: `-s pending`

- **--priority, -p** (optional): Filter by priority level
  - Valid values: `low`, `medium`, `high`
  - Example: `-p high`

- **--sort-by** (optional): Sort tasks by field
  - Valid values: `id`, `title`, `due_date`, `priority`, `created_at`
  - Default: `id` (ascending)
  - Example: `--sort-by due_date`

### Success Output (Table Format)

```
ID    Title                          Status       Priority    Due Date
-----------------------------------------------------------------------------
1     Buy groceries                  pending      high        2025-12-08
2     Call dentist                   pending      medium      N/A
3     Submit report                  completed    high        2025-12-05
5     Read documentation             pending      low         2025-12-20

Total: 4 tasks (3 pending, 1 completed)
```

### Empty State Output

```
No tasks found.
```

### Filtered Output Example

```bash
todo list --status pending --priority high
```

```
ID    Title                          Status       Priority    Due Date
-----------------------------------------------------------------------------
1     Buy groceries                  pending      high        2025-12-08

Total: 1 task
```

### Contract Tests

```python
def test_list_all_tasks():
    result = run_cli(['list'])
    assert result.exit_code == 0
    assert "ID" in result.output
    assert "Title" in result.output

def test_list_filter_pending():
    result = run_cli(['list', '--status', 'pending'])
    assert result.exit_code == 0
    assert "pending" in result.output.lower()
    # Should not contain completed tasks

def test_list_empty():
    # Clear all tasks first
    result = run_cli(['list'])
    assert result.exit_code == 0
    assert "No tasks found" in result.output or "Total: 0" in result.output
```

---

## 3. Complete Task

### Command

```bash
todo complete <task_id>
```

### Arguments

- **task_id** (required): Numeric ID of the task to mark as completed
  - Must be a valid integer
  - Task must exist
  - Example: `5`

### Success Output

```
Task #5 marked as completed!
Title: Buy groceries
```

### Error Outputs

**Task not found**:
```
Error: Task with ID 999 not found
```

**Invalid ID (non-numeric)**:
```
usage: todo complete [-h] task_id
todo complete: error: argument task_id: invalid int value: 'abc'
```

### Examples

```bash
# Mark task 3 as complete
todo complete 3
```

### Contract Tests

```python
def test_complete_task_success():
    # Add a task first
    add_result = run_cli(['add', 'Test task'])
    task_id = extract_id(add_result.output)

    # Complete it
    result = run_cli(['complete', str(task_id)])
    assert result.exit_code == 0
    assert "marked as completed" in result.output

    # Verify status changed
    list_result = run_cli(['list'])
    assert "completed" in list_result.output

def test_complete_nonexistent_task():
    result = run_cli(['complete', '9999'])
    assert result.exit_code == 1
    assert "not found" in result.output.lower()
```

---

## 4. Update Task

### Command

```bash
todo update <task_id> [--title TEXT] [--description TEXT] [--due-date YYYY-MM-DD] [--priority LEVEL] [--status STATUS]
```

### Arguments

- **task_id** (required): Numeric ID of the task to update
  - Must be a valid integer
  - Task must exist

### Options

- **--title** (optional): New task title
- **--description** (optional): New description
- **--due-date** (optional): New due date (YYYY-MM-DD)
- **--priority** (optional): New priority (`low`, `medium`, `high`)
- **--status** (optional): New status (`pending`, `completed`)

**Note**: At least one option must be provided

### Success Output

```
Task #2 updated successfully!
Updated fields: title, priority
```

### Error Outputs

**Task not found**:
```
Error: Task with ID 99 not found
```

**No fields to update**:
```
Error: At least one field must be specified to update
```

**Invalid field value** (same as `add` command errors)

### Examples

```bash
# Update title only
todo update 2 --title "Client meeting at 3pm"

# Update multiple fields
todo update 5 --priority high --due-date 2025-12-10

# Change status (undo completion)
todo update 3 --status pending
```

### Contract Tests

```python
def test_update_task_title():
    task_id = create_test_task()
    result = run_cli(['update', str(task_id), '--title', 'New title'])
    assert result.exit_code == 0
    assert "updated successfully" in result.output

def test_update_task_no_fields():
    task_id = create_test_task()
    result = run_cli(['update', str(task_id)])
    assert result.exit_code == 1
    assert "at least one field" in result.output.lower()

def test_update_nonexistent_task():
    result = run_cli(['update', '9999', '--title', 'Test'])
    assert result.exit_code == 1
    assert "not found" in result.output.lower()
```

---

## 5. Delete Task

### Command

```bash
todo delete <task_id> [--confirm]
```

### Arguments

- **task_id** (required): Numeric ID of the task to delete
  - Must be a valid integer
  - Task must exist

### Options

- **--confirm, -y** (optional): Skip confirmation prompt
  - Default: Prompt for confirmation

### Success Output (with confirmation)

```
Are you sure you want to delete task #5: "Buy groceries"? (y/N): y
Task #5 deleted successfully!
```

### Success Output (with --confirm flag)

```
Task #5 deleted successfully!
```

### Cancelled Deletion

```
Are you sure you want to delete task #5: "Buy groceries"? (y/N): n
Deletion cancelled.
```

### Error Outputs

**Task not found**:
```
Error: Task with ID 99 not found
```

### Examples

```bash
# Delete with confirmation prompt
todo delete 5

# Delete without prompt (auto-confirm)
todo delete 5 --confirm
```

### Contract Tests

```python
def test_delete_task_with_confirm():
    task_id = create_test_task()
    result = run_cli(['delete', str(task_id), '--confirm'])
    assert result.exit_code == 0
    assert "deleted successfully" in result.output

def test_delete_nonexistent_task():
    result = run_cli(['delete', '9999', '--confirm'])
    assert result.exit_code == 1
    assert "not found" in result.output.lower()

def test_delete_task_cancelled(monkeypatch):
    task_id = create_test_task()
    # Simulate user entering 'n' at prompt
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    result = run_cli(['delete', str(task_id)])
    assert result.exit_code == 0
    assert "cancelled" in result.output.lower()

    # Verify task still exists
    list_result = run_cli(['list'])
    assert str(task_id) in list_result.output
```

---

## Help Command

### Command

```bash
todo --help
todo <command> --help
```

### Output (Main Help)

```
usage: todo [-h] {add,list,complete,update,delete} ...

Todo CLI - Manage your tasks from the command line

positional arguments:
  {add,list,complete,update,delete}
    add                 Add a new task
    list                List all tasks
    complete            Mark a task as completed
    update              Update task details
    delete              Delete a task

optional arguments:
  -h, --help            show this help message and exit
```

### Output (Command-Specific Help)

```bash
todo add --help
```

```
usage: todo add [-h] [--description TEXT] [--due-date YYYY-MM-DD] [--priority {low,medium,high}] title

Add a new task

positional arguments:
  title                 Task title

optional arguments:
  -h, --help            show this help message and exit
  --description TEXT, -d TEXT
                        Task description
  --due-date YYYY-MM-DD
                        Due date (format: YYYY-MM-DD)
  --priority {low,medium,high}, -p {low,medium,high}
                        Task priority (default: medium)
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | User error (invalid input, task not found) |
| 2 | System error (file I/O, JSON corruption) |

---

## Contract Test Suite Summary

```
tests/contract/test_cli_interface.py
├── test_add_task_minimal
├── test_add_task_full
├── test_add_task_empty_title
├── test_add_task_invalid_date
├── test_list_all_tasks
├── test_list_filter_pending
├── test_list_empty
├── test_complete_task_success
├── test_complete_nonexistent_task
├── test_update_task_title
├── test_update_task_no_fields
├── test_update_nonexistent_task
├── test_delete_task_with_confirm
├── test_delete_task_cancelled
├── test_delete_nonexistent_task
└── test_help_command
```

All commands must pass contract tests before implementation is considered complete.
