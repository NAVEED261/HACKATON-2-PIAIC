# Research: Phase 1 - Console Todo App

**Date**: 2025-12-06
**Feature**: 001-phase1-console-todo
**Purpose**: Document technology decisions and design patterns for Python CLI implementation

## Research Areas

### 1. CLI Design Patterns for Python

**Decision**: Use `argparse` with subcommands pattern

**Rationale**:
- Part of Python standard library (no dependencies)
- Industry-standard for CLI applications (used by git, docker CLIs)
- Supports subcommands (`todo add`, `todo list`, etc.) naturally
- Automatic help generation (`--help` flag)
- Type validation and error handling built-in

**Alternatives Considered**:
- **click**: More ergonomic API but requires external dependency (violates Phase 1 simplicity)
- **sys.argv parsing**: Too low-level, requires manual validation and help text
- **getopt**: Older, less intuitive than argparse

**Implementation Approach**:
```python
# Main CLI structure
parser = argparse.ArgumentParser(description='Todo CLI')
subparsers = parser.add_subparsers(dest='command')

# Subcommand: add
add_parser = subparsers.add_parser('add', help='Add a new task')
add_parser.add_argument('title', type=str, help='Task title')
add_parser.add_argument('--description', '-d', type=str, help='Task description')
add_parser.add_argument('--due-date', type=str, help='Due date (YYYY-MM-DD)')
add_parser.add_argument('--priority', choices=['low', 'medium', 'high'], default='medium')

# Similar for: list, complete, update, delete subcommands
```

---

### 2. JSON Storage Best Practices

**Decision**: Single `tasks.json` file with atomic write operations

**Rationale**:
- JSON is human-readable for debugging
- Native Python `json` module (no dependencies)
- Simple schema migration path to PostgreSQL in Phase 2
- Atomic writes prevent data corruption (write to temp file, then rename)

**Alternatives Considered**:
- **SQLite**: More robust but adds complexity for single-user CLI; overkill for Phase 1
- **CSV**: Less flexible for nested data (description, metadata)
- **Pickle**: Binary format, not human-readable, security concerns

**File Location**: Current working directory (`./tasks.json`) for simplicity; user can organize tasks per project folder

**Atomic Write Pattern**:
```python
import json
import tempfile
import shutil
from pathlib import Path

def save_tasks(tasks, file_path='tasks.json'):
    # Write to temp file first
    with tempfile.NamedTemporaryFile('w', delete=False, dir='.') as tmp:
        json.dump(tasks, tmp, indent=2)
        tmp_path = tmp.name

    # Atomic rename (prevents corruption if interrupted)
    shutil.move(tmp_path, file_path)
```

---

### 3. Task ID Generation Strategy

**Decision**: Sequential integer IDs starting from 1, persisted in JSON

**Rationale**:
- Simple and predictable for CLI users (type "1" not "a3f2b9c")
- Easy to reference in commands (`todo complete 5`)
- Matches database auto-increment behavior (Phase 2 compatibility)
- No external dependencies (UUID would require uuid module)

**Alternatives Considered**:
- **UUID**: More robust for distributed systems but overkill for single-user CLI
- **Timestamp-based**: Not user-friendly for CLI commands
- **Hash-based**: Collision risk, not sequential

**Implementation**:
```python
# Track highest ID in tasks list
def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1
```

---

### 4. Date Handling

**Decision**: Store as ISO 8601 strings (`YYYY-MM-DD`), validate with `datetime.strptime`

**Rationale**:
- ISO 8601 is internationally recognized standard
- Easy to parse and validate with stdlib `datetime` module
- JSON-serializable (strings)
- PostgreSQL-compatible for Phase 2 migration
- No timezone complexity (dates only, no times)

**Validation**:
```python
from datetime import datetime

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
```

---

### 5. Error Handling Strategy

**Decision**: Graceful error messages with exit codes; no stack traces for user errors

**Rationale**:
- CLI users should see clear error messages, not Python tracebacks
- Exit codes follow Unix conventions (0=success, 1=error)
- Differentiate user errors (invalid input) from system errors (file permissions)

**Error Types**:
- **User Errors**: Invalid task ID, empty title, bad date format → Print friendly message + exit(1)
- **System Errors**: File I/O errors, JSON corruption → Print error + recovery suggestion + exit(2)

**Example**:
```python
try:
    tasks = load_tasks()
except FileNotFoundError:
    # First run, create empty file
    tasks = []
except json.JSONDecodeError:
    print("Error: tasks.json is corrupted. Backup and delete to reset.")
    sys.exit(2)
```

---

### 6. Output Formatting

**Decision**: Tabular format with color-coded status (optional ANSI colors)

**Rationale**:
- Table format is scannable and CLI-friendly
- Color coding improves UX (green=completed, yellow=pending) but optional for compatibility
- Use built-in string formatting (no external libs like rich/tabulate)

**Implementation**:
```python
# Simple table without external dependencies
def format_task_list(tasks, use_color=True):
    if not tasks:
        print("No tasks found.")
        return

    # Header
    print(f"{'ID':<5} {'Title':<30} {'Status':<12} {'Priority':<10} {'Due Date':<12}")
    print("-" * 75)

    # Rows
    for task in tasks:
        status = task['status']
        if use_color:
            status = colorize_status(status)  # Green/yellow ANSI codes

        print(f"{task['id']:<5} {task['title']:<30} {status:<12} {task['priority']:<10} {task.get('due_date', 'N/A'):<12}")
```

---

### 7. Testing Strategy

**Decision**: pytest with separate unit/integration/contract test suites

**Rationale**:
- pytest is Python industry standard (even though it's external, testing tools are acceptable)
- Fixtures for test data setup
- Parameterized tests for edge cases
- Clear test organization matches TDD workflow

**Test Organization**:
- **Unit tests**: Pure functions (validators, formatters, Task model)
- **Integration tests**: Storage operations (file I/O), service layer
- **Contract tests**: CLI command interfaces (input/output contracts)

**Example**:
```python
# tests/unit/test_validators.py
import pytest
from src.utils.validators import validate_title, validate_date

def test_validate_title_success():
    assert validate_title("Buy groceries") == True

def test_validate_title_empty():
    assert validate_title("") == False

@pytest.mark.parametrize("date,expected", [
    ("2025-12-06", True),
    ("12/06/2025", False),
    ("2025-13-01", False),
])
def test_validate_date(date, expected):
    assert validate_date(date) == expected
```

---

### 8. Migration Path to Phase 2

**Decision**: Design Task model structure to match future PostgreSQL schema

**Rationale**:
- Minimize refactoring when migrating to SQLAlchemy/Prisma
- Same field names and types (id, title, description, status, priority, due_date, created_at)
- Service layer abstraction allows swapping storage backend

**Phase 2 Migration Plan**:
1. Task model → SQLAlchemy ORM model (same fields)
2. JSON storage → PostgreSQL database
3. CLI commands → REST API endpoints with same business logic
4. Add user_id foreign key for multi-user support

**Forward Compatibility**:
```python
# Phase 1: Dictionary-based Task
task = {
    'id': 1,
    'title': 'Buy groceries',
    'description': 'Milk, eggs, bread',
    'status': 'pending',
    'priority': 'medium',
    'due_date': '2025-12-08',
    'created_at': '2025-12-06T10:00:00'
}

# Phase 2: SQLAlchemy model (similar structure)
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default='pending')
    priority = Column(String, default='medium')
    due_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))  # New in Phase 2
```

---

## Technology Stack Summary

| Component | Technology | Justification |
|-----------|-----------|---------------|
| Language | Python 3.11+ | Constitution requirement |
| CLI Framework | argparse (stdlib) | No dependencies, industry standard |
| Storage | JSON file | Simple, human-readable, no dependencies |
| Date Handling | datetime (stdlib) | ISO 8601 support, PostgreSQL-compatible |
| Testing | pytest | Industry standard, TDD-friendly |
| Validation | Custom functions (stdlib) | No complex schemas needed |
| Output | String formatting + optional ANSI | No external dependencies |

---

## Unknowns Resolved

All technical context items from plan.md are now resolved:
- ✅ Language/Version: Python 3.11+
- ✅ Primary Dependencies: None (stdlib only)
- ✅ Storage: JSON file with atomic writes
- ✅ Testing: pytest with unit/integration/contract tests
- ✅ Performance: Sequential ID generation, in-memory operations
- ✅ CLI Design: argparse with subcommands
- ✅ Error Handling: Graceful messages, Unix exit codes

**No NEEDS CLARIFICATION items remain.**

---

## Next Steps

Proceed to **Phase 1: Design & Contracts** to generate:
1. `data-model.md` - Task entity schema and validation rules
2. `contracts/cli-commands.md` - Command-line interface contracts
3. `quickstart.md` - User guide for CLI operations
