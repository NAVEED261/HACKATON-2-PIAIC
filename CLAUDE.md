# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AI-Native Todo SaaS Platform** - A five-phase evolution from Python CLI to cloud-native enterprise application with AI chatbot integration.

**Current Phase**: ✅ Phase 1 Complete - Console Todo App (Python CLI with JSON storage)
**Status**: Production-ready, 50 tests passing, all 75 tasks complete
**Next Phase**: Phase 2 - Full Web App (Next.js + FastAPI + Neon PostgreSQL)

## Phase Evolution Architecture

This project follows a strict **Phase-Driven Evolution** where each phase builds on the previous:

1. **Phase 1** ✅ COMPLETE: Python CLI with JSON file storage, stdlib only (50 tests passing)
2. **Phase 2** 🎯 NEXT: Next.js frontend + FastAPI backend + Neon PostgreSQL + JWT auth
3. **Phase 3** ⏳ PLANNED: OpenAI Agents SDK + MCP tools for natural language task management
4. **Phase 4** ⏳ PLANNED: Docker + Kubernetes (Minikube) + Helm charts
5. **Phase 5** ⏳ PLANNED: DigitalOcean Kubernetes + Kafka event streaming + Dapr service mesh

**⚠️ CRITICAL**: Phase N+1 cannot start until Phase N is complete and tested. No premature features from future phases.

**Phase 1 Achievement**: ✅ All acceptance criteria met, constitution compliant, production-ready

## Phase 1 Completion Status ✅

**Completed**: 2025-12-07
**Tasks**: 75/75 (100%)
**Tests**: 50/50 passing (100%)
**Constitution Compliance**: ✅ PASS

### Implemented Features

✅ **User Story 1 (P1)**: Add and View Tasks - MVP
✅ **User Story 2 (P2)**: Mark Tasks Complete
✅ **User Story 3 (P3)**: Update Task Details
✅ **User Story 4 (P4)**: Delete Tasks
✅ **User Story 5 (P5)**: Filter Tasks by Status/Priority

### Test Coverage

- **Contract Tests**: 6 tests (CLI interface validation)
- **Integration Tests**: 11 tests (storage, workflows)
- **Unit Tests**: 33 tests (models, validators, services, formatters)
- **Total**: 50 tests, 100% passing

### Phase 1 Tech Stack

- **Language**: Python 3.14.0 (compatible with 3.11+)
- **Dependencies**: Python stdlib only (json, datetime, pathlib, sys, argparse)
- **Runtime Dependencies**: 0 (zero external packages)
- **Dev Dependencies**: pytest only
- **Storage**: JSON file (`tasks.json` in current working directory)
- **CLI Framework**: argparse (stdlib)
- **Performance**: ✅ <500ms startup, ✅ <1s for 100 tasks

## Project Structure

```
specs/
├── 001-phase1-console-todo/        # Phase 1 feature documentation
│   ├── spec.md                      # User stories (P1-P5 prioritized)
│   ├── plan.md                      # Architecture and technical decisions
│   ├── tasks.md                     # 75 implementation tasks (TDD workflow)
│   ├── data-model.md                # Task entity schema
│   ├── contracts/cli-commands.md    # CLI interface contracts
│   ├── quickstart.md                # User guide
│   └── research.md                  # Technology decisions

src/
├── todo_cli.py                      # Main CLI entry point (argparse)
├── models/task.py                   # Task entity (7 fields)
├── services/
│   ├── task_service.py              # CRUD operations
│   └── storage.py                   # JSON persistence (atomic writes)
└── utils/
    ├── validators.py                # Input validation
    └── formatters.py                # Output formatting

tests/
├── unit/                            # Pure function tests
├── integration/                     # Storage and workflow tests
└── contract/                        # CLI interface contract tests

.specify/
├── memory/constitution.md           # Project principles and standards
├── templates/                       # Spec-Driven Development templates
└── scripts/                         # Automation scripts

history/
├── prompts/                         # Prompt History Records (PHRs)
└── adr/                            # Architectural Decision Records
```

## Development Commands

### Testing (Phase 1)

```bash
# Install dev dependencies
pip install pytest

# Run all tests
pytest tests/ -v

# Run specific test types
pytest tests/unit/ -v                          # Unit tests only
pytest tests/integration/ -v                   # Integration tests only
pytest tests/contract/test_cli_interface.py -v # CLI contract tests

# Run tests for specific user story
pytest tests/ -k "US1" -v                      # User Story 1 tests
```

### Running the CLI (Phase 1)

```bash
# Run CLI directly
python src/todo_cli.py --help

# Add task
python src/todo_cli.py add "Task title" --description "Details" --priority high

# List tasks
python src/todo_cli.py list
python src/todo_cli.py list --status pending --priority high

# Complete task
python src/todo_cli.py complete <task_id>

# Update task
python src/todo_cli.py update <task_id> --title "New title" --priority high

# Delete task
python src/todo_cli.py delete <task_id> --confirm
```

### Spec-Driven Development Workflow

```bash
# Create constitution (project principles)
/sp.constitution

# Create feature specification
/sp.specify

# Create implementation plan
/sp.plan

# Generate task list
/sp.tasks

# Execute implementation (TDD workflow)
/sp.implement
```

## Constitution Compliance (Phase 1)

### Test-First Development (NON-NEGOTIABLE)

**TDD Workflow**: Write tests → Verify FAIL → Implement → Verify PASS

1. Write all test tasks for a user story FIRST (marked in tasks.md)
2. Run tests and verify they FAIL
3. Implement functionality
4. Run tests and verify they PASS
5. Checkpoint validation before next story

### Simplicity & Incremental Complexity

**Phase 1 Constraints**:
- ✅ Pure Python CLI (no frameworks)
- ✅ Python stdlib only (no external dependencies except pytest for testing)
- ✅ JSON file storage (simplest persistence)
- ❌ No web frameworks (deferred to Phase 2)
- ❌ No database (deferred to Phase 2)
- ❌ No AI/LLM integration (deferred to Phase 3)
- ❌ No containers/K8s (deferred to Phase 4)

## Task Entity Schema

The Task model (defined in data-model.md) has 7 fields designed for Phase 2 PostgreSQL migration:

```python
{
  "id": int,              # Sequential, starting from 1
  "title": str,           # Required, max 200 chars
  "description": str,     # Optional, max 1000 chars
  "status": str,          # "pending" or "completed"
  "priority": str,        # "low", "medium", "high"
  "due_date": str,        # ISO 8601 (YYYY-MM-DD), optional
  "created_at": str       # ISO 8601 timestamp, auto-generated
}
```

## User Stories (Priority Order)

Defined in `specs/001-phase1-console-todo/spec.md`:

- **P1**: Add and View Tasks (MVP - 19 tasks)
- **P2**: Mark Tasks Complete (8 tasks)
- **P3**: Update Task Details (7 tasks)
- **P4**: Delete Tasks (7 tasks)
- **P5**: Filter Tasks by Status (8 tasks)

Each story is independently testable and can be implemented in isolation after the Foundational phase (T007-T012).

## Implementation Tasks (tasks.md)

**Total**: 75 tasks across 8 phases

**MVP Scope** (31 tasks):
- Phase 1: Setup (T001-T006)
- Phase 2: Foundational (T007-T012) ⚠️ **BLOCKS all user stories**
- Phase 3: User Story 1 - Add/View (T013-T031)

**TDD Breakdown**:
- Test tasks: 30 (40%)
- Implementation tasks: 45

## Critical Patterns

### Atomic File Writes (storage.py)

Prevent data corruption using temp file + rename pattern:

```python
import tempfile
import shutil

def save_tasks(tasks, file_path='tasks.json'):
    with tempfile.NamedTemporaryFile('w', delete=False, dir='.') as tmp:
        json.dump(tasks, tmp, indent=2)
        tmp_path = tmp.name
    shutil.move(tmp_path, file_path)  # Atomic rename
```

### Sequential ID Generation (task_service.py)

```python
def get_next_id(tasks: list) -> int:
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1
```

### Date Validation (validators.py)

```python
from datetime import datetime

def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
```

## Error Handling Standards

- **User Errors** (invalid input, task not found): Exit code 1, friendly message
- **System Errors** (file I/O, JSON corruption): Exit code 2, recovery suggestion
- **Success**: Exit code 0

Example:
```python
try:
    tasks = load_tasks()
except FileNotFoundError:
    tasks = []  # First run
except json.JSONDecodeError:
    print("Error: tasks.json is corrupted. Backup and delete to reset.")
    sys.exit(2)
```

## Phase 2 Migration Path

Phase 1 is designed for clean Phase 2 migration:

- Task model → SQLAlchemy ORM model (same 7 fields + user_id)
- JSON storage → Neon PostgreSQL
- CLI commands → FastAPI REST endpoints
- task_service.py → Reusable business logic layer

## Spec-Driven Development (SDD)

This project follows SDD workflow managed via `.specify/` templates and scripts:

1. **Constitution** (`.specify/memory/constitution.md`): Project principles
2. **Specification** (`specs/<feature>/spec.md`): User stories and requirements
3. **Plan** (`specs/<feature>/plan.md`): Architecture and technical decisions
4. **Tasks** (`specs/<feature>/tasks.md`): Implementation task list
5. **PHRs** (`history/prompts/`): Prompt History Records for traceability
6. **ADRs** (`history/adr/`): Architectural Decision Records

## Phase 2 Readiness

**Migration Path**: Phase 1 → Phase 2

### Ready for Migration

✅ **Task Entity**: 7 fields map directly to PostgreSQL schema
✅ **Business Logic**: CRUD operations in `task_service.py` ready for API layer
✅ **Data Model**: Schema designed for Neon PostgreSQL migration
✅ **Service Layer**: Clean separation ready for FastAPI endpoints

### Phase 2 Requirements

**Frontend**: Next.js 14+ with TypeScript
**Backend**: FastAPI with Python 3.11+
**Database**: Neon PostgreSQL (serverless)
**Auth**: JWT tokens with refresh mechanism
**Migration**: Convert JSON → PostgreSQL with migration script

### Next Steps for Phase 2

1. Run `/sp.specify` to create Phase 2 specification
2. Design API endpoints (RESTful CRUD)
3. Plan database schema migration
4. Implement authentication system
5. Build Next.js frontend

## Documentation References

### Phase 1 Documentation ✅ COMPLETE

- **Constitution**: `.specify/memory/constitution.md` (comprehensive principles)
- **Phase 1 Spec**: `specs/001-phase1-console-todo/spec.md` (user stories P1-P5)
- **Phase 1 Plan**: `specs/001-phase1-console-todo/plan.md` (technical context)
- **Phase 1 Tasks**: `specs/001-phase1-console-todo/tasks.md` (75 tasks, ALL COMPLETE ✅)
- **Data Model**: `specs/001-phase1-console-todo/data-model.md` (Task entity schema)
- **CLI Contracts**: `specs/001-phase1-console-todo/contracts/cli-commands.md`
- **User Guide**: `specs/001-phase1-console-todo/quickstart.md`
- **Compliance**: `CONSTITUTION-COMPLIANCE.md` (Phase 1 validation)
- **User Documentation**: `README.md` (installation and usage)

### Phase 2 Documentation 🎯 READY FOR IMPLEMENTATION

**Branch**: `002-full-web-app`
**Status**: Planning complete, tasks generated, ready for `/sp.implement` command

- **Phase 2 Spec**: `specs/002-full-web-app/spec.md` (5 user stories P1-P5, 30 functional requirements)
- **Phase 2 Plan**: `specs/002-full-web-app/plan.md` (architecture, constitution compliance)
- **Phase 2 Tasks**: `specs/002-full-web-app/tasks.md` (176 implementation tasks organized by user story)
- **Research**: `specs/002-full-web-app/research.md` (technology decisions and best practices)
- **Data Model**: `specs/002-full-web-app/data-model.md` (User, Task, RefreshToken entities with SQLAlchemy)
- **API Contracts**: `specs/002-full-web-app/contracts/` (REST API documentation + OpenAPI 3.0 spec)
- **Quickstart**: `specs/002-full-web-app/quickstart.md` (development environment setup)
- **Requirements Checklist**: `specs/002-full-web-app/checklists/requirements.md` (spec validation)

**Phase 2 Tech Stack**:
- **Frontend**: Next.js 14+ (TypeScript, React 18+, TailwindCSS)
- **Backend**: FastAPI (Python 3.11+, SQLAlchemy, Alembic, PyJWT, bcrypt)
- **Database**: Neon PostgreSQL (serverless, cloud-hosted)
- **Email**: SendGrid (free tier 100 emails/day)
- **Testing**: pytest (backend), Jest/Vitest (frontend), Playwright (E2E)
- **Deployment**: Vercel (frontend), Railway/Render (backend), Neon (database)

**Phase 2 Key Features**:
- User registration and authentication (JWT tokens)
- Task CRUD operations via REST API
- Multi-user support with data isolation
- Password reset via email verification
- User profile management
- Real-time task sync across devices
- Task search and advanced filtering

**Phase 2 Database Schema**:
```sql
-- Users table (new in Phase 2)
users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  display_name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
)

-- Tasks table (Phase 1 schema + user_id + updated_at)
tasks (
  id SERIAL PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  status VARCHAR(20) DEFAULT 'pending',
  priority VARCHAR(10) DEFAULT 'medium',
  due_date DATE,
  created_at TIMESTAMP DEFAULT NOW(),
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,  -- NEW
  updated_at TIMESTAMP DEFAULT NOW()                       -- NEW
)

-- Refresh tokens table (new in Phase 2)
refresh_tokens (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(500) UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
)
```

**Phase 2 Implementation Tasks**: 176 tasks total
- Setup (15 tasks): Project initialization, dependencies
- Foundational (20 tasks): Database, models, shared utilities - BLOCKS all user stories
- US1 Authentication (46 tasks): Registration, login, JWT, password reset
- US2 Task Management (35 tasks): CRUD operations, filtering, data isolation
- US3 Real-Time Sync (18 tasks): Multi-device sync, offline support
- US4 User Profile (15 tasks): Account settings, preferences, dark mode
- US5 Search & Filtering (11 tasks): Advanced search, date ranges
- Polish (16 tasks): Security, performance, error handling, deployment

**MVP Scope** (111 tasks): Setup + Foundational + US1 + US2 + Essential polish

**Next Step**: Run `/sp.implement` to execute TDD workflow and begin implementation
