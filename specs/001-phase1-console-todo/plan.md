# Implementation Plan: Phase 1 - Console Todo App

**Branch**: `001-phase1-console-todo` | **Date**: 2025-12-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase1-console-todo/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a Python CLI todo application that establishes core task management logic (add, update, delete, list, mark complete) as the foundation for the AI-Native Todo SaaS Platform. This phase uses only Python standard library with JSON file-based persistence, implementing the Task entity model that will migrate to PostgreSQL in Phase 2 and support AI integration in Phase 3.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: None (Python standard library only - json, datetime, pathlib, sys, argparse)
**Storage**: JSON file (`tasks.json`) in user's home directory or current working directory
**Testing**: pytest (unit, integration, contract tests)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux) via terminal/command prompt
**Project Type**: Single project (Python CLI application)
**Performance Goals**: All operations complete in < 1 second for up to 100 tasks; startup time < 500ms
**Constraints**: Offline-only operation; no network dependencies; single-user local storage; no external package dependencies
**Scale/Scope**: Support 1-1000 tasks per user; single installation per user; file size < 1MB typical workload

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase 1 Principles (from Constitution)

✅ **I. Phase-Driven Evolution** - PASS
- Implementing Phase 1 only (console app)
- No premature Phase 2/3/4/5 features
- Clear foundation for Phase 2 migration path

✅ **VIII. Test-First Development** - PASS
- TDD workflow: Write tests → User approval → Implement
- pytest for unit and integration tests
- Test coverage for all CRUD operations

✅ **X. Simplicity & Incremental Complexity** - PASS
- No frameworks (pure Python CLI)
- Standard library only (no pip dependencies)
- JSON file storage (simplest persistence mechanism)
- No premature optimization

✅ **Phase 1 Technology Stack Compliance** - PASS
- Python 3.11+ ✓
- No dependencies (stdlib only) ✓
- JSON file storage ✓

### Principles Not Applicable to Phase 1

- **II. Cloud-Native Architecture** - Deferred to Phase 2+ (web app, containers)
- **III. AI-First Integration** - Deferred to Phase 3 (OpenAI Agents SDK)
- **IV. Event-Driven Communication** - Deferred to Phase 5 (Kafka)
- **V. Dapr Service Mesh** - Deferred to Phase 5 (cloud deployment)
- **VI. Database-Backed Persistence** - Deferred to Phase 2 (Neon PostgreSQL)
- **VII. Authentication & Authorization** - Deferred to Phase 2 (JWT, multi-user)
- **IX. Observability & Monitoring** - Deferred to Phase 2+ (structured logging acceptable for CLI)

### Constitution Gates: ✅ ALL PASS

No violations. Phase 1 implementation fully complies with constitution requirements.

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-console-todo/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (CLI design patterns, JSON storage best practices)
├── data-model.md        # Phase 1 output (Task entity schema)
├── quickstart.md        # Phase 1 output (User guide for CLI operations)
├── contracts/           # Phase 1 output (CLI command interface contracts)
│   └── cli-commands.md  # Command syntax and expected outputs
└── checklists/
    └── requirements.md  # Spec quality checklist (completed)
```

### Source Code (repository root)

```text
src/
├── todo_cli.py          # Main CLI entry point (argument parsing, command routing)
├── models/
│   └── task.py          # Task entity class (id, title, description, status, priority, due_date, created_at)
├── services/
│   ├── task_service.py  # Business logic (CRUD operations, validation)
│   └── storage.py       # JSON file persistence (read/write tasks.json)
└── utils/
    ├── validators.py    # Input validation (title not empty, date format, priority values)
    └── formatters.py    # Output formatting (table display, status indicators)

tests/
├── unit/
│   ├── test_task_model.py       # Task entity validation
│   ├── test_task_service.py     # CRUD operation logic
│   ├── test_validators.py       # Input validation rules
│   └── test_formatters.py       # Output formatting
├── integration/
│   ├── test_storage.py          # JSON file read/write operations
│   └── test_cli_workflows.py    # End-to-end user workflows
└── contract/
    └── test_cli_interface.py    # Command-line interface contracts

tasks.json               # Task storage file (created at runtime, gitignored)
```

**Structure Decision**: Using **Option 1: Single project** structure because Phase 1 is a standalone CLI application with no web/mobile components. The `src/` directory follows standard Python package layout with clear separation of concerns:

- **models/** - Data structures (Task entity)
- **services/** - Business logic and persistence
- **utils/** - Cross-cutting utilities (validation, formatting)
- **tests/** - Comprehensive test coverage organized by test type

This structure enables clean migration to Phase 2:
- `models/task.py` → becomes SQLAlchemy/Prisma model
- `services/task_service.py` → becomes FastAPI service layer
- CLI interface → becomes REST API endpoints

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations** - Constitution Check passed all gates. No complexity tracking required.
