# Todo CLI - Phase 1 Console Todo App

**AI-Native Todo SaaS Platform** - Phase 1: Python CLI with JSON storage

## Features

✅ **User Story 1 (P1)**: Add and View Tasks
✅ **User Story 2 (P2)**: Mark Tasks Complete
✅ **User Story 3 (P3)**: Update Task Details
✅ **User Story 4 (P4)**: Delete Tasks
✅ **User Story 5 (P5)**: Filter Tasks by Status/Priority

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Setup

```bash
# Install development dependencies (for testing)
pip install -r requirements-dev.txt

# No runtime dependencies - uses Python stdlib only!
```

## Usage

### Add a Task

```bash
# Minimal (title only)
python src/todo_cli.py add "Buy groceries"

# With all options
python src/todo_cli.py add "Submit report" \
  --description "Q4 financial analysis" \
  --due-date 2025-12-15 \
  --priority high
```

### List Tasks

```bash
# List all tasks
python src/todo_cli.py list

# Filter by status
python src/todo_cli.py list --status pending
python src/todo_cli.py list --status completed

# Filter by priority
python src/todo_cli.py list --priority high

# Sort tasks
python src/todo_cli.py list --sort-by due_date
python src/todo_cli.py list --sort-by priority
```

### Complete a Task

```bash
python src/todo_cli.py complete <task_id>

# Example
python src/todo_cli.py complete 1
```

### Update a Task

```bash
# Update title
python src/todo_cli.py update <task_id> --title "New title"

# Update multiple fields
python src/todo_cli.py update 2 \
  --priority high \
  --due-date 2025-12-10 \
  --description "Updated description"

# Change status (undo completion)
python src/todo_cli.py update 3 --status pending
```

### Delete a Task

```bash
# With confirmation prompt
python src/todo_cli.py delete <task_id>

# Skip confirmation
python src/todo_cli.py delete <task_id> --confirm
```

### Help

```bash
# General help
python src/todo_cli.py --help

# Command-specific help
python src/todo_cli.py add --help
python src/todo_cli.py list --help
```

## Task Model

Each task has 7 fields:

| Field | Type | Required | Default | Example |
|-------|------|----------|---------|---------|
| id | Integer | Auto | Sequential | 1 |
| title | String | Yes | - | "Buy groceries" |
| description | String | No | null | "Milk, eggs, bread" |
| status | Enum | Auto | "pending" | "pending" or "completed" |
| priority | Enum | No | "medium" | "low", "medium", "high" |
| due_date | ISO 8601 | No | null | "2025-12-31" |
| created_at | ISO 8601 | Auto | Current time | "2025-12-06T10:00:00" |

## Storage

Tasks are stored in `tasks.json` in the current working directory.

**Features**:
- Atomic writes (prevents corruption)
- Automatic creation on first run
- Human-readable JSON format

**Location**: `./tasks.json`

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test types
pytest tests/unit/ -v           # Unit tests
pytest tests/integration/ -v    # Integration tests
pytest tests/contract/ -v       # CLI contract tests

# Test coverage
pytest tests/ -v --cov=src --cov-report=html
```

**Test Results**: 42 tests, 100% passing ✅

## Project Structure

```
src/
├── todo_cli.py          # Main CLI entry point
├── models/
│   └── task.py          # Task entity model
├── services/
│   ├── task_service.py  # Business logic (CRUD)
│   └── storage.py       # JSON file persistence
└── utils/
    ├── validators.py    # Input validation
    └── formatters.py    # Output formatting

tests/
├── unit/                # Pure function tests
├── integration/         # Workflow tests
└── contract/            # CLI interface tests
```

## Constitution Compliance

✅ **Phase-Driven Evolution**: Phase 1 complete
✅ **Test-First Development**: 42 tests written before implementation
✅ **Simplicity**: Python stdlib only, no external dependencies
✅ **Data Integrity**: Atomic file writes, validation on all inputs
✅ **Exit Codes**: 0 (success), 1 (user error), 2 (system error)

## Performance

- **Startup**: <500ms
- **Operations**: <1s for 100 tasks
- **Storage**: ~500 bytes per task

## Next Phase

**Phase 2**: Full Web App
- Next.js frontend
- FastAPI backend
- Neon PostgreSQL database
- JWT authentication
- Multi-user support

See `specs/001-phase1-console-todo/spec.md` for complete specification.

## Documentation

- **Specification**: `specs/001-phase1-console-todo/spec.md`
- **Implementation Plan**: `specs/001-phase1-console-todo/plan.md`
- **Task Breakdown**: `specs/001-phase1-console-todo/tasks.md`
- **Data Model**: `specs/001-phase1-console-todo/data-model.md`
- **CLI Contracts**: `specs/001-phase1-console-todo/contracts/cli-commands.md`
- **User Guide**: `specs/001-phase1-console-todo/quickstart.md`

## License

MIT License - AI-Native Todo SaaS Platform

---

**Generated with TDD workflow** | **42 tests passing** | **Python 3.11+ stdlib only**
